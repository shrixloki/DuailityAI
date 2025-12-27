#!/usr/bin/env python3
"""
DUALITY AI - Complete System Startup
Starts the professional frontend and backend services
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path
from datetime import datetime

class DualityAIManager:
    def __init__(self):
        self.processes = []
        self.project_root = Path(__file__).parent
        self.running = True
        
    def log(self, message, component="DUALITY"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {component}: {message}")
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.log("🛑 Shutting down DUALITY AI system...", "SHUTDOWN")
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
        
        self.log("✅ DUALITY AI system stopped", "SHUTDOWN")
        sys.exit(0)
    
    def start_model_api(self):
        """Start the Model API server"""
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
                    if self.running and "Running on" in line:
                        self.log("✅ Model API is ready!", "MODEL-API")
                        break
                        
            except Exception as e:
                self.log(f"❌ Model API failed: {e}", "MODEL-API")
        
        thread = threading.Thread(target=run_model_api, daemon=True)
        thread.start()
        time.sleep(3)  # Give it time to start
    
    def start_frontend(self):
        """Start the React frontend"""
        self.log("🌐 Starting Professional Frontend (Port 3000)...", "FRONTEND")
        
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
                
                # Monitor output
                for line in iter(process.stdout.readline, ''):
                    if self.running and "Local:" in line and "http://" in line:
                        url = line.split("http://")[1].split()[0]
                        self.log(f"✅ Frontend ready at: http://{url}", "FRONTEND")
                        break
                        
            except Exception as e:
                self.log(f"❌ Frontend failed: {e}", "FRONTEND")
        
        thread = threading.Thread(target=run_frontend, daemon=True)
        thread.start()
        time.sleep(3)  # Give it time to start
    
    def run(self):
        """Run the complete DUALITY AI system"""
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🛡️  DUALITY AI - PROFESSIONAL SYSTEM STARTUP")
        print("=" * 60)
        self.log("Visual Inference System for Target Assessment", "INFO")
        print("=" * 60)
        
        # Start services
        self.start_model_api()
        self.start_frontend()
        
        # Show service information
        print("\n" + "🌟" * 60)
        self.log("🎯 DUALITY AI SYSTEM READY!", "SUCCESS")
        print("🌟" * 60)
        
        self.log("🌐 Professional Frontend: http://localhost:3000", "INFO")
        self.log("🤖 Model API:             http://localhost:8000", "INFO")
        self.log("📊 Health Check:          http://localhost:8000/api/health", "INFO")
        
        print("\n" + "📋 FEATURES:")
        self.log("   ✅ Professional UI with gradient design", "FEATURE")
        self.log("   ✅ Real-time model performance metrics", "FEATURE")
        self.log("   ✅ Interactive confidence threshold", "FEATURE")
        self.log("   ✅ Drag & drop image upload", "FEATURE")
        self.log("   ✅ Visual detection results", "FEATURE")
        self.log("   ✅ 7 safety equipment classes", "FEATURE")
        self.log("   ✅ Multiple model selection", "FEATURE")
        
        print("\n" + "🎯 DETECTION CLASSES:")
        classes = [
            "🔥 FireExtinguisher", "📞 EmergencyPhone", "🚨 FireAlarm",
            "🩹 FirstAidBox", "💨 NitrogenTank", "💨 OxygenTank", "⚡ SafetySwitchPanel"
        ]
        for cls in classes:
            self.log(f"   {cls}", "CLASS")
        
        print("\n" + "=" * 60)
        self.log("Press Ctrl+C to stop the system", "INFO")
        print("=" * 60)
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(None, None)

def main():
    manager = DualityAIManager()
    manager.run()

if __name__ == "__main__":
    main()