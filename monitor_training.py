#!/usr/bin/env python3
"""
Monitor Ultra-Optimized Training Progress for 90%+ mAP50
"""

import os
import time
import glob

def monitor_training():
    print("🔍 MONITORING ULTRA-OPTIMIZED TRAINING FOR 90%+ mAP50")
    print("=" * 60)
    
    # Find the latest training run
    training_dirs = glob.glob("runs/train/ultra_90plus*")
    if not training_dirs:
        print("❌ No ultra-optimized training runs found")
        return
    
    latest_dir = max(training_dirs, key=os.path.getctime)
    results_file = os.path.join(latest_dir, "results.csv")
    
    print(f"📁 Monitoring: {latest_dir}")
    print(f"📊 Results file: {results_file}")
    
    if not os.path.exists(results_file):
        print("⏳ Training starting... results file not yet created")
        return
    
    # Read and display current progress
    with open(results_file, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        print("⏳ Training in progress... no results yet")
        return
    
    # Parse header
    header = lines[0].strip().split(',')
    epoch_idx = header.index('epoch')
    map50_idx = header.index('metrics/mAP50(B)')
    precision_idx = header.index('metrics/precision(B)')
    recall_idx = header.index('metrics/recall(B)')
    
    # Get latest results
    latest_line = lines[-1].strip().split(',')
    current_epoch = int(float(latest_line[epoch_idx]))
    current_map50 = float(latest_line[map50_idx])
    current_precision = float(latest_line[precision_idx])
    current_recall = float(latest_line[recall_idx])
    
    # Find best so far
    best_map50 = 0.0
    for line in lines[1:]:
        values = line.strip().split(',')
        if len(values) > map50_idx:
            map50 = float(values[map50_idx])
            if map50 > best_map50:
                best_map50 = map50
    
    print(f"\n📊 CURRENT PROGRESS:")
    print(f"   Epoch: {current_epoch}/100")
    print(f"   Current mAP50: {current_map50:.4f} ({current_map50*100:.2f}%)")
    print(f"   Best mAP50 so far: {best_map50:.4f} ({best_map50*100:.2f}%)")
    print(f"   Current Precision: {current_precision:.4f} ({current_precision*100:.2f}%)")
    print(f"   Current Recall: {current_recall:.4f} ({current_recall*100:.2f}%)")
    
    # Progress towards 90%
    progress_to_90 = (best_map50 / 0.9) * 100
    print(f"\n🎯 PROGRESS TOWARDS 90% TARGET:")
    print(f"   Progress: {progress_to_90:.1f}% of target")
    print(f"   Remaining: {0.9 - best_map50:.4f} ({(0.9 - best_map50)*100:.2f}%)")
    
    if best_map50 >= 0.9:
        print("🎉 TARGET ACHIEVED! 90%+ mAP50 reached!")
    elif best_map50 >= 0.85:
        print("🔥 EXCELLENT PROGRESS! Very close to 90%!")
    elif best_map50 >= 0.8:
        print("✅ GOOD PROGRESS! On track for 90%!")
    else:
        print("⏳ EARLY STAGES: Building up performance...")
    
    # Estimate completion time
    if current_epoch > 0:
        epochs_remaining = 100 - current_epoch
        print(f"\n⏰ ESTIMATED TIME:")
        print(f"   Epochs remaining: {epochs_remaining}")
        print(f"   Estimated completion: ~{epochs_remaining * 0.5:.0f} minutes")

if __name__ == "__main__":
    monitor_training()