#!/usr/bin/env python3
"""
Monitor Perfect Training Progress
Real-time monitoring of the 90%+ accuracy training
"""

import os
import time
import pandas as pd
from datetime import datetime

def monitor_training():
    """Monitor the perfect training progress"""
    
    results_path = "runs/train/perfect_90plus/results.csv"
    target_map50 = 0.90
    
    print("🎯 PERFECT TRAINING MONITOR")
    print("=" * 50)
    print(f"Target: {target_map50*100:.1f}% mAP50")
    print(f"Results file: {results_path}")
    print("Monitoring every 30 seconds...")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 50)
    
    last_epoch = 0
    best_map50 = 0.0
    
    while True:
        try:
            if os.path.exists(results_path):
                df = pd.read_csv(results_path)
                
                if len(df) > last_epoch:
                    # New epoch data available
                    latest = df.iloc[-1]
                    current_epoch = len(df)
                    current_map50 = latest['metrics/mAP50(B)']
                    current_precision = latest['metrics/precision(B)']
                    current_recall = latest['metrics/recall(B)']
                    
                    # Update best
                    if current_map50 > best_map50:
                        best_map50 = current_map50
                        best_epoch = current_epoch
                    
                    # Progress calculation
                    progress = (current_map50 / target_map50) * 100
                    gap = target_map50 - current_map50
                    
                    # Status
                    status = "🎉 TARGET ACHIEVED!" if current_map50 >= target_map50 else "📈 Training..."
                    
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Epoch {current_epoch}/120")
                    print(f"   Current mAP50: {current_map50:.4f} ({current_map50*100:.2f}%)")
                    print(f"   Best mAP50: {best_map50:.4f} ({best_map50*100:.2f}%) at epoch {best_epoch}")
                    print(f"   Precision: {current_precision:.4f} ({current_precision*100:.2f}%)")
                    print(f"   Recall: {current_recall:.4f} ({current_recall*100:.2f}%)")
                    print(f"   Progress: {progress:.1f}% to target")
                    print(f"   Gap: {gap:.4f} ({gap*100:.2f}%)")
                    print(f"   Status: {status}")
                    
                    if current_map50 >= target_map50:
                        print("\n🎉 SUCCESS! 90%+ mAP50 ACHIEVED!")
                        print(f"🏆 Final result: {current_map50*100:.2f}% mAP50")
                        break
                    
                    last_epoch = current_epoch
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for training to start...")
            
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

def show_final_results():
    """Show final training results"""
    
    results_path = "runs/train/perfect_90plus/results.csv"
    
    if os.path.exists(results_path):
        df = pd.read_csv(results_path)
        
        best_map50 = df['metrics/mAP50(B)'].max()
        best_epoch = df['metrics/mAP50(B)'].idxmax() + 1
        final_map50 = df['metrics/mAP50(B)'].iloc[-1]
        best_precision = df['metrics/precision(B)'].max()
        best_recall = df['metrics/recall(B)'].max()
        
        print("\n🏆 FINAL TRAINING RESULTS")
        print("=" * 50)
        print(f"Best mAP50: {best_map50:.4f} ({best_map50*100:.2f}%)")
        print(f"Final mAP50: {final_map50:.4f} ({final_map50*100:.2f}%)")
        print(f"Best Precision: {best_precision:.4f} ({best_precision*100:.2f}%)")
        print(f"Best Recall: {best_recall:.4f} ({best_recall*100:.2f}%)")
        print(f"Best Epoch: {best_epoch}")
        print(f"Total Epochs: {len(df)}")
        
        if best_map50 >= 0.90:
            print("\n🎉 SUCCESS: 90%+ mAP50 ACHIEVED!")
            print("✅ Perfect accuracy target reached!")
        else:
            gap = 0.90 - best_map50
            print(f"\n📈 Gap to 90%: {gap:.4f} ({gap*100:.2f}%)")
            print("Consider additional optimization strategies")
        
        # Model file locations
        best_model = "runs/train/perfect_90plus/weights/best.pt"
        if os.path.exists(best_model):
            print(f"\n📁 Best model: {best_model}")
            print("Ready for deployment!")
    else:
        print("No training results found")

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "results":
        show_final_results()
    else:
        monitor_training()

if __name__ == "__main__":
    main()