#
# app.py
#

import os
import jwt
import json

from content_manager import ContentManager
from os.path import join
from uuid import uuid4
from flask import Flask, request, abort
from post import Post

app = Flask(__name__)

#
# Constants
#

sites_dir = join(app.root_path, "sites")
tmp_dir = join(app.root_path, ".tmp")

#
# Routes
#

@app.errorhandler(400)
def handle_400(error):
    return ({ "error": "invalid request" }, 400)

@app.errorhandler(401)
def handle_401(error):
    return ({ "error": "unauthorized" }, 401)

@app.errorhandler(500)
def handle_500(error):
    return ({ "error": "internal server error" }, 500)

@app.route("/post_image", methods=["POST"])
def handle_post_image():
    # Authenticate
    (sitename, authenticate_error) = authenticate_post_request(request)
    if authenticate_error is not None:
        abort(authenticate_error)

    # Get the request parameters
    if not request.form or not request.files:
        abort(400)

    image = request.files.get("image")
    if not image:
        abort(400)

    caption = request.form.get("caption")
    if not caption:
        abort(400)

    if len(caption) == 0:
        caption = None

    location = request.form.get("location")
    if not location:
        abort(400)

    if len(location) == 0:
        location = None

    # Save image to temporary file
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_image_path = join(tmp_dir, image.filename)
    image.save(tmp_image_path)

    # Create post
    try:
        content_manager = ContentManager(app_dir = app.root_path, sitename = sitename)
        post = content_manager.create_image_post(image_path = tmp_image_path, caption = caption, location = location)
    except Exception as error:
        print(error)
        abort(500)

    # Clean up temporary file
    os.remove(tmp_image_path)

    # Respond
    return (post.to_json(), 201)

@app.route("/post_text", methods=["POST"])
def handle_post_text():
    # Authenticate
    (sitename, authenticate_error) = authenticate_post_request(request)
    if authenticate_error is not None:
        abort(authenticate_error)

    # Get the request parameters
    if not request.form or not request.files:
        abort(400)

    text = request.files.get("text")
    if not text:
        abort(400)

    location = request.form.get("location")
    if not location:
        abort(400)

    if len(location) == 0:
        location = None

    # Save text to temporary file
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_text_path = join(tmp_dir, text.filename)
    text.save(tmp_text_path)

    # Create post
    try:
        content_manager = ContentManager(app_dir = app.root_path, sitename = sitename)
        post = content_manager.create_text_post(text_file_path = tmp_text_path, location = location)
    except Exception as error:
        print(error)
        abort(500)

    # Clean up temporary file
    os.remove(tmp_text_path)

    # Respond
    return (post.to_json(), 201)

#
# Authentication
#

def authenticate_post_request(request):
    if app.debug:
        sitename = request.headers.get("Sitename")
        if not sitename:
            return (None, 400)
    else:
        bearer = request.headers.get("Authorization")
        if not bearer:
            return (None, 401)

        host = request.host

        site_dir = join(sites_dir, host)
        secret_path = join(site_dir, "secret.txt")

        with open(secret_path, "r") as secret_file:
            secret = secret_file.read().strip()

        if not secret:
            return (None, 500)

        try:
            token = bearer.split()[-1]
            payload = jwt.decode(token, secret, algorithms=["HS256"])
        except:
            return (None, 401)

        sitename = payload.get("sitename")
        if sitename != host:
            return (None, 401)

    return (sitename, None)
#
# Main
#

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
