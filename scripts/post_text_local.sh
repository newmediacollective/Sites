#!/bin/bash
set -euo pipefail

curl -i -H "Sitename: $1" -F "post_type=text" -F "content=@$2" -F "location=$3" http://localhost:5000/posts
