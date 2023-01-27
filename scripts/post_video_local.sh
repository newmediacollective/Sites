#!/bin/bash
set -euo pipefail

curl -i -H "Host: $1" -F "video=@$2" -F "caption=$3" -F "location=$4" -F "date=$5" http://localhost:5000/post_video
