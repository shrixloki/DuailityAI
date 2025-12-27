#!/usr/bin/env python3
"""
Simple API test with minimal dependencies
"""

import urllib.request
import json

def test_health():
    try:
        print("🔍 Testing API health...")
        req = urllib.request.Request('http://localhost:8000/api/health')
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            print("✅ Health check successful:", data)
            return True
    except Exception as e:
        print("❌ Health check failed:", e)
        return False

def test_models():
    try:
        print("🔍 Testing models endpoint...")
        req = urllib.request.Request('http://localhost:8000/api/models')
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            print("✅ Models endpoint successful")
            print(f"Found {len(data['models'])} models")
            for model in data['models']:
                print(f"  - {model['name']}: {'✅' if model['available'] else '❌'}")
            return True
    except Exception as e:
        print("❌ Models test failed:", e)
        return False

if __name__ == "__main__":
    print("🛡️ DUALITY AI - Simple API Test")
    print("=" * 40)
    
    if test_health():
        test_models()
    else:
        print("❌ API is not responding")