#
# site_manager.py
#

import os
import sys
import json
import getopt
import shutil

from subprocess import check_call, PIPE
from os.path import dirname, join, exists

from properties import *

#
# Constants
#
app_dir = dirname(os.path.realpath(__file__))
sites_dir = join(app_dir, "sites")

#
# Methods
#
def create(host, title):
    if not exists(sites_dir):
        os.makedirs(sites_dir)

    site_dir = join(sites_dir, host)

    if exists(site_dir):
        print(f"Error: {host} already exists")
        sys.exit(2)
    else:
        os.mkdir(site_dir)

    #
    # Secret
    #
    secret_path = join(site_dir, "secret.txt")

    try:
        check_call(f"openssl rand -base64 32 > {secret_path}", stderr = PIPE, shell = True)
    except Exception as error:
        sys.exit(error)

    #
    # Templates
    #
    shutil.copytree(join(app_dir, "../template/templates"), join(site_dir, "templates"))

    #
    # Content
    #
    content_dir = join(site_dir, "content")

    os.makedirs(join(content_dir, "icons"))
    os.makedirs(join(content_dir, "images"))
    os.makedirs(join(content_dir, "videos"))
    os.makedirs(join(content_dir, "thumbnails"))
    os.makedirs(join(content_dir, "posts"))
    os.makedirs(join(content_dir, "views"))

    content_template_dir = join(app_dir, "../template/content")
    shutil.copytree(join(content_template_dir, "styles"), join(content_dir, "styles"))

    shutil.copy(join(content_template_dir, "robots.txt"), content_dir)

    with open(join(content_template_dir, "sitemap.txt"), "r") as sitemap_template_file:
        sitemap = sitemap_template_file.read().replace("{host}", host)

        with open(join(content_dir, "sitemap.txt"), "w") as sitemap_file:
            sitemap_file.write(sitemap)

    #
    # Data
    #
    data_dir = join(site_dir, "data")
    os.makedirs(data_dir)

    properties = Properties.default(title = title)

    with open(join(data_dir, "properties.json"), "w") as properties_file:
        properties_file.write(str(properties))

    os.makedirs(join(data_dir, "text_posts"))

def update_nginx():
    with open(join(app_dir, "../template/config/server.conf"), "r") as server_block_template_file:
        server_block_template = server_block_template_file.read()

    hosts = [host for host in os.listdir(sites_dir) if os.path.isdir(join(sites_dir, host))]

    server_blocks = []
    for host in hosts:
        print(f"> Configuring {host}")
        server_block = server_block_template.replace("{host}", host)
        server_blocks.append(server_block)

    with open(join(app_dir, "../template/config/nginx.conf"), "r") as nginx_conf_template_file:
        nginx_conf = nginx_conf_template_file.read().replace("# {server_blocks}", "\n".join(server_blocks))

        with open("/etc/nginx/nginx.conf", "w") as nginx_conf_file:
            nginx_conf_file.write(nginx_conf)

def main(argv):
    usage = "Usage:\n"
    usage += "    python3 site_manager.py create -s <host> -t title"
    usage += "    python3 site_manager.py update_nginx"

    if len(argv) == 0:
        print(usage)
        sys.exit(2)

    action_name = argv[0]

    host = None
    title = None

    try:
        opts, args = getopt.getopt(argv[1:],"s:t:d:f:")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-s":
            host = arg
        elif opt == "-t":
            title = arg
        else:
            print(f"Error: unrecognized option\n{usage}")
            sys.exit(2)

    if action_name == "help":
        print(usage)
        sys.exit()
    elif action_name == "create":
        create(host = host, title = title)
    elif action_name == "update_nginx":
        update_nginx()
    else:
        print(f"Error: unrecognized action\n{usage}")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
