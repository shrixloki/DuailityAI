import os, cv2
import yaml
from ultralytics import YOLO

def load_dataset_config():
    """Load dataset configuration from approved config file."""
    config_path = os.path.join(os.path.dirname(__file__), '../config/observo.yaml')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Dataset configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_default_test_image():
    """Get default test image path from configuration (no hard-coded paths)."""
    config = load_dataset_config()
    test_dir = os.path.join(config['path'], config['test'])
    return os.path.join(test_dir, 'sample.jpg')

def detect(image_path, model_path='models/weights/best.pt', save_dir=None):
    # Default save directory if not provided
    if save_dir is None:
        save_dir = os.environ.get('SAVE_DIR', 'models/logs/detect')
    
    # Make sure directories exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Load the model
    model = YOLO(model_path)
    
    # Run inference
    results = model.predict(source=image_path, save=True, save_dir=save_dir, imgsz=640)
    print(f"Detections saved to {save_dir}")
    return results

if __name__ == '__main__':
    import sys
    # Use configuration-driven path instead of hard-coded path
    img = sys.argv[1] if len(sys.argv)>1 else get_default_test_image()
    detect(img)