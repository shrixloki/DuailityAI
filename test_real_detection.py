#!/usr/bin/env python3
"""
Test real detection with API to verify class name fixes
"""

import requests
import json
from PIL import Image, ImageDraw
import io

def create_test_image():
    """Create a test image with some shapes that might trigger detections"""
    # Create a 640x640 image with some geometric shapes
    img = Image.new('RGB', (640, 640), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw some red rectangles (might look like fire extinguishers)
    draw.rectangle([100, 100, 200, 300], fill='red', outline='black', width=3)
    draw.rectangle([400, 150, 500, 350], fill='red', outline='black', width=3)
    
    # Draw some blue circles (might look like tanks)
    draw.ellipse([250, 200, 350, 300], fill='blue', outline='black', width=3)
    draw.ellipse([50, 400, 150, 500], fill='lightblue', outline='black', width=3)
    
    # Draw some green rectangles (might look like first aid boxes)
    draw.rectangle([300, 400, 400, 500], fill='green', outline='white', width=2)
    draw.rectangle([500, 300, 600, 400], fill='lightgreen', outline='white', width=2)
    
    return img

def test_api_detection():
    """Test the API with our test image"""
    print("🛡️ DUALITY AI - Real Detection Test")
    print("=" * 50)
    
    # Create test image
    test_img = create_test_image()
    test_img.save('api_test_image.jpg')
    
    # Test each model
    models = ['flagship', 'duality_final_gpu', 'backup_model']
    
    for model_id in models:
        print(f"\n🔍 Testing {model_id}:")
        
        try:
            # Prepare the request
            with open('api_test_image.jpg', 'rb') as img_file:
                files = {'image': img_file}
                data = {
                    'model': model_id,
                    'confidence': '0.3'  # Lower confidence to see more detections
                }
                
                # Make API request
                response = requests.post('http://localhost:8000/api/predict', 
                                       files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    if result['success']:
                        print(f"   ✅ API call successful")
                        print(f"   📊 Model: {result['model_name']}")
                        print(f"   🎯 Detections: {result['detection_count']}")
                        
                        for i, detection in enumerate(result['detections']):
                            print(f"      {i+1}. {detection['class_name']}: {detection['confidence']:.3f}")
                    else:
                        print(f"   ❌ API error: {result.get('error', 'Unknown error')}")
                else:
                    print(f"   ❌ HTTP error: {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Real detection test complete!")

if __name__ == "__main__":
    test_api_detection()