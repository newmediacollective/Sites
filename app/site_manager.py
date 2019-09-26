#
# site_manager.py
#

import os
import sys
import json
import getopt
import shutil

from os.path import dirname, join, exists

#
# Constants
#
app_dir = dirname(os.path.realpath(__file__))
sites_dir = join(app_dir, ".sites")

#
# Methods
#
def create(sitename, title, description):
    site_dir = join(sites_dir, sitename)

    if exists(site_dir):
        print(f"Error: {sitename} already exists")
        sys.exit(2)

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
    os.makedirs(join(content_dir, "views"))

    content_template_dir = join(app_dir, "../template/content")
    shutil.copytree(join(content_template_dir, "styles"), join(content_dir, "styles"))

    shutil.copy(join(content_template_dir, "robots.txt"), content_dir)

    with open(join(content_template_dir, "sitemap.txt"), "r") as sitemap_template_file:
        sitemap = sitemap_template_file.read().replace("{host}", sitename)

        with open(join(content_dir, "sitemap.txt"), "w") as sitemap_file:
            sitemap_file.write(sitemap)

    #
    # Data
    #
    data_dir = join(site_dir, "data")
    os.makedirs(data_dir)

    with open(join(data_dir, "properties.json"), "w") as properties_file:
        properties = {
            "title": title,
            "description": description
        }

        json.dump(properties, properties_file, sort_keys = True, indent = 4)

    #
    # Config
    #
    config_dir = join(site_dir, "config")
    os.makedirs(config_dir)

    with open(join(app_dir, "../template/config/server.conf"), "r") as config_template_file:
        config = config_template_file.read().replace("{host}", sitename)

        with open(join(config_dir, "server.conf"), "w") as config_file:
            config_file.write(config)

def update_nginx():
    sitenames = [sitename for sitename in os.listdir(sites_dir) if os.path.isdir(join(sites_dir, sitename))]

    server_blocks = []
    for sitename in sitenames:
        print(f"> Configuring {sitename}")
        with open(join(sites_dir, f"{sitename}/config/server.conf"), "r") as server_block_file:
            server_block = server_block_file.read()
            server_blocks.append(server_block)

    with open(join(app_dir, "../template/config/nginx.conf"), "r") as nginx_conf_template_file:
        nginx_conf = nginx_conf_template_file.read().replace("# {server_blocks}", "\n".join(server_blocks))

        with open("/etc/nginx/nginx.conf", "w") as nginx_conf_file:
            nginx_conf_file.write(nginx_conf)

def main(argv):
    usage = "Usage:\n"
    usage += "> python3 site_manager.py create -s sitename -t title -d description"
    usage += "> python3 site_manager.py update_nginx"

    if len(argv) == 0:
        print(usage)
        sys.exit(2)

    action_name = argv[0]
    sitename = None
    title = None
    description = None

    try:
        opts, args = getopt.getopt(argv[1:],"s:t:d:")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-s":
            sitename = arg
        elif opt == "-t":
            title = arg
        elif opt == "-d":
            description = arg
        else:
            print(f"Error: unrecognized option\n{usage}")
            sys.exit(2)

    if action_name == "help":
        print(usage)
        sys.exit()
    elif action_name == "create":
        create(sitename = sitename, title = title, description = description)
    elif action_name == "update_nginx":
        update_nginx()
    else:
        print(f"Error: unrecognized action\n{usage}")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
