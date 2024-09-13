from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from utils.get_brella import GET_INVITE_LIST
from tools.cleaner import TRANSFORM_BRELLA_LIST

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    get = GET_INVITE_LIST()
    got = get.get_information_brella()
    transform = TRANSFORM_BRELLA_LIST(got)
    qr_list = transform.transform_brella_qr()
    file = request.files['image']
    image_np = np.fromstring(file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    barcodes = decode(image)
    qr_data = None
    output = "No QR code detected"
    status = "fail"

    if barcodes:
        for barcode in barcodes:
            qr_data = barcode.data.decode("utf-8")
            if qr_data in qr_list:
                output = "Valid Code"
                status = "success"
                break
            else:
                output = "Invalid Code"
                status = "fail"

    return jsonify({"status": status, "message": output, "qr_data": qr_data})

if __name__ == "__main__":
    app.run(debug=True)

