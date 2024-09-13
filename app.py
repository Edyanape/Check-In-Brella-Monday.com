from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    file = request.files['image']
    image_np = np.fromstring(file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    barcodes = decode(image)
    qr_data = None

    if barcodes:
        for barcode in barcodes:
            qr_data = barcode.data.decode("utf-8")
            break

    if qr_data:
        return jsonify({"status": "success", "qr_data": qr_data})
    else:
        return jsonify({"status": "fail", "message": "No QR code detected"})

if __name__ == "__main__":
    app.run(debug=True)

