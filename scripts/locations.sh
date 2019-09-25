#!/bin/bash

#
# locations.sh
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Local Root
website_dir=~/.website
mkdir -p $website_dir

# Remote Root
remote_website_dir=/website

# Local Config
config_dir="$website_dir/config"
mkdir -p $config_dir

server_file="$config_dir/server.txt"
nginx_config_file="$config_dir/nginx.conf"

# Remote Config
remote_nginx_config_file=/etc/nginx/nginx.conf

# Local Logs
log_dir="$website_dir/logs"
mkdir -p $log_dir

access_log_file="$log_dir/access.log"

# Remote Logs
remote_access_log_file=/var/log/nginx/access.log

# Local Content
content_dir="$website_dir/content"
mkdir -p $content_dir

view_dir="$content_dir/views"
mkdir -p $view_dir

style_dir="$content_dir/styles"
mkdir -p $style_dir

image_dir="$content_dir/images"
mkdir -p $image_dir

icon_dir="$content_dir/icons"
mkdir -p $icon_dir

posts_file="$content_dir/posts.json"
properties_file="$content_dir/properties.json"
main_style_file="$style_dir/main.css"
error_style_file="$style_dir/error.css"
robots_file="$content_dir/robots.txt"
sitemap_file="$content_dir/sitemap.txt"

# Input
template_dir="$script_dir/../templates"
