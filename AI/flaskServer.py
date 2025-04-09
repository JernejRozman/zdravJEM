# server.py
from flask import Flask, request, jsonify
import predict  # Predict.py mora biti v istem folderju kot flaskServer.py

app = Flask(__name__)

@app.route('/imageRating', methods=['POST'])
def image_rating():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if image_file and image_file.mimetype == 'image/jpeg':
        try:
            image_bytes = image_file.read()
            result = predict.predict(image_bytes)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File must be a JPEG image"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
