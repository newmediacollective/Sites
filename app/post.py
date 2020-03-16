#
# post.py
#

import abc
import datetime
import json

from os.path import join
from markdown_parser import parse_markdown

#
# Constants
#

stored_date_format = "%Y-%m-%d"

#
# Post Abstract Base Class
#

class Post(abc.ABC):

    def __init__(self, post_id):
        self.post_id = post_id

    @staticmethod
    def from_json(text_posts_dir, post_json):
        post_type = post_json["type"]

        if post_type == "image":
            return ImagePost.from_json(post_json)
        elif post_type == "text":
            return TextPost.from_json(text_posts_dir, post_json)
        else:
            raise Exception(f"Unknown post type: {post_type}")

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def to_html(self, date_format):
        pass

    def format_date(self, date_format):
        date = datetime.datetime.strptime(self.date, stored_date_format).date()
        return date.strftime(date_format)

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys = True, indent = 4)

#
# ImagePost
#

class ImagePost(Post):
    def __init__(self, post_id, image_filename, caption, date, location):
        super().__init__(post_id)
        self.image_filename = image_filename
        self.caption = caption
        self.date = date
        self.location = location

    @staticmethod
    def from_json(post_json):
        return ImagePost(
            post_id = post_json["id"],
            image_filename = post_json["image_filename"],
            caption = post_json.get("caption"),
            date = post_json["date"],
            location = post_json.get("location")
        )

    def to_json(self):
        return {
            "id": self.post_id,
            "type": "image",
            "image_filename": self.image_filename,
            "caption": self.caption,
            "date": self.date,
            "location": self.location,
        }

    def to_html(self, date_format):
        formatted_date = self.format_date(date_format)

        html = f"""
    <div class="image_post" id="{self.post_id}">
        <div class="image_link_div_fuck_css">
            <a href="../images/{self.image_filename}" class="image_link">
                <img src="../images/{self.image_filename}" alt="">
            </a>
        </div>
        """

        if self.caption:
            html += f"""
        <p class="caption">{self.caption}</p>
    """

        if self.location:
            html += f"""
        <p class="location">{self.location}</p>
    """

        return html + f"""
        <p class="date">{formatted_date}</p>
        <p class="permalink"><a href="../posts/{self.post_id}.html">∞</a></p>
    </div>"""

#
# TextPost
#

class TextPost(Post):
    def __init__(self, post_id, text_posts_dir, text_filename, date, location):
        super().__init__(post_id)

        self.text_posts_dir = text_posts_dir
        self.text_filename = text_filename
        self.date = date
        self.location = location

    @staticmethod
    def from_json(text_posts_dir, post_json):
        return TextPost(
            post_id = post_json["id"],
            text_posts_dir = text_posts_dir,
            text_filename = post_json["text_filename"],
            date = post_json["date"],
            location = post_json.get("location")
        )

    def to_json(self):
        return {
            "id": self.post_id,
            "type": "text",
            "text_filename": self.text_filename,
            "date": self.date,
            "location": self.location,
        }

    def to_html(self, date_format):
        with open(join(self.text_posts_dir, self.text_filename), "r") as text_file:
            text = text_file.read()
            parsed_text = parse_markdown(text)

        formatted_date = self.format_date(date_format)

        html = f"""
    <div class="text_post" id="{self.post_id}">
        <div class="text">{parsed_text}</div>
    """

        if self.location:
            html += f"""
        <p class="location">{self.location}</p>
        """

        return html + f"""
        <p class="date">{formatted_date}</p>
        <p class="permalink"><a href="../posts/{self.post_id}.html">∞</a></p>
    </div>"""
