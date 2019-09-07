# Website
A simple website manager to publish a list of posts.

## Getting Started
Follow the instructions to get your website up and running.

### Prerequisites
- Install python3 however you like :)
- Clone the repo:
```
git clone git@github.com:christianbator/Website.git
cd Website
```

### Set up properties
- Open `properties.json` and edit the fields for your site info

### Set up your remote server
- Open `config/server.txt` and put your server's IP or domain on the first line (e.g. `1.1.1.1` or `google.com`)
- Prepare the remote server:
```
./scripts/prepare-server.sh
```

This will:
- Install nginx
- Create a `/website` directory
- Copy over the default nginx config
- Start nginx to serve your website

### Set up https (optional, but like so easy)
We can use letsencrypt and certbot for dead simple https support.

Update `config/nginx.conf` for your domain name:
```
server_name  your_domain_here.com;
```

Then run the server prep script again:
```
./scripts/prepare-server.sh
```

Finally, we'll let certbot do the rest (when prompted, make sure to use the same domain you entered for `server_name` above):
```
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot python-certbot-nginx
sudo certbot --nginx
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
- Copy it to the `/images` directory
- Create a new post in `posts.json`

You can also provide an optional date with `-d` if you want to (it'll be passed through as a string so make sure it looks nice):
```
python3 website.py post -i ~/path/to/image.jpg -d "Apr 14 2020" -c "This didn't happen today"
```

### Publishing
To publish your changes:
```
python3 website.py publish
open views/index.html
```

This will:
- Read the posts out of `posts.json`
- Fill in the templates from `/templates`
- Write the resulting HTML to `/views`.

To publish your changes remotely, execute the same command with the `-r` option:
```
python3 website.py publish -r
open http://$(cat config/server.txt)
```

This will:
- Publish locally
- Sync the `/views /styles /images /icons` directories to your remote server's `/website` directory

### Monitoring
You can monitor the nginx access logs on your local machine with the following helper script:
```
./scripts/tail-access-logs.sh
open logs/access.log
```

This will:
- Tail the remote nginx access logs and write them to `logs/access.log`
