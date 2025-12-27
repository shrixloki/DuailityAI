#!/usr/bin/env python3
"""
Full Stack Deployment Script
Starts both backend API and frontend development server
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Start the Flask backend API"""
    print("🚀 Starting Backend API Server...")
    try:
        # Change to project root
        os.chdir(Path(__file__).parent)
        
        # Start Flask API
        subprocess.run([
            sys.executable, "src/model_api.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Backend server stopped")

def run_frontend():
    """Start the React frontend development server"""
    print("🚀 Starting Frontend Development Server...")
    try:
        # Change to frontend directory
        frontend_dir = Path(__file__).parent / "Web_App_frontend"
        os.chdir(frontend_dir)
        
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start development server
        subprocess.run(["npm", "run", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Frontend server stopped")

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import ultralytics
        import PIL
        print("✅ Python dependencies available")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Install with: pip install flask flask-cors ultralytics pillow")
        return False
    
    # Check Node.js
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ Node.js and npm available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js or npm not found")
        print("Install Node.js from: https://nodejs.org/")
        return False
    
    return True

def main():
    print("🏆 DUALITY AI - FULL STACK MODEL INTEGRATION")
    print("=" * 60)
    
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing dependencies.")
        return
    
    print("\n🚀 Starting Full Stack Application...")
    print("Backend API: http://localhost:8000")
    print("Frontend UI: http://localhost:3000 (or similar)")
    print("\nPress Ctrl+C to stop both servers")
    print("-" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(3)
    
    try:
        # Start frontend (this will block)
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("✅ Full stack application stopped")

if __name__ == "__main__":
    main()