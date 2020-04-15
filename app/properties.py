#
# properties.py
#

import json

class Properties:

    def __init__(self, json):
        self.site_title = json["site_title"]
        self.display_title = json["display_title"]
        self.subtitle = json["subtitle"]
        self.post_page_subtitle = json["post_page_subtitle"]
        self.description = json["description"]
        self.alt_text_prefix = json["alt_text_prefix"]
        self.date_format = json["date_format"]
        self.generate_post_pages = json["generate_post_pages"]
        self.icon_version = json["icon_version"]

    def to_json(self):
        return {
            "site_title": self.site_title,
            "display_title": self.display_title,
            "subtitle": self.subtitle,
            "post_page_subtitle": self.post_page_subtitle,
            "description": self.description,
            "alt_text_prefix": self.alt_text_prefix,
            "date_format": self.date_format,
            "generate_post_pages": self.generate_post_pages,
            "icon_version": self.icon_version
        }

    def renderable_items(self):
        keys = ["site_title", "display_title", "subtitle", "post_page_subtitle", "description", "icon_version"]

        return self.get_items(keys = keys)

    def get_items(self, keys):
        values = [str(self.to_json()[key]) for key in keys]

        return zip(keys, values)

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys = True, indent = 4)

    @staticmethod
    def default(title):
        return Properties({
            "site_title": title,
            "display_title": title,
            "subtitle": "",
            "post_page_subtitle": "",
            "description": "",
            "alt_text_prefix": "",
            "date_format": "%Y-%m-%d",
            "generate_post_pages": True,
            "icon_version": 0
        })
