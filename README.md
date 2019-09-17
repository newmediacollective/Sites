# Website
A simple website manager to publish a list of posts

## Getting Started
Follow the instructions to get your website up and running

### Prerequisites
- Install python3 however you like :)
- Clone the repo:
```
git clone git@github.com:christianbator/Website.git
cd Website
```

### Local Config
- Run:
```
./scripts/configure-local.sh
```

This will:
- Ask you for your website info
- Prepare the local directory `~/.website` (in which everything is stored)

### Remote Config
- Run:
```
./scripts/configure-remote.sh
```

This will:
- Ask you for your remote host (e.g. `1.1.1.1` or `google.com`)
- Copy the default nginx config to `~/.website/config`
- Remotely:
  - Create a `/website` directory
  - Install nginx
  - Copy the nginx config from `~/.website/config` to `/etc/nginx`
    - A backup of the remote nginx config is stored in `/etc/nginx/nginx-conf-backup` if there is an existing config

### HTTPS (optional)
We can use letsencrypt and certbot for HTTPS support.

On your remote machine, run the following (when prompted, make sure to use the same remote host you entered above):
```
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository -y ppa:certbot/certbot
sudo apt-get update
sudo apt-get install -y certbot python-certbot-nginx
sudo certbot --nginx
```

This will update your nginx config - if you'd like to copy it back to your local machine, run:
```
./scripts/download-nginx-conf.sh
```

### Icons (optional)
If you fill the `~/.website/content/icons` directory with the following files, your website will automatically serve a favicon and apple touch icon:
```
icon.png (64x64)
apple-touch-icon.png (180x180)
```

## Usage
Use the following commands and helper scripts to update and monitor your website:

### Getting Help
```
python3 website.py help
```

### Posting
To create a new post, pass a path to an image along with an optional caption like so:
```
python3 website.py post -i ~/path/to/image.jpg -c "I just posted something"
```

This will:
- Create a unique ID for the image
- Copy it to the `~/.website/content/images` directory
- Create a new post in `~/.website/content/posts.json`

You can also provide an optional date with `-d` if you want to (it'll be passed through as a string so make sure it looks nice):
```
python3 website.py post -i ~/path/to/image.jpg -d "Apr 14 2020" -c "This didn't happen today"
```

### Publishing
To publish your changes:
```
python3 website.py publish
open ~/.website/content/views/index.html
```

This will:
- Read the posts out of `~/.website/content/posts.json`
- Fill in the templates from `/templates`
- Write the resulting HTML to `~/.website/content/views`.

To publish your changes remotely, execute the same command with the `-r` option:
```
python3 website.py publish -r
open http://$(cat ~/.website/config/server.txt)
```

This will:
- Publish locally
- Sync the `/views /styles /images /icons` directories in `~/.website/content` to your remote server's `/website` directory

### Monitoring
You can monitor the nginx access logs on your local machine with the following helper script:
```
./scripts/tail-access-logs.sh
open ~/.website/logs/access.log
```

This will:
- Tail the remote nginx access logs and write them to `~/.website/logs/access.log`

## Miscellaneous
The following are some miscellaneous helpers:

### Image optimization
If you have [ImageMagick](https://imagemagick.org/index.php) installed (`brew install imagemagick`), you can optimize your images for web with:
```
./scripts/optimize-images.sh
```

This uses ImageMagick to export all `*.jpg` images as progressive jpegs with Google's recommended settings.
