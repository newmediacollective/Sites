#!/bin/bash
set -euo pipefail

rsync -vh webhost@$1:/home/webhost/Sites/app/.sites/secret.txt app/.sites/secret.txt
