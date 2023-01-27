#!/bin/bash
set -euo pipefail

curl -i -H "Host: $1" -F "post_id=$2" http://localhost:5000/delete_post
