#
# post.py
#

import abc
import json

from os.path import join
from flask import escape

#
# Post Abstract Base Class
#

class Post(abc.ABC):
    @staticmethod
    def from_json(text_files_dir, post_json):
        post_type = post_json["type"]

        if post_type == "image":
            return ImagePost(
                content_filename = post_json["content_filename"],
                caption = post_json["caption"],
                date = post_json["date"],
                location = post_json["location"]
            )
        elif post_type == "text":
            return TextPost(
                text_files_dir = text_files_dir,
                content_filename = post_json["content_filename"],
                date = post_json["date"],
                location = post_json["location"]
            )
        else:
            raise Exception(f"Unknown post type: {post_type}")

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def to_html(self):
        pass

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys = True, indent = 4)

#
# ImagePost
#

class ImagePost(Post):
    def __init__(self, content_filename, caption, date, location):
        self.content_filename = content_filename
        self.caption = caption
        self.date = date
        self.location = location

    def to_json(self):
        return {
            "type": "image",
            "content_filename": self.content_filename,
            "caption": self.caption,
            "date": self.date,
            "location": self.location,
        }

    def to_html(self):
        return f"""
    <div class="post">
        <a href="../images/{self.content_filename}">
            <img src="../images/{self.content_filename}" alt="">
        </a>
        <p class="caption">{self.caption}</p>
        <p class="date">{self.date}</p>
        <p class="location">{self.location}</p>
    </div>"""

#
# TextPost
#

class TextPost(Post):
    def __init__(self, text_files_dir, content_filename, date, location):
        self.text_files_dir = text_files_dir
        self.content_filename = content_filename
        self.date = date
        self.location = location

    def to_json(self):
        return {
            "type": "text",
            "content_filename": self.content_filename,
            "date": self.date,
            "location": self.location,
        }

    def to_html(self):
        with open(join(self.text_files_dir, self.content_filename), "r") as text_file:
            text = str(escape(text_file.read()))

        text = text.replace("\n\n", "\n<br><br>\n")

        return f"""
    <div class="post">
        <p class="text">{text}</p>
        <p class="date">{self.date}</p>
        <p class="location">{self.location}</p>
    </div>"""
