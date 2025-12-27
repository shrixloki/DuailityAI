#!/usr/bin/env python3
"""
Quick test to verify all models can be loaded
"""

import os
from ultralytics import YOLO

# Model paths from the API
models = {
    'flagship': 'models/weights/FINAL_SELECTED_MODEL.pt',
    'duality_final_gpu': 'runs/train/duality_final_gpu/weights/best.pt',
    'backup_model': 'models/weights/best.pt'
}

print("🛡️ DUALITY AI - Model Verification Test")
print("=" * 50)

for model_id, model_path in models.items():
    print(f"\n🔍 Testing {model_id}:")
    print(f"   Path: {model_path}")
    
    if os.path.exists(model_path):
        print(f"   ✅ File exists")
        try:
            model = YOLO(model_path)
            print(f"   ✅ Model loads successfully")
            print(f"   📊 Classes: {len(model.names)} classes")
            print(f"   🏷️  Names: {list(model.names.values())}")
        except Exception as e:
            print(f"   ❌ Failed to load: {e}")
    else:
        print(f"   ❌ File not found")

print("\n" + "=" * 50)
print("✅ Model verification complete!")