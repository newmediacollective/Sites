#!/bin/bash
set -euo pipefail

#
# Python
#
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-setuptools python3-venv build-essential libssl-dev libffi-dev

python3 -m venv app/.env
source app/.env/bin/activate
pip install wheel gunicorn flask
deactivate

#
# ImageMagick
#
sudo apt-get install -y imagemagick

#
# Nginx
#
sudo usermod -aG www-data webhost

sudo apt-get install -y nginx
sudo rm -r /etc/nginx/sites-available /etc/nginx/sites-enabled /etc/nginx/modules-available /etc/nginx/modules-enabled

sudo ufw allow "Nginx HTTP"
sudo ufw allow "Nginx HTTPS"
sudo ufw allow "Nginx Full"

#
# LetsEncrypt
#
sudo add-apt-repository -y universe ppa:certbot/certbot
sudo apt-get update
sudo apt-get install -y software-properties-common certbot
sudo certbot

#
# Gunicorn
#
sudo cp ../template/config/website.service /etc/systemd/system/website.service
sudo systemctl start website
sudo systemctl enable website
sudo systemctl status website
