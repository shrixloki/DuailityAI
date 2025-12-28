from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from io import BytesIO
from PIL import Image
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "DualityAI API is running"})

@app.route('/api/detect', methods=['POST'])
def detect_objects():
    try:
        # Get the uploaded image
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Basic image validation
        try:
            img = Image.open(image_file)
            width, height = img.size
        except Exception as e:
            return jsonify({"error": "Invalid image format"}), 400
        
        # Mock response for demonstration
        mock_response = {
            "detections": [
                {
                    "class": "cluttered_room",
                    "confidence": 0.85,
                    "bbox": [100, 100, 300, 200]
                },
                {
                    "class": "light_uncluttered", 
                    "confidence": 0.72,
                    "bbox": [150, 150, 250, 250]
                }
            ],
            "processing_time": 0.5,
            "image_size": [width, height],
            "model_version": "yolov8n-duality"
        }
        
        return jsonify(mock_response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    models = [
        {
            "name": "YOLOv8n-Duality",
            "description": "Lightweight model for room clutter detection",
            "accuracy": "85%",
            "speed": "Fast"
        },
        {
            "name": "YOLOv8s-Duality", 
            "description": "Balanced model for room clutter detection",
            "accuracy": "88%",
            "speed": "Medium"
        },
        {
            "name": "YOLOv8m-Duality",
            "description": "High accuracy model for room clutter detection", 
            "accuracy": "92%",
            "speed": "Slow"
        }
    ]
    return jsonify(models)

if __name__ == '__main__':
    app.run(debug=True)