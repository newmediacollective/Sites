#!/bin/bash

server=$(head -n 1 config/server.txt)

echo "Tailing access logs from $server..."

ssh root@$server "tail -f /var/log/nginx/access.log" >> logs/access.log
