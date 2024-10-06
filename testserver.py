from flask import Flask, request, jsonify
import json
import base64
from io import BytesIO
import requests
from .detect import detect_banner
app = Flask(__name__)

@app.route("/detect", methods=['POST'])
def cookie_banner_detection():
    data = request.json
    print(data)
    try:
        # Decode the base64 data
        imgdata = base64.b64decode(data.get('image'))

        # Create a BytesIO object to store the decoded data
        image_data = BytesIO(imgdata)
        result = detect_banner(image_data)
    except Exception as e:
        print(f"Error decoding image: {e}")
        return jsonify({'success': False})
    return jsonify({'success': True, 'hasCookieBanner': result})