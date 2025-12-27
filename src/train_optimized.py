#!/usr/bin/env python3
"""
Ultra-Optimized Training Script for 90%+ mAP50 Performance
"""

import argparse
import os
import torch
from ultralytics import YOLO
import yaml
import shutil

def main():
    parser = argparse.ArgumentParser(description='Ultra-Optimized VISTA-S Training for 90%+ mAP50')
    parser.add_argument('--epochs', type=int, default=100, help='Number of training epochs (increased for 90%+)')
    parser.add_argument('--batch', type=int, default=16, help='Batch size (optimized for GPU)')
    parser.add_argument('--imgsz', type=int, default=640, help='Image size')
    parser.add_argument('--project', type=str, default='runs/train', help='Project directory')
    parser.add_argument('--name', type=str, default='ultra_optimized_90plus', help='Training run name')
    parser.add_argument('--hyp', type=str, default='config/hyp_clean_optimized.yaml', help='Hyperparameters file')
    parser.add_argument('--data', type=str, default='config/observo.yaml', help='Dataset configuration')
    parser.add_argument('--weights', type=str, default='yolov8n.pt', help='Initial weights')
    parser.add_argument('--device', type=str, default='', help='Device (auto-detect)')
    parser.add_argument('--workers', type=int, default=8, help='Number of workers')
    parser.add_argument('--patience', type=int, default=50, help='Early stopping patience')
    parser.add_argument('--save_period', type=int, default=10, help='Save checkpoint every N epochs')
    
    args = parser.parse_args()
    
    print("🚀 ULTRA-OPTIMIZED VISTA-S TRAINING FOR 90%+ mAP50")
    print("=" * 60)
    print(f"📊 Target: 90%+ mAP50 Performance")
    print(f"⚙️ Configuration:")
    print(f"   Epochs: {args.epochs}")
    print(f"   Batch Size: {args.batch}")
    print(f"   Image Size: {args.imgsz}")
    print(f"   Hyperparameters: {args.hyp}")
    print(f"   Dataset: {args.data}")
    print(f"   Device: {args.device if args.device else 'auto-detect'}")
    print(f"   Workers: {args.workers}")
    print(f"   Patience: {args.patience}")
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"🔥 CUDA Device: {torch.cuda.get_device_name()}")
        print(f"   CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️ CUDA not available, using CPU")
    
    # Load model
    print(f"\n📁 Loading model: {args.weights}")
    model = YOLO(args.weights)
    
    # Load hyperparameters
    if os.path.exists(args.hyp):
        print(f"📁 Loading hyperparameters: {args.hyp}")
        with open(args.hyp, 'r') as f:
            hyp = yaml.safe_load(f)
    else:
        print("⚠️ Hyperparameters file not found, using defaults")
        hyp = {}
    
    # Start training with ultra-optimized settings
    print(f"\n🚀 Starting Ultra-Optimized Training...")
    print(f"📁 Results will be saved to: {args.project}/{args.name}")
    
    try:
        results = model.train(
            data=args.data,
            epochs=args.epochs,
            batch=args.batch,
            imgsz=args.imgsz,
            project=args.project,
            name=args.name,
            device=args.device,
            workers=args.workers,
            patience=args.patience,
            save_period=args.save_period,
            cache=True,
            amp=True,  # Automatic Mixed Precision
            fraction=1.0,  # Use full dataset
            profile=False,  # Disable profiling for speed
            freeze=None,  # Don't freeze layers
            val=True,  # Validate during training
            plots=True,  # Generate plots
            save_json=True,  # Save results as JSON
            half=False,  # Don't use half precision for training
            **hyp  # Apply hyperparameters
        )
        
        print("\n✅ Training completed successfully!")
        print(f"📁 Best model saved to: {args.project}/{args.name}/weights/best.pt")
        
        # Copy best model to standard location
        best_model_path = f"{args.project}/{args.name}/weights/best.pt"
        if os.path.exists(best_model_path):
            os.makedirs("models/weights", exist_ok=True)
            shutil.copy2(best_model_path, "models/weights/ULTRA_OPTIMIZED_90PLUS.pt")
            print(f"📁 Model also saved as: models/weights/ULTRA_OPTIMIZED_90PLUS.pt")
        
        # Print final results
        print(f"\n🎯 TRAINING COMPLETE!")
        print("Check the results.csv file for detailed metrics.")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()