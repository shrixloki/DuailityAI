#!/usr/bin/env python3
"""
Debug Model Predictions - Test all models with sample images
"""

import os
from ultralytics import YOLO
from PIL import Image
import requests
import numpy as np

def test_model_predictions():
    print("🛡️ DUALITY AI - Model Prediction Debug")
    print("=" * 60)
    
    # Model configurations
    models = {
        'flagship': 'models/weights/FINAL_SELECTED_MODEL.pt',
        'duality_final_gpu': 'runs/train/duality_final_gpu/weights/best.pt',
        'backup_model': 'models/weights/best.pt'
    }
    
    # Create a simple test image (solid color)
    test_image = Image.new('RGB', (640, 640), color='blue')
    test_image.save('test_image.jpg')
    
    for model_id, model_path in models.items():
        print(f"\n🔍 Testing {model_id}:")
        print(f"   Path: {model_path}")
        
        if not os.path.exists(model_path):
            print(f"   ❌ Model file not found")
            continue
            
        try:
            # Load model
            model = YOLO(model_path)
            print(f"   ✅ Model loaded successfully")
            print(f"   📊 Classes: {model.names}")
            
            # Test prediction on simple image
            results = model('test_image.jpg', conf=0.1)  # Low confidence to see all detections
            
            print(f"   🎯 Predictions on test image:")
            for result in results:
                boxes = result.boxes
                if boxes is not None and len(boxes) > 0:
                    for i in range(len(boxes)):
                        conf = boxes.conf[i].cpu().numpy()
                        cls = int(boxes.cls[i].cpu().numpy())
                        class_name = model.names[cls]
                        print(f"      - {class_name}: {conf:.3f} confidence")
                else:
                    print(f"      - No detections (good for test image)")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Clean up
    if os.path.exists('test_image.jpg'):
        os.remove('test_image.jpg')
    
    print("\n" + "=" * 60)
    print("🔍 Debug complete!")

if __name__ == "__main__":
    test_model_predictions()