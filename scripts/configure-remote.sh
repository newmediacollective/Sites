#!/bin/sh

#
# configure-server.sh
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$script_dir/locations.sh"

# Create config
if [ ! -f $server_file ]; then
    read -p "What domain or ip will the website be hosted on? " host
    echo $host > $server_file
fi

# Copy config
server=$(head -n 1 $server_file)

if [ ! -f $nginx_config_file ]; then
    sed "s/localhost/$server/g" config/nginx.conf > $nginx_config_file
fi

echo "\n---"
echo "Website host configured as: $server"
echo "open $config_dir to update"


# Configure remote
echo "\n---"
echo "Configuring $server..."

result=$(ssh root@$server '
apt-get update
apt-get install nginx
mkdir -p /website
chown -R www-data /website
')

echo "$result"

rsync -vh -b --backup-dir=nginx-conf-backup $nginx_config_file root@$server:$remote_nginx_config_file
ssh root@$server systemctl restart nginx
