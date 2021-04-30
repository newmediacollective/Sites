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

from post import *
from properties import *
from markdown_parser import *

import bullet

#
# Constants
#

image_file_extension = ".jpg"
video_file_extension = ".mp4"
text_file_extension = ".md"

#
# ContentManager
#

class ContentManager:

    #
    # Initialization
    #

    def __init__(self, app_dir, host):
        sites_dir = join(app_dir, "sites")

        self.host = host
        self.site_dir = join(sites_dir, host)

        self.templates_dir = join(self.site_dir, "templates")
        self.index_template_path = join(self.templates_dir, "index.html")
        self.error_template_path = join(self.templates_dir, "error.html")
        self.post_template_path = join(self.templates_dir, "post.html")

        self.data_dir = join(self.site_dir, "data")
        self.properties_path = join(self.data_dir, "properties.json")
        self.posts_path = join(self.data_dir, "posts.json")
        self.text_posts_dir = join(self.data_dir, "text_posts")

        self.content_dir = join(self.site_dir, "content")
        self.views_dir = join(self.content_dir, "views")
        self.images_dir = join(self.content_dir, "images")
        self.videos_dir = join(self.content_dir, "videos")
        self.thumbnails_dir = join(self.content_dir, "thumbnails")
        self.posts_dir = join(self.content_dir, "posts")
        self.index_path = join(self.views_dir, "index.html")
        self.error_path = join(self.views_dir, "error.html")

    #
    # Creating Posts
    #

    def create_text_post(self, text_file_path, location):
        text_file_id = str(uuid4())

        # Copy the original text file to the text_posts directory
        copied_text_filename = text_file_id + text_file_extension
        copied_text_file_path = join(self.text_posts_dir, copied_text_filename)
        shutil.copy(text_file_path, copied_text_file_path)

        # Create post
        post = TextPost(
            post_id = str(uuid4()),
            text_posts_dir = self.text_posts_dir,
            text_filename = copied_text_filename,
            location = location,
            date = datetime.now()
        )

        self.add_post_and_update(post = post)

        return post

    def create_image_post(self, image_path, caption, location):
        image_id = str(uuid4())

        # Optimize image
        optimized_image_filename = image_id + image_file_extension
        optimized_image_path = join(self.images_dir, optimized_image_filename)

        check_call(f"convert '{image_path}' -strip -auto-orient -sampling-factor 4:2:0 -quality 85 -interlace JPEG -colorspace RGB {optimized_image_path}", stderr = PIPE, shell = True)

        # Create post
        post = ImagePost(
            post_id = str(uuid4()),
            image_filename = optimized_image_filename,
            caption = caption,
            location = location,
            date = datetime.now()
        )

        self.add_post_and_update(post = post)

        return post

    def create_video_post(self, video_path, caption, location):
        video_id = str(uuid4())

        # Optimize video
        optimized_video_filename = video_id + video_file_extension
        optimized_video_path = join(self.videos_dir, optimized_video_filename)
        thumbnail_filename = video_id + image_file_extension
        thumbnail_path = join(self.thumbnails_dir, thumbnail_filename)

        if video_path.endswith(video_file_extension):
            shutil.copy(video_path, optimized_video_path)
        else:
            print("Optimizing video...")
            check_call(f"ffmpeg -i '{video_path}' {optimized_video_path}", stderr = PIPE, shell = True)

        print("Capturing thumbnail...")
        check_call(f"ffmpeg -ss 3 -i {optimized_video_path} -frames:v 1 -qscale:v 2 {thumbnail_path}", stderr = PIPE, shell = True)

        # Create post
        post = VideoPost(
            post_id = str(uuid4()),
            video_filename = optimized_video_filename,
            thumbnail_filename = thumbnail_filename,
            caption = caption,
            location = location,
            date = datetime.now()
        )

        self.add_post_and_update(post = post)

        return post

    #
    # Utilities
    #

    def get_properties(self):
        with open(self.properties_path, "r") as properties_file:
            properties_json = json.load(properties_file)
            properties = Properties(properties_json)

        return properties

    def get_posts(self):
        posts = []

        if exists(self.posts_path):
            with open(self.posts_path, "r") as posts_file:
                posts = [Post.from_json(text_posts_dir = self.text_posts_dir, post_json = post_json) for post_json in json.load(posts_file)]

        return posts

    def add_post_and_update(self, post):
        posts = self.get_posts()
        posts.insert(0, post)

        post_json = [post.to_json() for post in posts]

        with open(self.posts_path, "w") as posts_file:
            json.dump(post_json, posts_file, sort_keys = True, indent = 4)

        self.hydrate_templates()

    def find_post(self, post_id):
        posts = self.get_posts()

        for post in posts:
            if post.post_id == post_id:
                return post

        return None

    def delete_post(self, post):
        if type(post) == TextPost:
            content_file_path = join(self.text_posts_dir, post.text_filename)
        elif type(post) == ImagePost:
            content_file_path = join(self.images_dir, post.image_filename)
        elif type(post) == VideoPost:
            content_file_path = join(self.videos_dir, post.video_filename)
            thumbnail_path = join(self.thumbnails_dir, post.thumbnail_filename)
            os.remove(thumbnail_path)
        else:
            raise TypeError("Unknown post type")

        post_file_name = post.post_id + ".html"
        post_file_path = join(self.posts_dir, post_file_name)

        os.remove(content_file_path)
        os.remove(post_file_path)

        posts = self.get_posts()
        posts = filter(lambda x: (x.post_id != post.post_id), posts)

        post_json = [post.to_json() for post in posts]

        with open(self.posts_path, "w") as posts_file:
            json.dump(post_json, posts_file, sort_keys = True, indent = 4)

        self.hydrate_templates()

    #
    # Site Generation
    #

    def hydrate_templates(self):
        properties = self.get_properties()

        # Error template
        with open(self.error_template_path, "r") as error_template_file:
            error = error_template_file.read()

            for key, value in properties.renderable_items():
                error = error.replace(f"{{{key}}}", parse_light_markdown(value))

        with open(self.error_path, "w") as error_file:
            error_file.write(error)

        # Index template
        with open(self.index_template_path, "r") as index_file:
            index = index_file.read()

            for key, value in properties.renderable_items():
                index = index.replace(f"{{{key}}}", parse_light_markdown(value))

        # Post template
        if properties.generate_post_pages:
            with open(self.post_template_path, "r") as post_template_file:
                post_template = post_template_file.read()

                for key, value in properties.renderable_items():
                    post_template = post_template.replace(f"{{{key}}}", parse_light_markdown(value))

        # Generate post HTML
        posts = self.get_posts()
        post_htmls = [post.to_html(properties) for post in posts]
        post_html = "\n".join(post_htmls)

        # Write to index
        index = index.replace("{posts}", post_html)

        with open(join(self.views_dir, self.index_path), "w") as index_file:
            index_file.write(index)

        # Write to post pages
        if properties.generate_post_pages:
            for (post, post_html) in zip(posts, post_htmls):
                post_filename = post.post_id + ".html"

                if hasattr(post, "title"):
                    page_title = f"{properties.display_title} · {post.title}"
                else:
                    page_title = properties.site_title

                post_file_content = post_template.replace("{page_title}", page_title)
                post_file_content = post_file_content.replace("{post}", post_html)

                if type(post) == ImagePost:
                    post_file_content = post_file_content.replace("{og_preview}", f"""
                        <meta property='og:image' content='../images/{post.image_filename}'>
                    """
                    )
                elif type(post) == VideoPost:
                    post_file_content = post_file_content.replace("{og_preview}", f"""
                        <meta property="og:type" content="video">
                        <meta property="og:video" content="../videos/{post.video_filename}">
                        <meta property="og:image" content="../thumbnails/{post.thumbnail_filename}">
                    """
                    )
                else:
                    post_file_content = post_file_content.replace("{og_preview}", "")

                with open(join(self.posts_dir, post_filename), "w") as post_file:
                    post_file.write(post_file_content)

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
    elif post_type == "video":
        caption = input("Caption: ")
        if len(caption) == 0:
            caption = None

        location = input("Location: ")
        if len(location) == 0:
            location = None

        content_manager.create_video_post(content_file_path, caption, location)
    else:
        fuck_off()

