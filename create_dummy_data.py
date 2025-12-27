#!/usr/bin/env python3
"""
Create minimal dummy dataset for retraining the model head with correct labels.
This is a temporary solution to allow the training to proceed.
"""

import os
import numpy as np
from PIL import Image

def create_dummy_image(path, size=(640, 640)):
    """Create a dummy image with random noise."""
    # Create random RGB image
    img_array = np.random.randint(0, 255, (size[1], size[0], 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save(path)

def create_dummy_label(path, num_objects=2):
    """Create a dummy YOLO format label file."""
    with open(path, 'w') as f:
        for i in range(num_objects):
            # YOLO format: class_id center_x center_y width height (normalized 0-1)
            class_id = i % 7  # Use classes 0-6 (7 classes total)
            center_x = 0.3 + (i * 0.2)  # Spread objects across image
            center_y = 0.4 + (i * 0.1)
            width = 0.1 + (i * 0.05)
            height = 0.1 + (i * 0.05)
            f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")

def create_minimal_dataset():
    """Create minimal dataset structure with dummy data."""
    
    # Create dummy data for train, val, test
    splits = ['train', 'val', 'test']
    num_images = {'train': 10, 'val': 3, 'test': 2}  # Minimal counts
    
    for split in splits:
        img_dir = f"data/raw/{split}/images"
        label_dir = f"data/raw/{split}/labels"
        
        # Ensure directories exist
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)
        
        # Create dummy images and labels
        for i in range(num_images[split]):
            img_name = f"dummy_{i:03d}.jpg"
            label_name = f"dummy_{i:03d}.txt"
            
            img_path = os.path.join(img_dir, img_name)
            label_path = os.path.join(label_dir, label_name)
            
            create_dummy_image(img_path)
            create_dummy_label(label_path, num_objects=min(2, i+1))
            
        print(f"Created {num_images[split]} dummy images and labels for {split} split")

if __name__ == "__main__":
    print("Creating minimal dummy dataset for model head retraining...")
    create_minimal_dataset()
    print("✅ Dummy dataset created successfully!")
    print("⚠️  Note: This is minimal dummy data for retraining the model head only.")