#
# site_manager.py
#

import os
import jwt
import json

from os.path import dirname, join, realpath, isdir

#
# Constants
#
scripts_dir = dirname(realpath(__file__))
sites_dir = join(scripts_dir, "../app/sites")
secret_path = join(sites_dir, "secret.txt")

with open(secret_path, "r") as secret_file:
    secret = secret_file.read().strip()

sitenames = [sitename for sitename in os.listdir(sites_dir) if isdir(join(sites_dir, sitename))]

shortcut_input = {}
for sitename in sitenames:
    token = jwt.encode({"sitename": sitename}, secret, algorithm = "HS256").decode("utf-8")
    shortcut_input[sitename] = token

print(json.dumps(shortcut_input, sort_keys = True, indent = 4))
