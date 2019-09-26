#!/bin/bash
set -euo pipefail

curl -i -X POST -H "Sitename: $1" -F "image=@$2" -F "caption=$3" http://localhost:5000/posts
