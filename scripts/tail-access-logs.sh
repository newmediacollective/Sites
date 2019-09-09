#!/bin/sh

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$script_dir/locations.sh"

server=$(head -n 1 $server_file)

echo "\n---"
echo "Tailing access logs from $server... (open $access_log_file to view)"

touch $access_log_file
ssh root@$server "tail -n0 -f $remote_access_log_file" >> $access_log_file
