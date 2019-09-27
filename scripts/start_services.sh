#!/bin/bash
set -euo pipefail

#
# Website
#
sudo cp ../template/config/website.service /etc/systemd/system/website.service

sudo systemctl start website
sudo systemctl enable website

#
# Nginx
#
sudo systemctl restart nginx
sudo systemctl status nginx website
