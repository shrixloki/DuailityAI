#!/usr/bin/env python3
"""
Quick API test to check if the server is responding
"""

import requests
import time

def test_api():
    print("🔍 Testing API connectivity...")
    
    try:
        # Test health endpoint
        response = requests.get('http://localhost:8000/api/health', timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ API is responding")
            data = response.json()
            print(f"Status: {data.get('status')}")
        else:
            print("❌ API returned error")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API - server may be down")
    except requests.exceptions.Timeout:
        print("❌ API request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()