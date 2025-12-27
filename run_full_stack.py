#!/usr/bin/env python3
"""
Complete Full Stack Startup Script
Starts all components: Frontend, Backend APIs, and Models
No Docker required - runs everything locally
"""

import subprocess
import sys
import os
import time
import threading
import signal
import json
from pathlib import Path
import requests
import webbrowser
from datetime import datetime

class FullStackManager:
    def __init__(self):
        self.processes = []
        self.project_root = Path(__file__).parent
        self.running = True
        
    def log(self, message, component="MAIN"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {component}: {message}")
        
    def check_port(self, port, service_name):
        """Check if a port is available"""
        try:
            response = requests.get(f"http://localhost:{port}/api/health", timeout=2)
            if response.status_code == 200:
                self.log(f"✅ {service_name} already running on port {port}", "CHECK")
                return True
        except:
            pass
        return False
        
    def check_dependencies(self):
        """Check if all required dependencies are available"""
        self.log("🔍 Checking system dependencies...", "DEPS")
        
        missing_deps = []
        
        # Check Python dependencies
        python_deps = [
            ('flask', 'Flask'),
            ('flask_cors', 'Flask-CORS'), 
            ('ultralytics', 'Ultralytics YOLO'),
            ('PIL', 'Pillow'),
            ('torch', 'PyTorch'),
            ('numpy', 'NumPy')
        ]
        
        for module, name in python_deps:
            try:
                __import__(module)
                self.log(f"✅ {name} available", "DEPS")
            except ImportError:
                self.log(f"❌ {name} missing", "DEPS")
                missing_deps.append(name)
        
        # Check Node.js and npm
        node_ok = False
        npm_ok = False
        
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
            node_version = result.stdout.strip()
            self.log(f"✅ Node.js {node_version} available", "DEPS")
            node_ok = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("❌ Node.js not found", "DEPS")
        
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
            npm_version = result.stdout.strip()
            self.log(f"✅ npm {npm_version} available", "DEPS")
            npm_ok = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("❌ npm not found", "DEPS")
        
        if not (node_ok and npm_ok):
            missing_deps.append("Node.js/npm")
        
        # Check model files
        model_paths = [
            "models/weights/FINAL_SELECTED_MODEL.pt",
            "models/weights/best.pt"
        ]
        
        for model_path in model_paths:
            if (self.project_root / model_path).exists():
                self.log(f"✅ Model found: {model_path}", "DEPS")
            else:
                self.log(f"⚠️  Model not found: {model_path}", "DEPS")
        
        if missing_deps:
            self.log("❌ Missing dependencies. Install with:", "DEPS")
            if any("Node.js" in dep for dep in missing_deps):
                self.log("   - Install Node.js from: https://nodejs.org/", "DEPS")
            python_missing = [dep for dep in missing_deps if dep != "Node.js"]
            if python_missing:
                self.log(f"   - pip install flask flask-cors ultralytics pillow torch numpy", "DEPS")
            return False
            
        return True
    
    def setup_frontend(self):
        """Setup frontend dependencies if needed"""
        frontend_dir = self.project_root / "Web_App_frontend"
        node_modules = frontend_dir / "node_modules"
        
        if not node_modules.exists():
            self.log("📦 Installing frontend dependencies...", "FRONTEND")
            try:
                subprocess.run(
                    ["npm", "install"], 
                    cwd=frontend_dir, 
                    check=True,
                    capture_output=True
                )
                self.log("✅ Frontend dependencies installed", "FRONTEND")
            except subprocess.CalledProcessError as e:
                self.log(f"❌ Failed to install frontend deps: {e}", "FRONTEND")
                return False
        else:
            self.log("✅ Frontend dependencies already installed", "FRONTEND")
        
        return True
    
    def start_model_api(self):
        """Start the main model API server"""
        if self.check_port(8000, "Model API"):
            return
            
        self.log("🚀 Starting Model API Server (Port 8000)...", "MODEL-API")
        
        def run_model_api():
            try:
                os.chdir(self.project_root)
                process = subprocess.Popen([
                    sys.executable, "src/model_api.py"
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                self.processes.append(process)
                
                # Monitor output
                for line in iter(process.stdout.readline, ''):
                    if self.running:
                        self.log(line.strip(), "MODEL-API")
                    else:
                        break
                        
            except Exception as e:
                self.log(f"❌ Model API failed: {e}", "MODEL-API")
        
        thread = threading.Thread(target=run_model_api, daemon=True)
        thread.start()
        
        # Wait for API to be ready
        for i in range(30):  # Wait up to 30 seconds
            if self.check_port(8000, "Model API"):
                self.log("✅ Model API is ready!", "MODEL-API")
                return
            time.sleep(1)
        
        self.log("⚠️  Model API may not be ready yet", "MODEL-API")
    
    def start_web_backend(self):
        """Start the web application backend"""
        if self.check_port(8001, "Web Backend"):
            return
            
        self.log("🚀 Starting Web Backend (Port 8001)...", "WEB-BACKEND")
        
        def run_web_backend():
            try:
                os.chdir(self.project_root)
                env = os.environ.copy()
                env['PORT'] = '8001'
                
                process = subprocess.Popen([
                    sys.executable, "app/backend.py"
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                   text=True, env=env)
                
                self.processes.append(process)
                
                # Monitor output
                for line in iter(process.stdout.readline, ''):
                    if self.running:
                        self.log(line.strip(), "WEB-BACKEND")
                    else:
                        break
                        
            except Exception as e:
                self.log(f"❌ Web Backend failed: {e}", "WEB-BACKEND")
        
        thread = threading.Thread(target=run_web_backend, daemon=True)
        thread.start()
        
        # Wait for backend to be ready
        for i in range(20):
            if self.check_port(8001, "Web Backend"):
                self.log("✅ Web Backend is ready!", "WEB-BACKEND")
                return
            time.sleep(1)
    
    def start_frontend(self):
        """Start the React frontend development server"""
        self.log("🚀 Starting Frontend Development Server...", "FRONTEND")
        
        def run_frontend():
            try:
                frontend_dir = self.project_root / "Web_App_frontend"
                os.chdir(frontend_dir)
                
                process = subprocess.Popen([
                    "npm", "run", "dev"
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                self.processes.append(process)
                
                # Monitor output and look for the dev server URL
                for line in iter(process.stdout.readline, ''):
                    if self.running:
                        self.log(line.strip(), "FRONTEND")
                        # Look for Vite dev server URL
                        if "Local:" in line and "http://" in line:
                            url = line.split("http://")[1].split()[0]
                            self.log(f"🌐 Frontend available at: http://{url}", "FRONTEND")
                    else:
                        break
                        
            except Exception as e:
                self.log(f"❌ Frontend failed: {e}", "FRONTEND")
        
        thread = threading.Thread(target=run_frontend, daemon=True)
        thread.start()
    
    def start_mobile_metro(self):
        """Start React Native Metro bundler (optional)"""
        mobile_dir = self.project_root / "mobile"
        if not mobile_dir.exists():
            return
            
        self.log("📱 Starting React Native Metro Bundler...", "MOBILE")
        
        def run_metro():
            try:
                os.chdir(mobile_dir)
                
                # Check if node_modules exists
                if not (mobile_dir / "node_modules").exists():
                    self.log("📦 Installing mobile dependencies...", "MOBILE")
                    subprocess.run(["npm", "install"], check=True)
                
                process = subprocess.Popen([
                    "npm", "start"
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                self.processes.append(process)
                
                for line in iter(process.stdout.readline, ''):
                    if self.running:
                        self.log(line.strip(), "MOBILE")
                    else:
                        break
                        
            except Exception as e:
                self.log(f"❌ Mobile Metro failed: {e}", "MOBILE")
        
        thread = threading.Thread(target=run_metro, daemon=True)
        thread.start()
    
    def open_browser(self):
        """Open browser to the application"""
        time.sleep(5)  # Wait a bit for servers to start
        
        # Try to find the frontend URL
        frontend_urls = [
            "http://localhost:3000",  # New default
            "http://localhost:5173",  # Vite default
            "http://localhost:8080"   # Alternative
        ]
        
        for url in frontend_urls:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.log(f"🌐 Opening browser: {url}", "BROWSER")
                    webbrowser.open(url)
                    return
            except:
                continue
        
        self.log("🌐 Frontend URL not detected, check console output", "BROWSER")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.log("🛑 Shutting down all services...", "SHUTDOWN")
        self.running = False
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        self.log("✅ All services stopped", "SHUTDOWN")
        sys.exit(0)
    
    def show_status(self):
        """Show status of all services"""
        self.log("📊 Service Status:", "STATUS")
        
        services = [
            ("Model API", 8000, "http://localhost:8000/api/health"),
            ("Web Backend", 8001, "http://localhost:8001/api/health"),
            ("Frontend", 3000, "http://localhost:3000"),
            ("Frontend Alt", 5173, "http://localhost:5173")
        ]
        
        for name, port, url in services:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.log(f"✅ {name}: Running on port {port}", "STATUS")
                else:
                    self.log(f"⚠️  {name}: Responding but may have issues", "STATUS")
            except:
                self.log(f"❌ {name}: Not responding on port {port}", "STATUS")
    
    def run(self, include_mobile=False, open_browser_flag=True):
        """Run the full stack application"""
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🏆 DUALITY AI - FULL STACK STARTUP")
        print("=" * 60)
        
        # Check dependencies
        if not self.check_dependencies():
            self.log("❌ Dependency check failed. Please install missing dependencies.", "ERROR")
            return False
        
        # Setup frontend
        if not self.setup_frontend():
            self.log("❌ Frontend setup failed.", "ERROR")
            return False
        
        self.log("🚀 Starting all services...", "STARTUP")
        
        # Start backend services first
        self.start_model_api()
        time.sleep(2)
        
        self.start_web_backend()
        time.sleep(2)
        
        # Start frontend
        self.start_frontend()
        time.sleep(3)
        
        # Optionally start mobile metro
        if include_mobile:
            self.start_mobile_metro()
        
        # Open browser
        if open_browser_flag:
            browser_thread = threading.Thread(target=self.open_browser, daemon=True)
            browser_thread.start()
        
        # Show service URLs
        print("\n" + "=" * 60)
        self.log("🌐 Service URLs:", "INFO")
        self.log("   Frontend:     http://localhost:3000 (or check console)", "INFO")
        self.log("   Model API:    http://localhost:8000/api/health", "INFO")
        self.log("   Web Backend:  http://localhost:8001/api/health", "INFO")
        if include_mobile:
            self.log("   Mobile Metro: http://localhost:8081", "INFO")
        print("=" * 60)
        
        self.log("✅ Full stack application started!", "SUCCESS")
        self.log("Press Ctrl+C to stop all services", "INFO")
        
        # Show status every 30 seconds
        try:
            while self.running:
                time.sleep(30)
                if self.running:
                    self.show_status()
        except KeyboardInterrupt:
            self.signal_handler(None, None)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Start the full DUALITY AI stack")
    parser.add_argument("--mobile", action="store_true", 
                       help="Include React Native Metro bundler")
    parser.add_argument("--no-browser", action="store_true",
                       help="Don't automatically open browser")
    
    args = parser.parse_args()
    
    manager = FullStackManager()
    manager.run(
        include_mobile=args.mobile,
        open_browser_flag=not args.no_browser
    )

if __name__ == "__main__":
    main()