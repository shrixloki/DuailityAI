#!/usr/bin/env python3
"""
Performance Analysis Script for VISTA-S

Analyzes current model performance and suggests improvements
to achieve >90% mAP50 accuracy.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def analyze_training_results(results_path):
    """Analyze training results and identify improvement opportunities."""
    
    if not os.path.exists(results_path):
        print(f"❌ Results file not found: {results_path}")
        return None
    
    print(f"📊 Analyzing: {results_path}")
    
    try:
        df = pd.read_csv(results_path)
        
        # Extract key metrics
        epochs = len(df)
        best_map50 = df['metrics/mAP50(B)'].max()
        best_map50_95 = df['metrics/mAP50-95(B)'].max()
        final_map50 = df['metrics/mAP50(B)'].iloc[-1]
        best_precision = df['metrics/precision(B)'].max()
        best_recall = df['metrics/recall(B)'].max()
        
        # Find best epoch
        best_epoch = df['metrics/mAP50(B)'].idxmax() + 1
        
        # Training losses
        final_box_loss = df['train/box_loss'].iloc[-1]
        final_cls_loss = df['train/cls_loss'].iloc[-1]
        final_dfl_loss = df['train/dfl_loss'].iloc[-1]
        
        # Validation losses
        final_val_box_loss = df['val/box_loss'].iloc[-1]
        final_val_cls_loss = df['val/cls_loss'].iloc[-1]
        final_val_dfl_loss = df['val/dfl_loss'].iloc[-1]
        
        print("\n📈 PERFORMANCE ANALYSIS")
        print("=" * 50)
        print(f"🏆 Best mAP50: {best_map50:.4f} ({best_map50*100:.2f}%)")
        print(f"📊 Best mAP50-95: {best_map50_95:.4f} ({best_map50_95*100:.2f}%)")
        print(f"🎯 Final mAP50: {final_map50:.4f} ({final_map50*100:.2f}%)")
        print(f"🔍 Best Precision: {best_precision:.4f} ({best_precision*100:.2f}%)")
        print(f"🔍 Best Recall: {best_recall:.4f} ({best_recall*100:.2f}%)")
        print(f"⭐ Best Epoch: {best_epoch}/{epochs}")
        
        print(f"\n📉 FINAL LOSSES:")
        print(f"📦 Box Loss: {final_box_loss:.4f}")
        print(f"🏷️ Class Loss: {final_cls_loss:.4f}")
        print(f"📊 DFL Loss: {final_dfl_loss:.4f}")
        
        print(f"\n📉 VALIDATION LOSSES:")
        print(f"📦 Val Box Loss: {final_val_box_loss:.4f}")
        print(f"🏷️ Val Class Loss: {final_val_cls_loss:.4f}")
        print(f"📊 Val DFL Loss: {final_val_dfl_loss:.4f}")
        
        # Analyze convergence
        print(f"\n🔍 CONVERGENCE ANALYSIS:")
        
        # Check if training is still improving
        last_10_epochs = df['metrics/mAP50(B)'].tail(10)
        improvement = last_10_epochs.max() - last_10_epochs.min()
        
        if improvement > 0.01:
            print("📈 Model still improving - consider more epochs")
        else:
            print("📊 Model converged - consider different approach")
        
        # Check overfitting
        train_val_gap = abs(final_box_loss - final_val_box_loss)
        if train_val_gap > 0.1:
            print("⚠️ Possible overfitting detected")
        else:
            print("✅ No significant overfitting")
        
        # Suggestions for improvement
        print(f"\n💡 IMPROVEMENT SUGGESTIONS:")
        
        if best_map50 < 0.90:
            gap = 0.90 - best_map50
            print(f"🎯 Gap to 90%: {gap:.4f} ({gap*100:.2f} percentage points)")
            
            if best_precision < 0.95:
                print("🔧 Low precision - consider:")
                print("   - Increase classification loss weight")
                print("   - Reduce confidence threshold")
                print("   - Add hard negative mining")
            
            if best_recall < 0.80:
                print("🔧 Low recall - consider:")
                print("   - Increase box loss weight")
                print("   - More aggressive augmentation")
                print("   - Lower IoU threshold")
            
            if best_map50_95 < 0.70:
                print("🔧 Low mAP50-95 - consider:")
                print("   - Higher resolution training")
                print("   - Multi-scale training")
                print("   - Better anchor optimization")
            
            print("🚀 RECOMMENDED STRATEGIES:")
            print("   1. Use YOLOv8x (largest model)")
            print("   2. Increase image resolution to 1280+")
            print("   3. Train for more epochs (200-300)")
            print("   4. Apply Test Time Augmentation")
            print("   5. Use ensemble methods")
        else:
            print("🎉 Target achieved! Model performing excellently!")
        
        return {
            'best_map50': best_map50,
            'best_map50_95': best_map50_95,
            'best_precision': best_precision,
            'best_recall': best_recall,
            'best_epoch': best_epoch,
            'total_epochs': epochs,
            'converged': improvement <= 0.01,
            'overfitting': train_val_gap > 0.1
        }
        
    except Exception as e:
        print(f"❌ Error analyzing results: {e}")
        return None

def analyze_dataset_distribution():
    """Analyze dataset class distribution."""
    print("\n📊 DATASET ANALYSIS")
    print("=" * 50)
    
    # Check dataset configuration
    config_path = "config/observo.yaml"
    if os.path.exists(config_path):
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"📁 Dataset path: {config.get('path', 'Not specified')}")
        print(f"🏷️ Number of classes: {config.get('nc', 'Not specified')}")
        print(f"📋 Class names: {config.get('names', 'Not specified')}")
        
        # Check if dataset exists
        dataset_path = config.get('path', '')
        if os.path.exists(dataset_path):
            train_path = os.path.join(dataset_path, config.get('train', ''))
            val_path = os.path.join(dataset_path, config.get('val', ''))
            
            if os.path.exists(train_path):
                train_images = len([f for f in os.listdir(train_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                print(f"🖼️ Training images: {train_images}")
            
            if os.path.exists(val_path):
                val_images = len([f for f in os.listdir(val_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                print(f"🖼️ Validation images: {val_images}")
                
                # Calculate train/val ratio
                if train_images > 0 and val_images > 0:
                    ratio = train_images / val_images
                    print(f"📊 Train/Val ratio: {ratio:.2f}:1")
                    
                    if ratio < 3:
                        print("⚠️ Low train/val ratio - consider more training data")
                    elif ratio > 10:
                        print("⚠️ High train/val ratio - consider more validation data")
                    else:
                        print("✅ Good train/val ratio")
        else:
            print("❌ Dataset path not found")
    else:
        print("❌ Dataset configuration not found")

def compare_model_architectures():
    """Compare different YOLO model architectures."""
    print("\n🏗️ MODEL ARCHITECTURE COMPARISON")
    print("=" * 50)
    
    architectures = {
        'YOLOv8n': {'params': '3.2M', 'size': '6MB', 'speed': 'Fast', 'accuracy': 'Good'},
        'YOLOv8s': {'params': '11.2M', 'size': '22MB', 'speed': 'Fast', 'accuracy': 'Better'},
        'YOLOv8m': {'params': '25.9M', 'size': '52MB', 'speed': 'Medium', 'accuracy': 'Very Good'},
        'YOLOv8l': {'params': '43.7M', 'size': '87MB', 'speed': 'Slower', 'accuracy': 'Excellent'},
        'YOLOv8x': {'params': '68.2M', 'size': '136MB', 'speed': 'Slowest', 'accuracy': 'Best'},
    }
    
    print("📊 Architecture Comparison:")
    for arch, specs in architectures.items():
        print(f"   {arch}: {specs['params']} params, {specs['size']}, {specs['accuracy']} accuracy")
    
    print("\n💡 For >90% accuracy, recommend YOLOv8l or YOLOv8x")

def main():
    """Main analysis function."""
    print("🔍 VISTA-S PERFORMANCE ANALYSIS")
    print("🎯 Target: >90% mAP50 Accuracy")
    print("=" * 60)
    
    # Analyze current training results
    current_results = "runs/train/duality_final_gpu/results.csv"
    
    if os.path.exists(current_results):
        analysis = analyze_training_results(current_results)
        
        if analysis and analysis['best_map50'] >= 0.90:
            print("\n🎉 CONGRATULATIONS!")
            print("✅ Target of 90% mAP50 already achieved!")
            return True
    else:
        print(f"❌ No training results found at {current_results}")
        print("💡 Run training first to generate results")
    
    # Analyze dataset
    analyze_dataset_distribution()
    
    # Compare architectures
    compare_model_architectures()
    
    print("\n🚀 NEXT STEPS TO ACHIEVE 90%:")
    print("1. Run: python achieve_90_percent.py")
    print("2. This will systematically try different strategies")
    print("3. Monitor progress and adjust as needed")
    
    return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Target already achieved!")
    else:
        print("\n📈 Ready to pursue 90% accuracy target!")