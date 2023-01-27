#!/bin/bash
set -euo pipefail

curl -i -H "Host: $1" -F "image=@$2" -F "caption=$3" -F "location=$4" -F "date=$5" http://localhost:5000/post_image
