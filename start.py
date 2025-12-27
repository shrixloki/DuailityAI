#!/usr/bin/env python3
"""
Quick Start Script - Simplified version
Starts the essential components only
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def main():
    print("🚀 DUALITY AI - Quick Start")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    
    # Start Model API in background
    print("🔧 Starting Model API...")
    model_api_process = subprocess.Popen([
        sys.executable, "src/model_api.py"
    ], cwd=project_root)
    
    # Wait a moment for API to start
    time.sleep(3)
    
    # Start Frontend
    print("🌐 Starting Frontend...")
    frontend_dir = project_root / "Web_App_frontend"
    
    # Install deps if needed
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
    
    try:
        # Start frontend (this will block)
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        model_api_process.terminate()
        print("✅ Services stopped")

if __name__ == "__main__":
    main()