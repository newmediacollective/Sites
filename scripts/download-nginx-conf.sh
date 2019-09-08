#!/bin/sh

#
# download-nginx-conf.sh
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$script_dir/locations.sh"

server=$(head -n 1 $server_file)

rsync -vh root@$server:$remote_nginx_config_file $nginx_config_file
