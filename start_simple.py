#!/usr/bin/env python3
"""
Simple Full Stack Startup - Bypasses dependency checks
Use this if the main script has issues with npm detection
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path
from datetime import datetime

class SimpleStackManager:
    def __init__(self):
        self.processes = []
        self.project_root = Path(__file__).parent
        self.running = True
        
    def log(self, message, component="MAIN"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {component}: {message}")
    
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
    
    def start_model_api(self):
        """Start the main model API server"""
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
    
    def start_web_backend(self):
        """Start the web application backend"""
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
    
    def start_frontend(self):
        """Start the React frontend development server"""
        self.log("🚀 Starting Frontend Development Server...", "FRONTEND")
        
        def run_frontend():
            try:
                frontend_dir = self.project_root / "Web_App_frontend"
                os.chdir(frontend_dir)
                
                # Check if node_modules exists
                if not (frontend_dir / "node_modules").exists():
                    self.log("📦 Installing frontend dependencies...", "FRONTEND")
                    subprocess.run(["npm", "install"], check=True)
                
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
    
    def run(self):
        """Run the full stack application"""
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🚀 DUALITY AI - Simple Full Stack Startup")
        print("=" * 60)
        
        self.log("🚀 Starting all services...", "STARTUP")
        
        # Start backend services first
        self.start_model_api()
        time.sleep(3)
        
        self.start_web_backend()
        time.sleep(2)
        
        # Start frontend
        self.start_frontend()
        time.sleep(3)
        
        # Show service URLs
        print("\n" + "=" * 60)
        self.log("🌐 Service URLs:", "INFO")
        self.log("   Frontend:     http://localhost:3000 (or check console)", "INFO")
        self.log("   Model API:    http://localhost:8000/api/health", "INFO")
        self.log("   Web Backend:  http://localhost:8001/api/health", "INFO")
        print("=" * 60)
        
        self.log("✅ Full stack application started!", "SUCCESS")
        self.log("Press Ctrl+C to stop all services", "INFO")
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(None, None)

def main():
    manager = SimpleStackManager()
    manager.run()

if __name__ == "__main__":
    main()