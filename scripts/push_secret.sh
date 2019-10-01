#!/bin/bash
set -euo pipefail

rsync -vh -og --chown=webhost:www-data app/sites/$1/secret.txt webhost@$1:/home/webhost/sites/app/sites/$1/secret.txt
