#!/bin/bash
set -euo pipefail

python3 -m venv app/.env
source app/.env/bin/activate
pip install wheel
pip install flask PyJWT
