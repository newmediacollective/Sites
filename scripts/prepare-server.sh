#!/bin/bash

server=$(head -n 1 config/server.txt)

echo "Preparing $server..."

result=$(ssh root@$server '
apt-get update
apt-get install nginx
mkdir -p /website
chown -R www-data /website
')
echo "$result"

scp config/nginx.conf root@$server:/etc/nginx/nginx.conf
ssh root@$server systemctl restart nginx
