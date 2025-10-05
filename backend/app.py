from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import os

app = Flask(__name__)
CORS(app)

# تحميل الموديل YOLOv8
model = YOLO("yolov8n.pt")

# Route للصفحة الرئيسية
@app.route('/')
def serve_frontend():
    # ارجع رسالة تأكيد أن الخادم شغال
    return jsonify({
        "message": "AI Vision Assistant Server is running!",
        "status": "active",
        "endpoints": {
            "detect": "POST /detect"
        }
    })

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    img_bytes = file.read()
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # detect
    results = model.predict(img)

    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "box": box.xyxy[0].tolist()
            })

    return jsonify(detections)

if __name__ == "__main__":
    app.run(debug=True, port=5000)