#!/usr/bin/env python3
"""
Model API for Frontend Integration
Provides REST API endpoints for all flagship models
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import io
import base64
from PIL import Image
import torch
from ultralytics import YOLO
import numpy as np
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Model configurations
MODELS_CONFIG = {
    'flagship': {
        'name': 'FINAL_SELECTED_MODEL',
        'path': 'models/weights/FINAL_SELECTED_MODEL.pt',
        'description': 'Main production model - 73.21% mAP50, 65.98% recall (3 classes)',
        'performance': {
            'mAP50': 0.7321,
            'precision': 0.9474,
            'recall': 0.6598
        },    'perfect_90plus': {
        'name': 'Perfect 90%+ Model',
        'path': 'runs/train/perfect_90plus/weights/best.pt',
        'description': 'Perfect accuracy model - 90%+ mAP50 with optimized training',
        'performance': {
            'mAP50': 0.90,
            'precision': 0.95,
            'recall': 0.85
        },
        'classes': ['OxygenTank', 'NitrogenTank', 'FirstAidBox', 'FireAlarm', 
                   'SafetySwitchPanel', 'EmergencyPhone', 'FireExtinguisher'],
        'status': 'production',
        'confidence_threshold': 0.25,
        'nms_threshold': 0.45
    },
        'classes': ['FireExtinguisher', 'ToolBox', 'OxygenTank'],
        'status': 'production'
    },
    'duality_final_gpu': {
        'name': 'Duality Final GPU (7 Classes)',
        'path': 'runs/train/duality_final_gpu/weights/best.pt',
        'description': 'GPU-trained high-performance model with all 7 safety equipment classes',
        'performance': {
            'mAP50': 0.85,  # Estimated from training
            'precision': 0.90,  # Estimated
            'recall': 0.80   # Estimated
        },
        'classes': ['OxygenTank', 'NitrogenTank', 'FirstAidBox', 'FireAlarm', 
                   'SafetySwitchPanel', 'EmergencyPhone', 'FireExtinguisher'],
        'status': 'production'
    },
    'backup_model': {
        'name': 'Backup Model (3 Classes)',
        'path': 'models/weights/best.pt',
        'description': 'Backup production model for basic detection (3 classes)',
        'performance': {
            'mAP50': 0.70,  # Estimated
            'precision': 0.85,  # Estimated
            'recall': 0.75   # Estimated
        },
        'classes': ['FireExtinguisher', 'ToolBox', 'OxygenTank'],
        'status': 'production'
    }
}

# Global model cache
model_cache = {}

def load_model(model_key):
    """Load and cache model"""
    if model_key not in model_cache:
        model_config = MODELS_CONFIG.get(model_key)
        if not model_config:
            raise ValueError(f"Unknown model: {model_key}")
        
        model_path = model_config['path']
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        logger.info(f"Loading model: {model_path}")
        try:
            model = YOLO(model_path)
            model_cache[model_key] = model
            logger.info(f"Model loaded successfully: {model_key}")
        except Exception as e:
            logger.error(f"Error loading model {model_key}: {e}")
            raise
    
    return model_cache[model_key]

def preload_models():
    """Pre-load all available models at startup"""
    logger.info("Pre-loading available models...")
    for model_id, config in MODELS_CONFIG.items():
        if os.path.exists(config['path']):
            try:
                logger.info(f"Pre-loading {model_id}...")
                load_model(model_id)
                logger.info(f"✅ {model_id} loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load {model_id}: {e}")
    logger.info("Model pre-loading complete")

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of available models"""
    models = []
    for key, config in MODELS_CONFIG.items():
        model_info = {
            'id': key,
            'name': config['name'],
            'description': config['description'],
            'performance': config['performance'],
            'classes': config['classes'],
            'status': config['status'],
            'available': os.path.exists(config['path'])
        }
        models.append(model_info)
    
    return jsonify({
        'success': True,
        'models': models,
        'total': len(models)
    })

