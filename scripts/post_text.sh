#!/bin/bash
set -euo pipefail

token=$(pyjwt --key=$(cat app/sites/$1/secret.txt) encode host=$1)
curl -i -H "Authorization: Bearer $token" -F "text=@$2" -F "location=$3" -F "date=$4" https://$1/post_text
