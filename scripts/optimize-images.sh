#!/bin/sh

#
# optimize.sh
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$script_dir/locations.sh"

mogrify -verbose -strip -sampling-factor 4:2:0  -quality 85 -interlace JPEG -colorspace RGB $image_dir/*.jpg
