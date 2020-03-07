#
# content_manager.py
#

import os
import sys
import json
import getopt

from subprocess import check_call, PIPE
from os.path import splitext, join, exists, dirname
from uuid import uuid4
from datetime import datetime
from post import Post

#
# Constants
#

image_file_extension = ".jpg"

#
# ContentManager
#

class ContentManager:

    def __init__(self, app_dir, sitename):
        sites_dir = join(app_dir, "sites")

        self.sitename = sitename

        self.site_dir = join(sites_dir, sitename)
        self.templates_dir = join(self.site_dir, "templates")

        self.data_dir = join(self.site_dir, "data")
        self.properties_path = join(self.data_dir, "properties.json")
        self.posts_path = join(self.data_dir, "posts.json")

        self.content_dir = join(self.site_dir, "content")
        self.views_dir = join(self.content_dir, "views")
        self.images_dir = join(self.content_dir, "images")
        self.index_path = join(self.views_dir, "index.html")

    def create_post(self, image_path, caption, location):
        # Optimize image
        image_identifier = str(uuid4())
        optimized_image_filename = image_identifier + image_file_extension
        optimized_image_path = join(self.images_dir, optimized_image_filename)

        check_call(f"convert {image_path} -strip -auto-orient -sampling-factor 4:2:0 -quality 85 -interlace JPEG -colorspace RGB {optimized_image_path}", stderr = PIPE, shell = True)

        # Create post
        date = datetime.now().strftime("%b %-d, %Y")
        post = Post(image_filename = optimized_image_filename, caption = caption, date = date, location = location)

        # Update posts
        posts = self.get_posts()
        posts.insert(0, post)
        post_json = [post.to_json() for post in posts]

        with open(self.posts_path, "w") as posts_file:
            json.dump(post_json, posts_file, sort_keys = True, indent = 4)

        # Hydrate templates
        self.hydrate_templates()

        # Return the new post
        return post

    def hydrate_templates(self):
        properties = self.get_properties()

        template_names = [filename for filename in os.listdir(self.templates_dir)]

        for template_name in template_names:
            with open(join(self.templates_dir, template_name), "r") as template_file:
                template = template_file.read()

            view = template
            for key, value in properties.items():
                view = view.replace(f"{{{key}}}", value)

            with open(join(self.views_dir, template_name), "w") as view_file:
                view_file.write(view)

        with open(join(self.views_dir, self.index_path), "r") as index_file:
            index = index_file.read()

        posts = self.get_posts()
        post_html = "\n".join([post.to_html() for post in posts])
        index = index.replace("{posts}", post_html)

        with open(join(self.views_dir, self.index_path), "w") as index_file:
            index_file.write(index)

    def get_properties(self):
        properties = {}

        with open(self.properties_path, "r") as properties_file:
            properties = json.load(properties_file)

        return properties

    def get_posts(self):
        posts = []

        if exists(self.posts_path):
            with open(self.posts_path, "r") as posts_file:
                posts = [Post.from_json(post_json = post_json) for post_json in json.load(posts_file)]

        return posts

#
# Main
#

def regenerate(sitename):
    app_dir = dirname(os.path.realpath(__file__))
    content_manager = ContentManager(app_dir = app_dir, sitename = sitename)
    content_manager.hydrate_templates()

def main(argv):
    usage = "Usage: python3 content_manager.py regenerate -s sitename (e.g. google.com)"

    if len(argv) == 0:
        print(usage)
        sys.exit(2)

    action_name = argv[0]
    sitename = None

    try:
        opts, args = getopt.getopt(argv[1:],"s:")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-s":
            sitename = arg

    if action_name == "help":
        print(usage)
        sys.exit()
    elif action_name == "regenerate":
        regenerate(sitename = sitename)
    else:
        print(f"Error: unrecognized action\n{usage}")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
