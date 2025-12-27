#!/usr/bin/env python3
"""
Setup Validation Script
Checks if the environment is ready for full-stack startup
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_deps():
    """Check Python dependencies"""
    print("🐍 Checking Python Dependencies...")
    
    deps = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('ultralytics', 'Ultralytics YOLO'),
        ('PIL', 'Pillow'),
        ('torch', 'PyTorch'),
        ('numpy', 'NumPy'),
        ('requests', 'Requests')
    ]
    
    missing = []
    for module, name in deps:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - MISSING")
            missing.append(name)
    
    if missing:
        print(f"\n📦 Install missing packages:")
        print(f"   pip install {' '.join([dep[0] for dep in deps if dep[1] in missing])}")
        return False
    
    return True

def check_nodejs():
    """Check Node.js and npm"""
    print("\n📦 Checking Node.js...")
    
    node_ok = False
    npm_ok = False
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        node_version = result.stdout.strip()
        print(f"  ✅ Node.js {node_version}")
        node_ok = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  ❌ Node.js not found")
    
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
        npm_version = result.stdout.strip()
        print(f"  ✅ npm {npm_version}")
        npm_ok = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  ❌ npm not found")
    
    if not (node_ok and npm_ok):
        print("     Install from: https://nodejs.org/")
        return False
    
    return True

def check_project_structure():
    """Check project structure"""
    print("\n📁 Checking Project Structure...")
    
    required_paths = [
        "src/model_api.py",
        "app/backend.py", 
        "Web_App_frontend/package.json",
        "models/weights"
    ]
    
    project_root = Path(__file__).parent
    all_good = True
    
    for path in required_paths:
        full_path = project_root / path
        if full_path.exists():
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path} - MISSING")
            all_good = False
    
    return all_good

def check_models():
    """Check model files"""
    print("\n🤖 Checking Model Files...")
    
    model_paths = [
        "models/weights/FINAL_SELECTED_MODEL.pt",
        "models/weights/best.pt"
    ]
    
    project_root = Path(__file__).parent
    found_models = 0
    
    for model_path in model_paths:
        full_path = project_root / model_path
        if full_path.exists():
            size_mb = full_path.stat().st_size / (1024 * 1024)
            print(f"  ✅ {model_path} ({size_mb:.1f} MB)")
            found_models += 1
        else:
            print(f"  ⚠️  {model_path} - Not found")
    
    if found_models == 0:
        print("  ❌ No model files found. Train models first or download weights.")
        return False
    
    return True

def check_frontend_deps():
    """Check frontend dependencies"""
    print("\n🌐 Checking Frontend Dependencies...")
    
    frontend_dir = Path(__file__).parent / "Web_App_frontend"
    node_modules = frontend_dir / "node_modules"
    
    if node_modules.exists():
        print("  ✅ Frontend dependencies installed")
        return True
    else:
        print("  ⚠️  Frontend dependencies not installed")
        print("     Run: cd Web_App_frontend && npm install")
        return False

def main():
    print("🔍 DUALITY AI - Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Dependencies", check_python_deps),
        ("Node.js Environment", check_nodejs),
        ("Project Structure", check_project_structure),
        ("Model Files", check_models),
        ("Frontend Dependencies", check_frontend_deps)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Error checking {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("   Ready to run: python run_full_stack.py")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("   Fix the issues above before starting the application")
    
    print("=" * 50)
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)