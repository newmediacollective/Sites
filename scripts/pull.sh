#!/bin/bash
set -euo pipefail

rsync -vh -r --exclude ".DS_Store" --delete webhost@$1:/home/webhost/Sites/app/.sites/$1 app/.sites
