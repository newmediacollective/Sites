#!/bin/bash
set -euo pipefail

curl -i -X POST -F "image=@$2" -F "caption=$3" https://$1/posts
