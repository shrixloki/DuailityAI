#!/usr/bin/env python3
"""
Check model class configuration for GATE 4 compliance
"""

import os
import sys
from pathlib import Path

def check_model_classes():
    """Check the number of classes in the trained model."""
    try:
        from ultralytics import YOLO
        
        # Check if model exists
        model_path = 'models/weights/best.pt'
        if not os.path.exists(model_path):
            print(f"❌ Model not found at: {model_path}")
            return None
        
        print("🔍 Loading model to check class configuration...")
        model = YOLO(model_path)
        
        # Get model information
        class_names = model.names
        num_classes = len(class_names)
        
        print(f"📊 Model Class Information:")
        print(f"   Number of classes: {num_classes}")
        print(f"   Class names: {list(class_names.values())}")
        
        return {
            'num_classes': num_classes,
            'class_names': class_names,
            'model_path': model_path
        }
        
    except Exception as e:
        print(f"❌ Error checking model: {e}")
        return None

def check_config_classes():
    """Check the number of classes in configuration files."""
    config_files = [
        'config/observo.yaml',
        'data/raw/yolo_params.yaml',
        'hyp_optimized.yaml'
    ]
    
    configs = {}
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                
                if config and 'nc' in config:
                    configs[config_file] = {
                        'nc': config['nc'],
                        'names': config.get('names', [])
                    }
                    print(f"📁 {config_file}:")
                    print(f"   Classes: {config['nc']}")
                    print(f"   Names: {config.get('names', [])}")
                
            except Exception as e:
                print(f"❌ Error reading {config_file}: {e}")
    
    return configs

def check_gate4_compliance():
    """Check GATE 4 compliance requirements."""
    print("🎯 GATE 4 — MODEL CORRECTNESS COMPLIANCE CHECK")
    print("=" * 60)
    
    # Check model classes
    model_info = check_model_classes()
    
    print("\n🔍 Configuration Files:")
    config_info = check_config_classes()
    
    print("\n📋 GATE 4 Requirements:")
    print("   ✅ Final model outputs 7 classes")
    print("   ✅ Model head dimension = 7") 
    print("   ✅ No extra / missing classes")
    print("   ✅ Class order documented and matches dataset config")
    
    print("\n📊 Compliance Analysis:")
    
    if model_info:
        num_classes = model_info['num_classes']
        if num_classes == 7:
            print(f"   ✅ Model has {num_classes} classes (COMPLIANT)")
        else:
            print(f"   ❌ Model has {num_classes} classes, expected 7 (NON-COMPLIANT)")
    else:
        print("   ❌ Could not check model classes")
    
    # Check if any config has 7 classes
    has_7_classes_config = any(info['nc'] == 7 for info in config_info.values())
    
    if has_7_classes_config:
        print("   ✅ Configuration with 7 classes found")
    else:
        print("   ❌ No configuration with 7 classes found")
        print("   💡 Current config has 3 classes - needs update for GATE 4")
    
    return model_info, config_info

if __name__ == "__main__":
    model_info, config_info = check_gate4_compliance()