#!/usr/bin/env python
import os
import uuid
import subprocess
import json
from flask import Flask, request, jsonify, abort
from PIL import Image
import io

app = Flask(__name__)

TEMP_IMAGE_DIR = "temp_images"

os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)

def is_jpeg(file_bytes):
    """Check if the file is a valid JPEG using Pillow."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        return image.format.lower() == "jpeg"
    except Exception as e:
        print(f"Error verifying image: {e}")
        return False

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_bytes = file.read()
    file.seek(0)
    
    if file.content_type != "image/jpeg":
        return jsonify({"error": "Only JPEG images are allowed (Content-Type must be image/jpeg)"}), 400

    if not is_jpeg(file_bytes):
        return jsonify({"error": "Uploaded file is not a valid JPEG image"}), 400

    temp_filename = f"{uuid.uuid4().hex}.jpg"
    temp_path = os.path.join(TEMP_IMAGE_DIR, temp_filename)

    file.save(temp_path)
    
    try:
        command = ["python", "Oceni.py", temp_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            error_message = result.stderr.strip() or "Unknown error while running Oceni.py"
            return jsonify({"error": f"Error running inference: {error_message}"}), 500

        output_json = json.loads(result.stdout)
    except Exception as e:
        return jsonify({"error": f"Exception occurred: {str(e)}"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return jsonify(output_json), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
