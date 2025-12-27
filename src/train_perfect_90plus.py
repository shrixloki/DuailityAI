#!/usr/bin/env python3
"""
Perfect Training Script for 90%+ mAP50 Accuracy
Multi-stage training with progressive optimization
"""

import os
import torch
import yaml
from ultralytics import YOLO
from datetime import datetime
import shutil

class PerfectTrainer:
    def __init__(self):
        self.target_map50 = 0.90
        self.stages = [
            {
                'name': 'Stage 1: Foundation Training',
                'epochs': 60,
                'batch': 16,
                'imgsz': 640,
                'model': 'yolov8n.pt',
                'patience': 25
            },
            {
                'name': 'Stage 2: Enhanced Training',
                'epochs': 80,
                'batch': 12,
                'imgsz': 832,
                'model': 'best_from_stage1',
                'patience': 30
            },
            {
                'name': 'Stage 3: Perfect Fine-tuning',
                'epochs': 100,
                'batch': 8,
                'imgsz': 1024,
                'model': 'best_from_stage2',
                'patience': 40
            }
        ]
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] PERFECT: {message}")
    
    def train_stage(self, stage_config, stage_num):
        """Train a single stage"""
        self.log(f"🚀 Starting {stage_config['name']}")
        
        # Determine model path
        if stage_config['model'] == 'best_from_stage1':
            model_path = 'runs/train/perfect_stage1/weights/best.pt'
        elif stage_config['model'] == 'best_from_stage2':
            model_path = 'runs/train/perfect_stage2/weights/best.pt'
        else:
            model_path = stage_config['model']
        
        # Load model
        model = YOLO(model_path)
        
        # Training parameters
        train_name = f"perfect_stage{stage_num}"
        
        try:
            results = model.train(
                data='config/observo.yaml',
                epochs=stage_config['epochs'],
                batch=stage_config['batch'],
                imgsz=stage_config['imgsz'],
                project='runs/train',
                name=train_name,
                patience=stage_config['patience'],
                save_period=10,
                cache=True,
                amp=True,
                fraction=1.0,
                multi_scale=True,
                overlap_mask=True,
                mask_ratio=4,
                dropout=0.0,
                val=True,
                plots=True,
                cos_lr=True,
                close_mosaic=15,
                auto_augment='randaugment',
                erasing=0.5,
                label_smoothing=0.15,
                # Load perfect hyperparameters
                cfg='config/hyp_perfect_90plus.yaml'
            )
            
            # Check results
            best_model_path = f'runs/train/{train_name}/weights/best.pt'
            if os.path.exists(best_model_path):
                # Load and evaluate
                best_model = YOLO(best_model_path)
                val_results = best_model.val(data='config/observo.yaml')
                
                map50 = val_results.box.map50
                self.log(f"✅ {stage_config['name']} completed!")
                self.log(f"📊 mAP50: {map50:.4f} ({map50*100:.2f}%)")
                
                if map50 >= self.target_map50:
                    self.log(f"🎉 TARGET ACHIEVED! {map50*100:.2f}% >= 90%")
                    return True, map50
                
                return False, map50
            else:
                self.log(f"❌ Best model not found for {stage_config['name']}")
                return False, 0.0
                
        except Exception as e:
            self.log(f"❌ Stage {stage_num} failed: {e}")
            return False, 0.0
    
    def run_perfect_training(self):
        """Run multi-stage perfect training"""
        self.log("🎯 PERFECT TRAINING FOR 90%+ mAP50")
        self.log("=" * 60)
        
        best_map50 = 0.0
        
        for i, stage in enumerate(self.stages, 1):
            success, map50 = self.train_stage(stage, i)
            
            if map50 > best_map50:
                best_map50 = map50
                
                # Copy best model to standard location
                stage_best = f'runs/train/perfect_stage{i}/weights/best.pt'
                if os.path.exists(stage_best):
                    os.makedirs('models/weights', exist_ok=True)
                    shutil.copy2(stage_best, 'models/weights/PERFECT_90PLUS_MODEL.pt')
                    self.log(f"📁 Best model updated: PERFECT_90PLUS_MODEL.pt")
            
            if success:
                self.log(f"🎉 PERFECT ACCURACY ACHIEVED IN STAGE {i}!")
                break
            
            self.log(f"📈 Stage {i} best: {map50*100:.2f}%, continuing...")
        
        self.log(f"\n🏆 FINAL RESULTS:")
        self.log(f"   Best mAP50: {best_map50:.4f} ({best_map50*100:.2f}%)")
        
        if best_map50 >= self.target_map50:
            self.log("🎉 SUCCESS: 90%+ ACCURACY ACHIEVED!")
            return True
        else:
            gap = self.target_map50 - best_map50
            self.log(f"⚠️ Gap remaining: {gap:.4f} ({gap*100:.2f}%)")
            return False

def main():
    trainer = PerfectTrainer()
    success = trainer.run_perfect_training()
    
    if success:
        print("\n🎯 PERFECT TRAINING COMPLETED SUCCESSFULLY!")
    else:
        print("\n📈 Training completed, may need additional optimization")

if __name__ == "__main__":
    main()
