#
# website.py
#

import os
import sys
import getopt
import uuid
import json
import shutil

from os import listdir
from os.path import join
from datetime import datetime
from subprocess import Popen, PIPE

def log(message):
    print(f"\n---\n{message}")

def source(script):
    pipe = Popen(f"set -a; . {script}; set +a; env", stdout = PIPE, shell = True)
    output = pipe.communicate()[0]

    lines = map(lambda line: line.decode("utf-8"), output.splitlines())
    env = dict((line.split("=", 1) for line in lines))

    return env

env = source("scripts/locations.sh")

template_dir = env["template_dir"]
view_dir = env["view_dir"]
image_dir = env["image_dir"]

properties_filename = env["properties_file"]
posts_filename = env["posts_file"]
index_filename = "index.html"

class Post:
    def __init__(self, image, caption, date):
        self.image = image
        self.caption = caption
        self.date = date

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys = True, indent = 4)

    def to_json(self):
        return {
            "image": self.image,
            "caption": self.caption,
            "date": self.date
        }

    @staticmethod
    def from_json(json):
        return Post(
            image = json["image"],
            caption = json["caption"],
            date = json["date"]
        )

    def to_html(self):
        if not self.caption:
            return f"""
    <div class="post">
        <a href="../images/{self.image}">
            <img src="../images/{self.image}" alt="">
        </a>
        <p class="date">{self.date}</p>
    </div>"""
        else:
            return f"""
    <div class="post">
        <a href="../images/{self.image}">
            <img src="../images/{self.image}" alt="">
        </a>
        <p class="caption">{self.caption}</p>
        <p class="date">{self.date}</p>
    </div>"""

class PostAction:
    def __init__(self, image_path, date, caption):
        image_file_extension = os.path.splitext(image_path)[1]
        image = str(uuid.uuid4()) + image_file_extension

        if not date:
            date = datetime.now().strftime("(%b %-d %Y)")

        self.image_path = image_path
        self.post = Post(image = image, caption = caption, date = date)

    def execute(self):
        shutil.copy(self.image_path, join(image_dir, self.post.image))

        posts = get_posts()
        posts.insert(0, self.post)

        post_json = [post.to_json() for post in posts]

        with open(posts_filename, "w") as posts_file:
            json.dump(post_json, posts_file, sort_keys = True, indent = 4)

        log(f"Successfully created post: \n{self.post}")


class PublishAction:
    def __init__(self, remote):
        self.remote = remote

    def execute(self):
        log("Publishing locally...")

        properties = get_properties()
        template_names = [filename for filename in listdir(template_dir)]

        for template_name in template_names:
            print(template_name)

            with open(join(template_dir, template_name), "r") as template_file:
                template = template_file.read()

            view = template
            for key, value in properties.items():
                view = view.replace(f"{{{key}}}", value)

            with open(join(view_dir, template_name), "w") as view_file:
                view_file.write(view)

        with open(join(view_dir, index_filename), "r") as index_file:
            index = index_file.read()

        posts = get_posts()
        post_html = "\n".join([post.to_html() for post in posts])
        index = index.replace("{posts}", post_html)

        with open(join(view_dir, index_filename), "w") as index_file:
            index_file.write(index)

        if self.remote:
            os.system(f"./scripts/publish.sh")


def get_properties():
    properties = {}

    with open(properties_filename, "r") as properties_file:
        properties = json.load(properties_file)

    return properties


def get_posts():
    posts = []

    with open(posts_filename, "r") as posts_file:
        posts = [Post.from_json(json = post_json) for post_json in json.load(posts_file)]

    return posts


def parse_args(argv):
    usage = "Usage: python3 website.py (post -i image_path -d? date -c? caption | publish -r?)"

    if len(argv) == 0:
        log(usage)
        sys.exit(2)

    action_name = argv[0]
    image_path = None
    date = ""
    caption = ""
    remote = False

    try:
        opts, args = getopt.getopt(argv[1:],"i:d:c:r")
    except getopt.GetoptError:
        log(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-r":
            remote = True
        elif opt == "-i":
            image_path = arg
        elif opt == "-d":
            date = f"({arg})"
        elif opt == "-c":
            caption = arg

    if action_name == "help":
        log(usage)
        sys.exit()
    elif action_name == "post":
        if not image_path:
            log(f"Error: missing image file path\n{usage}")
            sys.exit(2)

        action = PostAction(image_path = image_path, date = date, caption = caption)
    elif action_name == "publish":
        action = PublishAction(remote = remote)
    else:
        log(f"Error: unrecognized action\n{usage}")
        sys.exit(2)

    return action


def main(argv):
    action = parse_args(argv)
    action.execute()


if __name__ == "__main__":
   main(sys.argv[1:])
