#!/bin/bash
set -euo pipefail

token=$(pyjwt --key=$(cat app/sites/$1/secret.txt) encode host=$1)
curl -i -H "Authorization: Bearer $token" -F "image=@$2" -F "caption=$3" -F "location=$4" -F "date=$5" https://$1/post_image
