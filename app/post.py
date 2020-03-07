#
# post.py
#

import json

#
# Post
#

class Post:
    def __init__(self, image_filename, caption, date, location):
        self.image_filename = image_filename
        self.caption = caption
        self.date = date
        self.location = location

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys = True, indent = 4)

    def to_json(self):
        return {
            "image_filename": self.image_filename,
            "caption": self.caption,
            "date": self.date,
            "location": self.location,
        }

    @staticmethod
    def from_json(post_json):
        return Post(
            image_filename = post_json["image_filename"],
            caption = post_json["caption"],
            date = post_json["date"],
            location = post_json["location"]
        )

    def to_html(self):
        return f"""
    <div class="post">
        <a href="../images/{self.image_filename}">
            <img src="../images/{self.image_filename}" alt="">
        </a>
        <p class="caption">{self.caption}</p>
        <p class="date">{self.date}</p>
        <p class="location">{self.location}</p>
    </div>"""
