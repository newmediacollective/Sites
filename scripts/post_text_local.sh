#!/bin/bash
set -euo pipefail

curl -i -H "Host: $1" -F "text=@$2" -F "location=$3" http://localhost:5000/post_text
