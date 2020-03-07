#!/bin/bash
set -euo pipefail

curl -i -H "Sitename: $1" -F "post_type=image" -F "content=@$2" -F "caption=$3" -F "location=$4" http://localhost:5000/posts
