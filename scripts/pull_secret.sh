#!/bin/bash
set -euo pipefail

rsync -vh webhost@$1:/home/webhost/sites/app/sites/$1/secret.txt app/sites/$1/secret.txt
