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

## Usage
Use the following commands and helper scripts to update and monitor your website:

### Getting Help
```
python3 website.py help
```

### Posting
To create a new post, pass a path to an image along with an optional caption like so:
```
python3 website.py post -i ~/path/to/image.jpg -c Check out my awesome image!
```

This will:
- Create a unique ID for the image
- Copy it to the `/images` directory
- Create a new post in `posts.json`

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
