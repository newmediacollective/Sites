#!/bin/bash
set -euo pipefail

token=$(pyjwt --key=$(cat app/.sites/secret.txt) encode sitename=$1)
curl -i -X POST -H "Authorization: Bearer $token" -F "image=@$2" -F "caption=$3" http://localhost:5000/posts

# curl -i -X POST -H "Sitename: $1" -F "image=@$2" -F "caption=$3" http://localhost:5000/posts
