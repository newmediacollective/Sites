#!/bin/bash
set -euo pipefail

rsync -vh -r --exclude ".DS_Store" --delete -og --chown=webhost:www-data app/.sites/$1 webhost@$1:/home/webhost/website/app/.sites
