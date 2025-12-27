#!/usr/bin/env python3
"""
90% Recall Training Script - Maximum Object Detection Sensitivity
"""

import argparse
import os
import torch
from ultralytics import YOLO
import yaml
import shutil

def main():
    parser = argparse.ArgumentParser(description='90% Recall Training - Maximum Detection Sensitivity')
    parser.add_argument('--epochs', type=int, default=120, help='Number of training epochs (extended for recall)')
    parser.add_argument('--batch', type=int, default=12, help='Batch size (optimized for recall)')
    parser.add_argument('--imgsz', type=int, default=640, help='Image size')
    parser.add_argument('--project', type=str, default='runs/train', help='Project directory')
    parser.add_argument('--name', type=str, default='recall_90_target', help='Training run name')
    parser.add_argument('--hyp', type=str, default='config/hyp_recall_valid.yaml', help='Recall-optimized hyperparameters')
    parser.add_argument('--data', type=str, default='config/observo.yaml', help='Dataset configuration')
    parser.add_argument('--weights', type=str, default='yolov8n.pt', help='Initial weights')
    parser.add_argument('--device', type=str, default='', help='Device (auto-detect)')
    parser.add_argument('--workers', type=int, default=8, help='Number of workers')
    parser.add_argument('--patience', type=int, default=80, help='Early stopping patience')
    parser.add_argument('--save_period', type=int, default=5, help='Save checkpoint every N epochs')
    
    args = parser.parse_args()
    
    print("🎯 90% RECALL TRAINING - MAXIMUM DETECTION SENSITIVITY")
    print("=" * 65)
    print(f"📊 Target: 90% Recall (Maximum Object Detection)")
    print(f"⚙️ Configuration:")
    print(f"   Epochs: {args.epochs} (extended for recall convergence)")
    print(f"   Batch Size: {args.batch} (optimized for recall)")
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
    
    # Load recall-optimized hyperparameters
    if os.path.exists(args.hyp):
        print(f"📁 Loading recall-optimized hyperparameters: {args.hyp}")
        with open(args.hyp, 'r') as f:
            hyp = yaml.safe_load(f)
    else:
        print("⚠️ Hyperparameters file not found, using defaults")
        hyp = {}
    
    # Display recall optimization strategy
    print(f"\n🚀 RECALL OPTIMIZATION STRATEGY:")
    print("1. ✅ Higher box loss weight (10.0) - Better localization")
    print("2. ✅ Lower class loss weight (0.3) - Prioritize detection")
    print("3. ✅ Lower anchor threshold (3.0) - More detections")
    print("4. ✅ Aggressive augmentation - Better generalization")
    print("5. ✅ Extended training (120 epochs) - Full convergence")
    print("6. ✅ AdamW optimizer - Better gradient handling")
    print("7. ✅ Multi-scale training - Size robustness")
    print("8. ✅ Higher learning rates - Faster recall learning")
    
    # Start recall-optimized training
    print(f"\n🚀 Starting 90% Recall Training...")
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
            **hyp  # Apply recall-optimized hyperparameters
        )
        
        print("\n✅ 90% Recall Training completed successfully!")
        print(f"📁 Best model saved to: {args.project}/{args.name}/weights/best.pt")
        
        # Copy best model to standard location
        best_model_path = f"{args.project}/{args.name}/weights/best.pt"
        if os.path.exists(best_model_path):
            os.makedirs("models/weights", exist_ok=True)
            shutil.copy2(best_model_path, "models/weights/RECALL_90_OPTIMIZED.pt")
            print(f"📁 Model also saved as: models/weights/RECALL_90_OPTIMIZED.pt")
        
        print(f"\n🎯 RECALL TRAINING COMPLETE!")
        print("Check the results.csv file for detailed recall metrics.")
        print("Expected: 90%+ recall with optimized precision balance.")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()