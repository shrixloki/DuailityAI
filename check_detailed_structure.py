#!/usr/bin/env python3
"""
Check the detailed structure of the hackathon dataset.
"""

import os

def check_detailed_structure():
    """Check the detailed structure of train3 and val3."""
    base_path = r"L:\Hackathons\Projects\Calcutta Hacks 2.O\DualityAI\hackathon2_train_3\train_3"
    
    for split in ['train3', 'val3']:
        split_path = os.path.join(base_path, split)
        print(f"\n📂 Checking {split}:")
        
        if os.path.exists(split_path):
            contents = os.listdir(split_path)
            print(f"   Contents: {contents}")
            
            # Check if there are images and labels subdirectories
            for item in contents:
                item_path = os.path.join(split_path, item)
                if os.path.isdir(item_path):
                    sub_contents = os.listdir(item_path)
                    print(f"   📁 {item}/: {len(sub_contents)} files")
                    if len(sub_contents) > 0:
                        # Show first few files as examples
                        examples = sub_contents[:3]
                        print(f"      Examples: {examples}")
                elif item.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.txt')):
                    print(f"   📄 Direct file: {item}")
        else:
            print(f"   ❌ Path does not exist: {split_path}")

if __name__ == "__main__":
    check_detailed_structure()