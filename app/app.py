#
# app.py
#

import os
import jwt
import json

from content_manager import ContentManager
from os.path import join
from uuid import uuid4
from flask import Flask, request, Response
from post import Post

app = Flask(__name__)

#
# Constants
#

tmp_dir = join(app.root_path, ".tmp")
secret_path = join(app.root_path, ".sites/secret.txt")

with open(secret_path, "r") as secret_file:
    secret = secret_file.read().strip()

#
# Routes
#

@app.route("/posts", methods=["POST"])
def handle_post():
    unauthorized_response = Response(json.dumps({ "error": "unauthorized" }), status = 401, mimetype = "application/json")
    invalid_request_response = Response(json.dumps({ "error": "invalid request" }), status = 400, mimetype = "application/json")

    if app.debug:
        sitename = request.headers.get("Sitename")

        if not sitename:
            return invalid_request_response
    else:
        bearer = request.headers.get("Authorization")

        if not bearer:
            return unauthorized_response

        try:
            token = bearer.split()[-1]
            payload = jwt.decode(token, secret, algorithms=["HS256"])
        except:
            return unauthorized_response

        sitename = payload.get("sitename")

        if sitename != request.host:
            return unauthorized_response

    if not request.form or not request.files:
        return invalid_request_response

    caption = request.form.get("caption")
    image = request.files.get("image")

    if not caption or not image:
        return invalid_request_response

    # Save image to temporary file
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_image_path = join(tmp_dir, image.filename)
    image.save(tmp_image_path)

    # Create post
    content_manager = ContentManager(app_dir = app.root_path, sitename = sitename)
    post = content_manager.create_post(image_path = tmp_image_path, caption = caption)

    # Clean up temporary file
    os.remove(tmp_image_path)

    # Respond
    return Response(json.dumps(post.to_json()), status = 201, mimetype = "application/json")

#
# Main
#

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
