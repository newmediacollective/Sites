#!/bin/sh

#
# configure-local.sh
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$script_dir/locations.sh"

echo "\n---"
read -p "What's the title of the website? " title

echo "\n---"
read -p "What's the website's description? " description

properties=$(cat content/properties.json)
properties="${properties/\{title\}/$title}"
properties="${properties/\{description\}/$description}"
echo $properties > $properties_file

if [ ! -f $posts_file ]; then
    cp content/posts.json $posts_file
fi

if [ ! -f $robots_file ]; then
    cp content/robots.txt $robots_file
fi

if [ ! -f $main_style_file ]; then
    cp content/styles/main.css $main_style_file
fi

if [ ! -f $error_style_file ]; then
    cp content/styles/error.css $error_style_file
fi

echo "\n---"
echo "Website \"$title\" configured in $website_dir"
