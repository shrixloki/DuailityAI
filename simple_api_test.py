#!/usr/bin/env python3
"""
Simple API test without model loading to check basic functionality
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Simple API is working'
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Return model info without loading them"""
    models = [
        {
            'id': 'flagship',
            'name': 'FINAL_SELECTED_MODEL',
            'available': os.path.exists('models/weights/FINAL_SELECTED_MODEL.pt'),
            'description': 'Test model'
        }
    ]
    return jsonify({
        'success': True,
        'models': models
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Mock prediction endpoint"""
    return jsonify({
        'success': True,
        'message': 'Mock prediction - API is working',
        'detections': [],
        'detection_count': 0
    })

if __name__ == '__main__':
    print("🧪 Starting simple API test server...")
    app.run(debug=True, host='0.0.0.0', port=8000)