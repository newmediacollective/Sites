#
# post.py
#

import json

#
# Post
#

class Post:
    def __init__(self, image_filename, caption, date):
        self.image_filename = image_filename
        self.caption = caption
        self.date = date

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys = True, indent = 4)

    def to_json(self):
        return {
            "image_filename": self.image_filename,
            "caption": self.caption,
            "date": self.date
        }

    @staticmethod
    def from_json(json):
        return Post(
            image_filename = json["image_filename"],
            caption = json["caption"],
            date = json["date"]
        )

    def to_html(self):
        if not self.caption:
            return f"""
    <div class="post">
        <a href="../images/{self.image_filename}">
            <img src="../images/{self.image_filename}" alt="">
        </a>
        <p class="date">{self.date}</p>
    </div>"""
        else:
            return f"""
    <div class="post">
        <a href="../images/{self.image_filename}">
            <img src="../images/{self.image_filename}" alt="">
        </a>
        <p class="caption">{self.caption}</p>
        <p class="date">{self.date}</p>
    </div>"""
