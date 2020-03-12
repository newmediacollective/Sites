#
# content_manager.py
#

import os
import sys
import json
import getopt
import shutil

from subprocess import check_call, PIPE
from os.path import splitext, join, exists, dirname
from uuid import uuid4
from datetime import datetime
from post import Post, ImagePost, TextPost

import bullet

#
# Constants
#

image_file_extension = ".jpg"
text_file_extension = ".md"

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
        self.text_posts_dir = join(self.data_dir, "text_posts")

        self.content_dir = join(self.site_dir, "content")
        self.views_dir = join(self.content_dir, "views")
        self.images_dir = join(self.content_dir, "images")
        self.index_path = join(self.views_dir, "index.html")

    def create_image_post(self, image_path, caption, location):
        # Optimize image
        image_id = str(uuid4())
        optimized_image_filename = image_id + image_file_extension
        optimized_image_path = join(self.images_dir, optimized_image_filename)

        check_call(f"convert {image_path} -strip -auto-orient -sampling-factor 4:2:0 -quality 85 -interlace JPEG -colorspace RGB {optimized_image_path}", stderr = PIPE, shell = True)

        # Create post
        properties = self.get_properties()
        date_format = properties["date_format"]
        date = datetime.now().strftime(date_format)
        post = ImagePost(post_id = str(uuid4()), image_filename = optimized_image_filename, caption = caption, date = date, location = location)

        # Add post
        self.add_post_and_update(post)
        return post

    def create_text_post(self, text_file_path, location):
        text_file_id = str(uuid4())

        # Copy the original text file to the text_posts directory
        copied_text_filename = text_file_id + text_file_extension
        copied_text_file_path = join(self.text_posts_dir, copied_text_filename)
        shutil.copy(text_file_path, copied_text_file_path)

        # Create post
        properties = self.get_properties()
        date_format = properties["date_format"]
        date = datetime.now().strftime(date_format)
        post = TextPost(post_id = str(uuid4()), text_posts_dir = self.text_posts_dir, text_filename = copied_text_filename, date = date, location = location)

        # Add post
        self.add_post_and_update(post)
        return post

    def add_post_and_update(self, post):
        # Update posts
        posts = self.get_posts()
        posts.insert(0, post)
        post_json = [post.to_json() for post in posts]

        with open(self.posts_path, "w") as posts_file:
            json.dump(post_json, posts_file, sort_keys = True, indent = 4)

        # Hydrate templates
        self.hydrate_templates()

    def find_post(self, post_id):
        posts = self.get_posts()

        for post in posts:
            if post.post_id == post_id:
                return post

        return None
        
    def delete_post(self, post):
        if type(post) == ImagePost:
            content_file_path = join(self.images_dir, post.image_filename)
        elif type(post) == TextPost:
            content_file_path = join(self.text_posts_dir, post.text_filename)
        else:
            raise TypeError("Unknown post type")

        os.remove(content_file_path)

        posts = self.get_posts()
        posts = filter(lambda x: (x.post_id != post.post_id), posts)

        post_json = [post.to_json() for post in posts]
        with open(self.posts_path, "w") as posts_file:
            json.dump(post_json, posts_file, sort_keys = True, indent = 4)

        self.hydrate_templates()

    def update_post(self, post):
        posts = self.get_posts()

        for i, existing_post in enumerate(posts):
            if existing_post.post_id == post.post_id:
                posts[i] = post
                break

        post_json = [post.to_json() for post in posts]

        with open(self.posts_path, "w") as posts_file:
            json.dump(post_json, posts_file, sort_keys = True, indent = 4)

        self.hydrate_templates()

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
                posts = [Post.from_json(text_posts_dir = self.text_posts_dir, post_json = post_json) for post_json in json.load(posts_file)]

        return posts

#
# Command Line Interface
#

def create(content_manager, argv):
    if len(argv) < 2:
        fuck_off()

    post_type = argv[0]
    content_file_path = argv[1]

    if post_type == "image":
        caption = input("Caption: ")
        if len(caption) == 0:
            caption = None

        location = input("Location: ")
        if len(location) == 0:
            location = None

        content_manager.create_image_post(content_file_path, caption, location)
    elif post_type == "text":
        location = input("Location: ")
        if len(location) == 0:
            location = None

        content_manager.create_text_post(content_file_path, location)
    else:
        fuck_off()

def update(content_manager, argv):
    if len(argv) < 1:
        fuck_off()

    post_id = argv[0]
    post = content_manager.find_post(post_id)

    if post is None:
        print("Unknown post")
        return

    if type(post) == ImagePost:
        choices = ["Caption", "Location"]
    elif type(post) == TextPost:
        choices = ["Location", "Text"]
    else:
        raise TypeError("Unknown post type")

    choices.append("Nothing")
    choice = bullet.Bullet(prompt="What would you like to edit?", choices=choices, bullet=" ").launch()

    if choice == "Caption":
        caption = input("Caption: ")
        post.caption = caption
    elif choice == "Location":
        location = input("Location: ")
        post.location = location
    elif choice == "Text":
        text_file_path = join(content_manager.text_posts_dir, post.text_filename)
        check_call(f"vim {text_file_path}", stderr = PIPE, shell = True)
        content_manager.hydrate_templates()
    elif choice == "Nothing":
        pass
    else:
        raise ValueError("Unknown choice")

    content_manager.update_post(post)

def delete(content_manager, argv):
    if len(argv) < 1:
        fuck_off()

    post_id = argv[0]
    post = content_manager.find_post(post_id)

    if post is None:
        print("Unknown post")
        return

    sure = bullet.YesNo("Are you sure? ").launch()

    if sure:
        content_manager.delete_post(post)
        print("Post deleted")
    else:
        print("Aborting")

def generate(content_manager, argv):
    content_manager.hydrate_templates()

def main(argv):
    if len(argv) < 2:
        fuck_off()

    sitename = argv[0]
    action = argv[1]

    app_dir = dirname(os.path.realpath(__file__))
    content_manager = ContentManager(app_dir = app_dir, sitename = sitename)

    if action == "create":
        create(content_manager, argv[2:])
    elif action == "update":
        update(content_manager, argv[2:])
    elif action == "delete":
        delete(content_manager, argv[2:])
    elif action == "generate":
        generate(content_manager, argv[2:])
    elif action == "push":
        push(content_manager, argv[2:])
    else:
        fuck_off()

def fuck_off():
    usage  = "Usage:\n"
    usage += "    python3 content_manager.py <sitename> create <text | image> <content_file_path>\n"
    usage += "    python3 content_manager.py <sitename> update <post_id>\n"
    usage += "    python3 content_manager.py <sitename> delete <post_id>\n"
    usage += "    python3 content_manager.py <sitename> generate\n"
    usage += "    python3 content_manager.py <sitename> push\n"

    print(usage)
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
