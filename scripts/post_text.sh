#!/bin/bash
set -euo pipefail

token=$(pyjwt --key=$(cat app/sites/$1/secret.txt) encode sitename=$1)
curl -i -H "Authorization: Bearer $token" -F "post_type=text" -F "content=@$2" -F "location=$3" https://$1/posts