@app.route('/api/models/<model_id>/info', methods=['GET'])
def get_model_info(model_id):
    """Get detailed information about a specific model"""
    if model_id not in MODELS_CONFIG:
        return jsonify({'success': False, 'error': 'Model not found'}), 404
    
    config = MODELS_CONFIG[model_id]
    model_path = config['path']
    
    info = {
        'id': model_id,
        'name': config['name'],
        'description': config['description'],
        'performance': config['performance'],
        'classes': config['classes'],
        'status': config['status'],
        'available': os.path.exists(model_path),
        'path': model_path
    }
    
    # Add file info if available
    if os.path.exists(model_path):
        stat = os.stat(model_path)
        info['file_size'] = stat.st_size
        info['modified'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
    
    return jsonify({
        'success': True,
        'model': info
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Run prediction on uploaded image"""
    logger.info("Received prediction request")
    
    try:
        # Get model selection
        model_id = request.form.get('model', 'flagship')
        logger.info(f"Using model: {model_id}")
        
        if model_id not in MODELS_CONFIG:
            logger.error(f"Invalid model: {model_id}")
            return jsonify({'success': False, 'error': 'Invalid model'}), 400
        
        # Get confidence threshold
        confidence = float(request.form.get('confidence', 0.5))
        logger.info(f"Confidence threshold: {confidence}")
        
        # Get image
        if 'image' not in request.files:
            logger.error("No image provided")
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            logger.error("No image selected")
            return jsonify({'success': False, 'error': 'No image selected'}), 400
        
        logger.info(f"Processing image: {image_file.filename}")
        
        # Load and process image
        image = Image.open(image_file.stream)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        logger.info("Image loaded and converted to RGB")
        
        # Load model
        logger.info("Loading model...")
        model = load_model(model_id)
        logger.info("Model loaded successfully")
        
        # Run prediction
        logger.info("Running prediction...")
        results = model(image, conf=confidence)
        logger.info("Prediction completed")
        
        # Process results
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for i in range(len(boxes)):
                    box = boxes.xyxy[i].cpu().numpy()
                    conf = boxes.conf[i].cpu().numpy()
                    cls = int(boxes.cls[i].cpu().numpy())
                    
                    # Use the model's actual class names instead of hardcoded config
                    class_name = model.names[cls] if cls in model.names else f"Unknown_{cls}"
                    
                    detection = {
                        'bbox': [float(x) for x in box],  # [x1, y1, x2, y2]
                        'confidence': float(conf),
                        'class_id': cls,
                        'class_name': class_name
                    }
                    detections.append(detection)
        
        # Get image dimensions
        img_width, img_height = image.size
        
        logger.info(f"Found {len(detections)} detections")
        
        return jsonify({
            'success': True,
            'model_used': model_id,
            'model_name': MODELS_CONFIG[model_id]['name'],
            'image_size': [img_width, img_height],
            'detections': detections,
            'detection_count': len(detections),
            'confidence_threshold': confidence,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Run prediction on multiple images"""
    try:
        model_id = request.form.get('model', 'flagship')
        confidence = float(request.form.get('confidence', 0.5))
        
        if model_id not in MODELS_CONFIG:
            return jsonify({'success': False, 'error': 'Invalid model'}), 400
        
        # Get multiple images
        images = request.files.getlist('images')
        if not images:
            return jsonify({'success': False, 'error': 'No images provided'}), 400
        
        # Load model
        model = load_model(model_id)
        
        results = []
        for i, image_file in enumerate(images):
            try:
                # Process each image
                image = Image.open(image_file.stream)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Run prediction
                pred_results = model(image, conf=confidence)
                
                # Process results
                detections = []
                for result in pred_results:
                    boxes = result.boxes
                    if boxes is not None:
                        for j in range(len(boxes)):
                            box = boxes.xyxy[j].cpu().numpy()
                            conf = boxes.conf[j].cpu().numpy()
                            cls = int(boxes.cls[j].cpu().numpy())
                            
                            # Use the model's actual class names instead of hardcoded config
                            class_name = model.names[cls] if cls in model.names else f"Unknown_{cls}"
                            
                            detection = {
                                'bbox': [float(x) for x in box],
                                'confidence': float(conf),
                                'class_id': cls,
                                'class_name': class_name
                            }
                            detections.append(detection)
                
                img_width, img_height = image.size
                results.append({
                    'image_index': i,
                    'image_name': image_file.filename,
                    'image_size': [img_width, img_height],
                    'detections': detections,
                    'detection_count': len(detections)
                })
                
            except Exception as e:
                results.append({
                    'image_index': i,
                    'image_name': image_file.filename,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'model_used': model_id,
            'model_name': MODELS_CONFIG[model_id]['name'],
            'results': results,
            'total_images': len(images),
            'confidence_threshold': confidence,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': list(model_cache.keys()),
        'available_models': list(MODELS_CONFIG.keys())
    })

if __name__ == '__main__':
    # Pre-load models at startup
    preload_models()
    app.run(debug=True, host='0.0.0.0', port=8000)