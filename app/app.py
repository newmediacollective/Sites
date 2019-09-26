#
# app.py
#

import os
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

#
# Routes
#

@app.route("/posts", methods=["POST"])
def handle_post():
    error_response = Response(json.dumps({ "error": "invalid request" }), status = 400, mimetype = "application/json")

    raw_host = request.host
    if raw_host.startswith("www."):
        raw_host = raw_host.replace("www.", "")

    raw_host = "christianbator.com"

    if not request.form or not request.files:
        return error_response

    caption = request.form.get("caption")
    image = request.files.get("image")

    if not caption or not image:
        return error_response

    # Save image to temporary file
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_image_path = join(tmp_dir, image.filename)
    image.save(tmp_image_path)

    # Create post
    content_manager = ContentManager(app_dir = app.root_path, sitename = raw_host)
    post = content_manager.create_post(image_path = tmp_image_path, caption = caption)

    # Clean up temporary file
    os.remove(tmp_image_path)

    # Respond
    return Response(json.dumps(post.to_json()), status = 201, mimetype = "application/json")

#
# Main
#

if __name__ == "__main__":
    app.run(host="0.0.0.0")
