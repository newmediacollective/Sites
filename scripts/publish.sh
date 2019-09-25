#!/bin/bash

#
# publish.sh
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$script_dir/locations.sh"

server=$(head -n 1 $server_file)

printf "\n---\n"
echo "Publishing to $server..."

rsync -vh -r --no-perms --no-owner --no-group --delete $view_dir $style_dir $image_dir $icon_dir $robots_file $sitemap_file root@$server:$remote_website_dir

result=$(ssh root@$server 'chown -R www-data /website')
echo "$result"
