# website
A simple website manager for posting images

## Getting Started
Follow the instructions to get your website up and running

### Prerequisites
- Python3 installed locally
- A domain names (e.g. google.com)
- Proper DNS configuration pointing the domain name to an Ubuntu 18.04 server
- Root ssh access to that server

### Setup
Setup your server with the following commands, substituting your domain name for `{host}` (e.g. google.com):
```
# Clone the repo
git clone git@github.com:christianbator/website.git
cd website

# Local setup
source scripts/setup_local.sh

# Create a webhost user with sudo privileges
ssh root@{host} "bash -s" -- < scripts/setup_webhost.sh

# Configure the server
ssh webhost@{host}
git clone git@github.com:christianbator/website.git
cd website
source scripts/setup_server.sh

# Create a website
python app/site_manager.py create -s "{host}" -t "title" -d "description"

# Encrypt the traffic to it
sudo certbot --nginx -d {host} -d www.{host}

# Start it up!
sudo python app/site_manager.py update_nginx
./scripts/start_services.sh
```

You should see an empty site with your title and description at https://{host}

## Usage
There's a toolbox of commands to manage your website. You can manage multiple sites, but they must be hosted on the same server.

### Background
For each website, content is stored in `app/.sites/{host}`.

### Syncing
You can sync your website content to & from the remote server with:
```
# Pull website down
./scripts/pull.sh {host}

# Push website up
./scripts/push.sh {host}
```

You can also sync the secret key used to sign tokens with:
```
# Pull secret down
./scripts/pull_secret.sh {host}

# Push secret up
./scripts/push_secret.sh {host}
```

For now, there is only one secret shared across all websites on the same server.

**Note:** this will overwrite the destination secret!

### Running Locally
To run the app locally, simply:
```
python app/app.py
```

### Posting
To post locally in debug mode, use:
```
./scripts/post_local.sh {host} /path/to/image.jpg "caption"
```

To post to your server, first pull the secret as mentioned above:
```
./scripts/pull_secret.sh {host}

# Verify we can create a token
pyjwt --key=$(cat app/.sites/secret.txt) encode sitename={host}
```

Then you can use the helper script to post images:
```
./scripts/post.sh {host} /path/to/image.jpg "caption"
```

Under the hood, it's just a simple http post request (meaning you can use that token to post images from anywhere):
```
curl -i -H "Authorization: Bearer {token}" -F "image=@{/path/to/image}" -F "caption={caption}" https://{host}/posts
```

### Icons
Fill in the `.sites/{host}/content/icons` directory with the following files, so your website will automatically serve a favicon and apple touch icon:
```
icon.png (64x64)
apple-touch-icon.png (180x180)
```

### Multiple Websites
Managing multiple websites on the same machine is pretty simple:
```
#
# Logged into webhost@{host}, in ~/website
#

# Create a new website
python app/site_manager.py create -s "{new_host}" -t "title" -d "description"

# Encrypt the traffic to it
sudo certbot --nginx -d {new_host} -d www.{new_host}

# Update and restart nginx
sudo python app/site_manager.py update_nginx
sudo systemctl restart nginx
```

Then you can sync the website down to your local machine as mentioned above.
