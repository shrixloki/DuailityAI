#!/usr/bin/env python3
"""
Show the actual capabilities of each model
"""

from ultralytics import YOLO
import os

def show_model_capabilities():
    print("🛡️ DUALITY AI - Model Capabilities Report")
    print("=" * 60)
    
    models = {
        'flagship': {
            'path': 'models/weights/FINAL_SELECTED_MODEL.pt',
            'description': 'Main production model'
        },
        'duality_final_gpu': {
            'path': 'runs/train/duality_final_gpu/weights/best.pt',
            'description': 'GPU-trained comprehensive model'
        },
        'backup_model': {
            'path': 'models/weights/best.pt',
            'description': 'Backup model'
        }
    }
    
    for model_id, config in models.items():
        print(f"\n🎯 {model_id.upper()}")
        print(f"   Description: {config['description']}")
        print(f"   Path: {config['path']}")
        
        if os.path.exists(config['path']):
            try:
                model = YOLO(config['path'])
                print(f"   ✅ Status: Available")
                print(f"   📊 Total Classes: {len(model.names)}")
                print(f"   🏷️  Detection Classes:")
                
                for class_id, class_name in model.names.items():
                    print(f"      {class_id}: {class_name}")
                    
            except Exception as e:
                print(f"   ❌ Error loading: {e}")
        else:
            print(f"   ❌ Status: File not found")
    
    print("\n" + "🎯 RECOMMENDATIONS:")
    print("   • Use 'duality_final_gpu' for best results (7 classes)")
    print("   • Use 'flagship' or 'backup_model' for basic detection (3 classes)")
    print("   • Lower confidence threshold (0.3-0.5) for more detections")
    print("   • Higher confidence threshold (0.7-0.9) for more accurate detections")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    show_model_capabilities()