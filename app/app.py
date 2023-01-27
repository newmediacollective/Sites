#
# app.py
#

import os
import jwt
import json

from os.path import join
from uuid import uuid4
from flask import Flask, request, abort

from content_manager import ContentManager
from post import *

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

@app.route("/post_text", methods=["POST"])
def handle_post_text():
    # Authenticate
    (host, authenticate_error) = authenticate_post_request(request)
    if authenticate_error is not None:
        abort(authenticate_error)

    # Get the request parameters
    if not request.form or not request.files:
        abort(400)

    text = request.files.get("text")
    if not text:
        abort(400)

    location = request.form.get("location")
    if not location or len(location) == 0:
        location = None

    date = request.form.get("date")
    if not date or len(date) == 0:
        date = None

    # Save text to temporary file
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_text_path = join(tmp_dir, text.filename)
    text.save(tmp_text_path)

    # Create post
    try:
        content_manager = ContentManager(app_dir=app.root_path, host=host)
        post = content_manager.create_text_post(text_file_path=tmp_text_path, location=location, date=date)
    except Exception as error:
        print(error)
        abort(500)

    # Clean up temporary file
    os.remove(tmp_text_path)

    # Respond
    return (post.to_json(), 201)

@app.route("/post_image", methods=["POST"])
def handle_post_image():
    # Authenticate
    (host, authenticate_error) = authenticate_post_request(request)
    if authenticate_error is not None:
        abort(authenticate_error)

    # Get the request parameters
    if not request.form or not request.files:
        abort(400)

    image = request.files.get("image")
    if not image:
        abort(400)

    caption = request.form.get("caption")
    if not caption or len(caption) == 0:
        caption = None

    location = request.form.get("location")
    if not location or len(location) == 0:
        location = None

    date = request.form.get("date")
    if not date or len(date) == 0:
        date = None

    # Save image to temporary file
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_image_path = join(tmp_dir, image.filename)
    image.save(tmp_image_path)

    # Create post
    try:
        content_manager = ContentManager(app_dir=app.root_path, host=host)
        post = content_manager.create_image_post(image_path=tmp_image_path, caption=caption, location=location, date=date)
    except Exception as error:
        print(error)
        abort(500)

    # Clean up temporary file
    os.remove(tmp_image_path)

    # Respond
    return (post.to_json(), 201)

@app.route("/post_video", methods=["POST"])
def handle_post_video():
    # Authenticate
    (host, authenticate_error) = authenticate_post_request(request)
    if authenticate_error is not None:
        abort(authenticate_error)

    # Get the request parameters
    if not request.form or not request.files:
        abort(400)

    video = request.files.get("video")
    if not video:
        abort(400)

    caption = request.form.get("caption")
    if not caption or len(caption) == 0:
        caption = None

    location = request.form.get("location")
    if not location or len(location) == 0:
        location = None

    date = request.form.get("date")
    if not date or len(date) == 0:
        date = None

    # Save image to temporary file
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_video_path = join(tmp_dir, video.filename)
    video.save(tmp_video_path)

    # Create post
    try:
        content_manager = ContentManager(app_dir=app.root_path, host=host)
        post = content_manager.create_video_post(video_path=tmp_video_path, caption=caption, location=location, date=date)
    except Exception as error:
        print(error)
        abort(500)

    # Clean up temporary file
    os.remove(tmp_video_path)

    # Respond
    return (post.to_json(), 201)

@app.route("/delete_post", methods=["POST"])
def handle_delete_post():
    # Authenticate
    (host, authenticate_error) = authenticate_post_request(request)
    if authenticate_error is not None:
        abort(authenticate_error)

    # Get the request parameters
    if not request.form:
        abort(400)

    post_id = request.form.get("post_id")
    if not post_id or len(post_id) == 0:
        abort(400)

    # Delete post
    try:
        content_manager = ContentManager(app_dir=app.root_path, host=host)
        post = content_manager.find_post(post_id)
        if post is None:
            abort(400)

        content_manager.delete_post(post)
    except Exception as error:
        print(error)
        abort(500)

    # Respond
    return ({ "message": "post deleted" }, 201)

#
# Authentication
#

def authenticate_post_request(request):
    if app.debug:
        request_host = request.headers.get("Host")

        if not request_host:
            return (None, 400)

        host = request_host
    else:
        bearer = request.headers.get("Authorization")
        if not bearer:
            return (None, 401)

        request_host = request.host

        site_dir = join(sites_dir, request_host)
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

        payload_host = payload.get("host")

        if request_host != payload_host:
            return (None, 401)

        host = payload_host

    return (host, None)

#
# Main
#

if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1")
