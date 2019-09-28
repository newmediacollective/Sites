#!/bin/bash
set -euo pipefail

#
# Sites
#
sudo cp template/config/sites.service /etc/systemd/system/sites.service
sudo systemctl daemon-reload

sudo systemctl start sites
sudo systemctl enable sites

#
# Nginx
#
sudo systemctl restart nginx
sudo systemctl status nginx sites
