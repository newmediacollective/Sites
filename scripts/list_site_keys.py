#
# list_site_keys.py
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

hosts = [host for host in os.listdir(sites_dir) if isdir(join(sites_dir, host))]

shortcut_input = {}
for host in hosts:
    secret_path = join(sites_dir, f"{host}/secret.txt")
    with open(secret_path, "r") as secret_file:
        secret = secret_file.read().strip()

    token = jwt.encode({"host": host}, secret, algorithm = "HS256").decode("utf-8")
    shortcut_input[host] = token

print(json.dumps(shortcut_input, sort_keys = True, indent = 4))
