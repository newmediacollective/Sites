#!/bin/bash
set -euo pipefail

rm -rf app/.env
python3 -m venv app/.env
source app/.env/bin/activate

pip install -r requirements.txt
