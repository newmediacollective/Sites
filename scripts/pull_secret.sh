#!/bin/bash
set -euo pipefail

rsync -vh webhost@$1:/home/webhost/sites/app/.sites/secret.txt app/.sites/secret.txt
