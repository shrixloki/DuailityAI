#!/usr/bin/env python3
"""
Check the structure of the hackathon dataset and prepare it for training.
"""

import os
import shutil

def check_dataset_structure(dataset_path):
    """Check what's in the dataset directory."""
    print(f"Checking dataset at: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset path does not exist: {dataset_path}")
        return False
    
    print(f"✅ Dataset path exists")
    
    # List contents
    try:
        contents = os.listdir(dataset_path)
        print(f"📁 Contents: {contents}")
        
        # Check for common YOLO dataset structures
        expected_dirs = ['train', 'val', 'test']
        found_dirs = []
        
        for item in contents:
            item_path = os.path.join(dataset_path, item)
            if os.path.isdir(item_path):
                found_dirs.append(item)
                print(f"📂 Directory: {item}")
                # Check subdirectories
                try:
                    sub_contents = os.listdir(item_path)
                    print(f"   └── Contents: {sub_contents}")
                except Exception as e:
                    print(f"   └── Error reading: {e}")
        
        # Check if we have the expected structure
        missing_dirs = [d for d in expected_dirs if d not in found_dirs]
        if missing_dirs:
            print(f"⚠️  Missing expected directories: {missing_dirs}")
            
            # Check if there are images directly in the dataset folder
            image_files = [f for f in contents if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            if image_files:
                print(f"📸 Found {len(image_files)} image files in root directory")
                print("💡 Dataset might need restructuring")
                return "needs_restructuring"
        else:
            print("✅ Found expected train/val/test structure")
            return True
            
    except Exception as e:
        print(f"❌ Error accessing dataset: {e}")
        return False

def restructure_dataset_if_needed(dataset_path):
    """Restructure dataset if all images are in one folder."""
    contents = os.listdir(dataset_path)
    
    # Check if we have images and labels in root
    image_files = [f for f in contents if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    label_files = [f for f in contents if f.lower().endswith('.txt')]
    
    if len(image_files) > 0 and len(label_files) > 0:
        print(f"Found {len(image_files)} images and {len(label_files)} labels in root")
        
        # Create train/val/test split (80/15/5)
        total_images = len(image_files)
        train_count = int(0.8 * total_images)
        val_count = int(0.15 * total_images)
        
        # Create directories
        for split in ['train', 'val', 'test']:
            os.makedirs(os.path.join(dataset_path, split, 'images'), exist_ok=True)
            os.makedirs(os.path.join(dataset_path, split, 'labels'), exist_ok=True)
        
        # Move files
        for i, img_file in enumerate(image_files):
            # Determine split
            if i < train_count:
                split = 'train'
            elif i < train_count + val_count:
                split = 'val'
            else:
                split = 'test'
            
            # Move image
            src_img = os.path.join(dataset_path, img_file)
            dst_img = os.path.join(dataset_path, split, 'images', img_file)
            shutil.move(src_img, dst_img)
            
            # Move corresponding label if exists
            label_file = img_file.rsplit('.', 1)[0] + '.txt'
            src_label = os.path.join(dataset_path, label_file)
            if os.path.exists(src_label):
                dst_label = os.path.join(dataset_path, split, 'labels', label_file)
                shutil.move(src_label, dst_label)
        
        print("✅ Dataset restructured successfully!")
        return True
    
    return False

if __name__ == "__main__":
    dataset_path = r"L:\Hackathons\Projects\Calcutta Hacks 2.O\DualityAI\hackathon2_train_3"
    
    result = check_dataset_structure(dataset_path)
    
    if result == "needs_restructuring":
        print("\n🔄 Attempting to restructure dataset...")
        if restructure_dataset_if_needed(dataset_path):
            print("✅ Dataset ready for training!")
        else:
            print("❌ Could not restructure dataset automatically")
    elif result:
        print("✅ Dataset structure looks good!")
    else:
        print("❌ Dataset check failed")