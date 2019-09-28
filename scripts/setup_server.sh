#!/bin/bash
set -euo pipefail

#
# Update
#
sudo apt-get update

#
# Nginx
#
sudo usermod -aG www-data webhost

sudo apt-get install -y nginx
sudo rm -rf /etc/nginx/sites-available /etc/nginx/sites-enabled /etc/nginx/modules-available /etc/nginx/modules-enabled

sudo ufw allow "Nginx HTTP"
sudo ufw allow "Nginx HTTPS"
sudo ufw allow "Nginx Full"

#
# LetsEncrypt
#
sudo add-apt-repository -y universe
sudo add-apt-repository -y ppa:certbot/certbot
sudo apt-get update
sudo apt-get install -y software-properties-common certbot python-certbot-nginx

#
# ImageMagick
#
sudo apt-get install -y imagemagick

#
# Python
#
sudo apt-get install -y python3-pip python3-dev python3-setuptools python3-venv build-essential libssl-dev libffi-dev

rm -rf app/.env
python3 -m venv app/.env
source app/.env/bin/activate
pip install wheel
pip install flask PyJWT gunicorn gevent
