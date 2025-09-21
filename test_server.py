#!/usr/bin/env python3
"""
Simple test script to verify server functionality
"""
import requests
import json
import time
import subprocess
import sys
import os

def test_local_server():
    """Test the server running on localhost:5000"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing local server...")
    
    # Test 1: Home page
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Home page: {response.status_code}")
        if "Automation Server Status" in response.text:
            print("   📄 Status page loaded correctly")
    except Exception as e:
        print(f"❌ Home page failed: {e}")
        return False
    
    # Test 2: GET request to /trigger
    try:
        response = requests.get(f"{base_url}/trigger?test=hello&method=GET")
        print(f"✅ GET /trigger: {response.status_code}")
        data = response.json()
        print(f"   📦 Response: {data}")
    except Exception as e:
        print(f"❌ GET /trigger failed: {e}")
        return False
    
    # Test 3: POST request to /trigger
    try:
        test_data = {"test": "post_request", "timestamp": time.time()}
        response = requests.post(f"{base_url}/trigger", json=test_data)
        print(f"✅ POST /trigger: {response.status_code}")
        data = response.json()
        print(f"   📦 Response: {data}")
    except Exception as e:
        print(f"❌ POST /trigger failed: {e}")
        return False
    
    print("\n🎉 All local tests passed!")
    return True

def test_ngrok_server(ngrok_url):
    """Test the server through ngrok URL"""
    print(f"\n🌐 Testing ngrok URL: {ngrok_url}")
    
    # Test 1: Home page through ngrok
    try:
        response = requests.get(f"{ngrok_url}/")
        print(f"✅ Ngrok home page: {response.status_code}")
        if "Automation Server Status" in response.text:
            print("   📄 Status page loaded correctly through ngrok")
    except Exception as e:
        print(f"❌ Ngrok home page failed: {e}")
        return False
    
    # Test 2: POST request through ngrok
    try:
        test_data = {"test": "ngrok_request", "timestamp": time.time()}
        response = requests.post(f"{ngrok_url}/trigger", json=test_data)
        print(f"✅ Ngrok POST /trigger: {response.status_code}")
        data = response.json()
        print(f"   📦 Response: {data}")
    except Exception as e:
        print(f"❌ Ngrok POST /trigger failed: {e}")
        return False
    
    print("\n🎉 All ngrok tests passed!")
    return True

def start_server():
    """Start the server in background"""
    print("🚀 Starting server...")
    try:
        # Start server in background
        process = subprocess.Popen([sys.executable, 'server.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        print("✅ Server started in background")
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def wait_for_server(max_attempts=10):
    """Wait for server to be ready"""
    print("⏳ Waiting for server to be ready...")
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:5000/", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"   Attempt {i+1}/{max_attempts}...")
    return False

if __name__ == "__main__":
    print("🚀 Server Testing Script")
    print("=" * 40)
    
    # Start server if not already running
    server_process = None
    try:
        # Try to connect first
        response = requests.get("http://localhost:5000/", timeout=2)
        print("✅ Server already running")
    except:
        # Start server
        server_process = start_server()
        if not server_process or not wait_for_server():
            print("❌ Failed to start server")
            sys.exit(1)
    
    # Test local server
    if test_local_server():
        print("\n" + "=" * 40)
        print("📋 Next steps:")
        print("1. Start ngrok: ngrok http 5000")
        print("2. Run this script with ngrok URL: python test_server.py <ngrok_url>")
    else:
        print("\n❌ Local server tests failed. Please check your server setup.")
    
    # If ngrok URL provided, test it
    if len(sys.argv) > 1:
        ngrok_url = sys.argv[1]
        test_ngrok_server(ngrok_url)
    
    # Clean up
    if server_process:
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()
