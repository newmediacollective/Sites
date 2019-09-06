#!/bin/bash

server=$(head -n 1 config/server.txt)

mkdir -p logs
touch logs/access.log

echo "Tailing access logs from $server..."

ssh root@$server "tail -f /var/log/nginx/access.log" >> logs/access.log
