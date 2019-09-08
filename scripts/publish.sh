#!/bin/sh

#
# publish.sh
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$script_dir/locations.sh"

server=$(head -n 1 $server_file)

echo "\n---"
echo "Publishing to $server..."

rsync -vh -r $view_dir $style_dir $image_dir $icon_dir root@$server:$remote_website_dir