#
# post.py
#

import abc
import json

from os.path import join
from datetime import datetime

from markdown_parser import *

#
# Post Abstract Base Class
#

stored_date_format = "%Y-%m-%d"

class Post(abc.ABC):

    def __init__(self, post_id):
        self.post_id = post_id

    @staticmethod
    def from_json(text_posts_dir, post_json):
        post_type = post_json["type"]

        if post_type == "text":
            return TextPost.from_json(text_posts_dir, post_json)
        elif post_type == "image":
            return ImagePost.from_json(post_json)
        elif post_type == "video":
            return VideoPost.from_json(post_json)
        else:
            raise Exception(f"Unknown post type: {post_type}")

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def to_html(self, properties):
        pass

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys = True, indent = 4)

#
# TextPost
#

class TextPost(Post):

    def __init__(self, post_id, text_posts_dir, text_filename, location, date):
        super().__init__(post_id)

        self.text_posts_dir = text_posts_dir
        self.text_filename = text_filename
        self.location = location
        self.date = date

    @staticmethod
    def from_json(text_posts_dir, post_json):
        return TextPost(
            post_id = post_json["id"],
            text_posts_dir = text_posts_dir,
            text_filename = post_json["text_filename"],
            location = post_json.get("location"),
            date = datetime.strptime(post_json["date"], stored_date_format)
        )

    def to_json(self):
        return {
            "id": self.post_id,
            "type": "text",
            "text_filename": self.text_filename,
            "location": self.location,
            "date": self.date.strftime(stored_date_format)
        }

    def to_html(self, properties):
        with open(join(self.text_posts_dir, self.text_filename), "r") as text_file:
            text = text_file.read()
            parsed_text = parse_full_markdown(text)

        html = f"""
            <div class="text_post" id="{self.post_id}">
                <div class="text">{parsed_text}</div>
        """

        if self.location:
            html += f"""
                <p class="location">{self.location}</p>
            """

        html += f"""
            <p class="date">{self.date.strftime(properties.date_format)}</p>
        """

        if properties.generate_post_pages:
            html += f"""
                <p class="permalink"><a href="../posts/{self.post_id}">∞</a></p>
            """

        return html + """
            </div>
        """

#
# ImagePost
#

class ImagePost(Post):

    def __init__(self, post_id, image_filename, caption, location, date):
        super().__init__(post_id)
        self.image_filename = image_filename
        self.caption = caption
        self.location = location
        self.date = date

    @staticmethod
    def from_json(post_json):
        return ImagePost(
            post_id = post_json["id"],
            image_filename = post_json["image_filename"],
            caption = post_json.get("caption"),
            location = post_json.get("location"),
            date = datetime.strptime(post_json["date"], stored_date_format)
        )

    def to_json(self):
        return {
            "id": self.post_id,
            "type": "image",
            "image_filename": self.image_filename,
            "caption": self.caption,
            "location": self.location,
            "date": self.date.strftime(stored_date_format)
        }

    def to_html(self, properties):
        parsed_caption = None
        alt_text = properties.alt_text_prefix

        if self.caption:
            parsed_caption = parse_light_markdown(self.caption)
            alt_text += f", {self.caption}"

        html = f"""
            <div class="image_post" id="{self.post_id}">
                <div class="image_link_div_fuck_css">
                    <a href="../images/{self.image_filename}" class="image_link">
                        <img src="../images/{self.image_filename}" alt="{alt_text}">
                    </a>
                </div>
        """

        if parsed_caption:
            html += f"""
                <p class="caption">{parsed_caption}</p>
            """

        if self.location:
            html += f"""
                <p class="location">{self.location}</p>
            """

        html += f"""
            <p class="date">{self.date.strftime(properties.date_format)}</p>
        """

        if properties.generate_post_pages:
            html += f"""
                <p class="permalink"><a href="../posts/{self.post_id}">∞</a></p>
            """

        return html + """
            </div>
        """

#
# VideoPost
#

class VideoPost(Post):

    def __init__(self, post_id, video_filename, thumbnail_filename, caption, location, date):
        super().__init__(post_id)
        self.video_filename = video_filename
        self.thumbnail_filename = thumbnail_filename
        self.caption = caption
        self.location = location
        self.date = date

    @staticmethod
    def from_json(post_json):
        return VideoPost(
            post_id = post_json["id"],
            video_filename = post_json["video_filename"],
            thumbnail_filename = post_json["thumbnail_filename"],
            caption = post_json.get("caption"),
            location = post_json.get("location"),
            date = datetime.strptime(post_json["date"], stored_date_format)
        )

    def to_json(self):
        return {
            "id": self.post_id,
            "type": "video",
            "video_filename": self.video_filename,
            "thumbnail_filename": self.thumbnail_filename,
            "caption": self.caption,
            "location": self.location,
            "date": self.date.strftime(stored_date_format)
        }

    def to_html(self, properties):
        html = f"""
            <div class="video_post" id="{self.post_id}">
                <video id="video_{self.post_id}" poster="../thumbnails/{self.thumbnail_filename}" onloadedmetadata="showVideoControls(this);">
                    <source type="video/mp4" src="../videos/{self.video_filename}">
                </video>
        """

        if self.caption:
            parsed_caption = parse_light_markdown(self.caption)
            html += f"""
                <p class="caption">{parsed_caption}</p>
            """

        if self.location:
            html += f"""
                <p class="location">{self.location}</p>
            """

        html += f"""
            <p class="date">{self.date.strftime(properties.date_format)}</p>
        """

        if properties.generate_post_pages:
            html += f"""
                <p class="permalink"><a href="../posts/{self.post_id}">∞</a></p>
            """

        return html + """
            </div>
        """