def delete(content_manager, argv):
    if len(argv) < 1:
        fuck_off()

    post_id = os.path.basename(argv[0])
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

def push(content_manager, argv):
    check_call(f"rsync -vh -r --exclude '.DS_Store' --delete -og --chown=webhost:www-data app/sites/{content_manager.host} webhost@{content_manager.host}:/home/webhost/Sites/app/sites", stderr = PIPE, shell = True)

def pull(content_manager, argv):
    check_call(f"rsync -vh -r --exclude '.DS_Store' --delete webhost@{content_manager.host}:/home/webhost/Sites/app/sites/{content_manager.host} app/sites", stderr = PIPE, shell = True)

def main(argv):
    if len(argv) < 2:
        fuck_off()

    host = argv[0]
    action = argv[1]

    app_dir = dirname(os.path.realpath(__file__))
    content_manager = ContentManager(app_dir = app_dir, host = host)

    if action == "create":
        create(content_manager, argv[2:])
    elif action == "delete":
        delete(content_manager, argv[2:])
    elif action == "generate":
        generate(content_manager, argv[2:])
    elif action == "push":
        push(content_manager, argv[2:])
    elif action == "pull":
        pull(content_manager, argv[2:])
    else:
        fuck_off()

def fuck_off():
    usage  = "Usage:\n"
    usage += "    python3 content_manager.py <host> create <text | image | video> <content_file_path>\n"
    usage += "    python3 content_manager.py <host> delete <post_id | post_url>\n"
    usage += "    python3 content_manager.py <host> generate\n"
    usage += "    python3 content_manager.py <host> push\n"
    usage += "    python3 content_manager.py <host> pull\n"

    print(usage)
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
