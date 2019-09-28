# Sites
A set of tools to manage photo stream sites.

In a few minutes you can have your own https site and the ability to post photos from anywhere. Here's [my site](https://christianbator.com) managed with these tools.

## Getting Started
Follow along with the instructions below, and your site should be up in no time.

### Prerequisites
* Python3 and ImageMagick installed locally
```
brew install python
brew install imagemagick
```
* A domain name (e.g. google.com), which we'll call `{host}`
    * I like [namecheap](https://www.namecheap.com)  
* An Ubuntu 18.04 server (with ssh access to root)
    * You can set one up through [DigitalOcean](https://www.digitalocean.com/docs/droplets/how-to/create/)  
* DNS configured to point the domain to the server
    * You can follow [these instructions](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars)  

Verify your domain points to your ip with:
```
nslookup {host}
```

### Setup
Setup your server with the following commands, substituting your domain for `{host}`:

**1. Clone the repo**
```
git clone git@github.com:christianbator/Sites.git
cd Sites
```

**2. Configure your local environment**
```
source scripts/setup_local.sh
```

* This will create a virtual environment in `app/.env` and install [Flask](https://www.fullstackpython.com/flask.html)
* **All `python` commands should be run with your virtual env activated** 
  * You can reactivate with `source app/.env/bin/activate` and exit with `deactivate`

**3. Configure your remote environment**  
Create a user named `webhost` with sudo privileges (so we don't run our server as `root`):
```
ssh root@{host} "bash -s" -- < scripts/setup_webhost.sh
```

Configure the server:
```
ssh webhost@{host}
git clone git@github.com:christianbator/Sites.git
cd Sites
source scripts/setup_server.sh
```

This will setup [nginx](https://www.nginx.com/resources/wiki/), [Let's Encrypt](https://letsencrypt.org), and your python environment. 

Everything will be run from the `webhost` user as part of the nginx default group, `www-data`.

**4. Create your site**
```
python app/site_manager.py create -s "{host}" -t "site title" -d "site description"
```

This will create the directory `app/.sites/{host}` that contains all your site's data. It will also generate a secret key in `app/.sites/secret.txt` that we'll use to sign tokens. To post to your site, you'll need to provide a valid token (more on that later).

You can always update your title and description in the `app/.sites/{host}/data/properties.json` file.

**5. Encrypt the traffic**
```
sudo certbot --nginx -d {host} -d www.{host}
```

Follow the certbot prompts to obtain a certificate. When asked, choose "no redirect" - it doesn't really matter though, we'll update the nginx config ourselves.

**6. Start it up**  
Update the nginx config in `/etc/nginx/nginx.conf` for every site defined in `app/.sites`:
```
sudo python app/site_manager.py update_nginx
```

Start nginx (to serve the static site) and a gunicorn daemon (to serve the flask app for image uploads):
```
./scripts/start_services.sh
```

You should see an empty site with your title and description at https://{host}

### Setup Notes
* The site is served as static content from nginx (out of the `/home/webhost/Sites/app/.sites/{host}` directory)
* Posts are stored in `app/.sites/data/posts.json`, and the html pages are generated by the `app/content_manager.py` script
* Posting new images is handled by a Flask app served by a Gunicorn daemon
    * Images should be uploaded as a common type (png, jpg, etc.)  
    * Images are then converted to progressive jpgs using [ImageMagick](https://imagemagick.org/index.php) and Google's recommended settings for image optimization
* All http traffic is redirected to https
* All `www.` urls are redirected to non-www, cause that's nicer
* All trailing slash urls are rewritten to non-trailing slash urls, cause that's nicer

## Usage
There are a few tools to help manage your site - you can even manage multiple sites, but they must be hosted on the same server.

### Syncing
You can sync your site content to and from your remote server with:
```
./scripts/pull.sh {host}
./scripts/push.sh {host}
```

This will just `rsync` the `app/.sites/{host}` directory to and from the remote server. Pulling is useful when you've posted an image directly to your remote server, and you want to pull down the latest version of your site to your local machine. Pushing is useful when you've posted an image on your local machine and want to update your your public site.

**Note:** this will overwrite the destination site!

You can also sync the secret key with:
```
./scripts/pull_secret.sh {host}
./scripts/push_secret.sh {host}
```

**Note:** for now, there is only one secret shared across all sites on the same server. This will overwrite the destination secret!

### Running Locally
To run the app locally in debug mode, use:
```
python app/app.py
```

This will run the app at `http://localhost:5000`, so you can post images locally.

You can open your site locally with:
```
open app/.sites/{host}/content/views/index.html
```

### Posting
To post locally in debug mode, use:
```
./scripts/post_local.sh {host} /path/to/image.jpg "caption"
```

To post to your server, first pull the secret if you don't have it in `app/.sites/secret.txt`:
```
./scripts/pull_secret.sh {host}
```

Then verify we can create a token from it:
```
pyjwt --key=$(cat app/.sites/secret.txt) encode sitename={host}
```

Then you can use the helper script to post images:
```
./scripts/post.sh {host} /path/to/image.jpg "caption"
```

Under the hood, it's just an http post request to `https://{host}.posts`, meaning you can use that token to post images from anywhere:
```
curl -i -H "Authorization: Bearer token" -F "image=@/path/to/image" -F "caption=caption" https://{host}/posts
```

### Icons
Fill in the `.sites/{host}/content/icons` directory with the following files so your site will automatically serve a favicon and apple touch icon:
```
icon.png (64x64)
apple-touch-icon.png (180x180)
```

Then push your site to your remote server:
```
./scripts/push.sh {host}
```

### Regenerating Site
If you ever edit the `app/.sites/{host}/data/posts.json` file - which is essentially a little database of posts - you can regenerate your site with:
```
python app/content_manager.py regenerate -s {host}
```

### Multiple Sites
Managing multiple sites on the same machine is pretty simple, since all of the scripts take a {host} argument.

**1. Create a new site on your server**
```
python app/site_manager.py create -s "{new_host}" -t "new site title" -d "new site description"
```

**2. Encrypt the traffic**
```
sudo certbot --nginx -d {new_host} -d www.{new_host}
```

**3. Update and restart nginx**
```
sudo python app/site_manager.py update_nginx
sudo systemctl restart nginx
```

## Posting from your phone
As mentioned above, posting a photo is just an http post request, so you can post from anywhere.

### iOS
I made an iOS shortcut that you can use to post from your iPhone:

* Enable shortcut sharing: Settings > Shortcuts > Allow Untrusted Shortcuts
* Download [the shortcut](https://www.icloud.com/shortcuts/2517d7a649e541289d09ba00c86c05f3)
* Get your sites and tokens with:
```
python scripts/ios_shortcut_input.py
```
* Paste the result into the shortcut configuration when prompted

You should be able to run the shortcut and select a photo to post (it will also appear as a share sheet option).

### Android
Buy a [real phone](https://www.apple.com/iphone/) ;)

Open to submissions!

## Caveats
The site design is simple and inflexible, but there are already plenty of tools for managing complex sites. I wanted to post photos to an https site from my laptop and phone, and I wanted to serve them as static content.

That said, feel free to fork the project and mess around with the `template` directory. There are css files in `template/content/styles`, and you should be able to create something you like. Restructuring the html requires code changes in `app/post.py`.

Happy site building!
