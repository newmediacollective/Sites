#!/bin/bash
set -euo pipefail

token=$(pyjwt --key=$(cat app/sites/$1/secret.txt) encode host=$1)
curl -i -H "Authorization: Bearer $token" -F "post_id=$2" https://$1/delete_post
