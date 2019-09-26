# Website
A simple website manager to publish a list of posts

## Getting Started
Follow the instructions to get your website up and running

### Prerequisites
- An Ubuntu 18.04 server you can ssh into

### Config
```
ssh root@host "bash -s" -- < /path/to/setup_webhost.sh
ssh webhost@host
git clone git@github.com:christianbator/website.git
cd website
source scripts/setup_server.sh
cd app
python3 site_manager.py create -s "sitename" -t "title" -d "description"
python3 site_manager.py update_nginx
sudo systemctl restart nginx
```

### Usage
```
./scripts/post.sh {host} /path/to/image.jpg "caption"
```

### Icons (optional)
If you fill the `.sites/{host}/content/icons` directory with the following files, your website will automatically serve a favicon and apple touch icon:
```
icon.png (64x64)
apple-touch-icon.png (180x180)
```
