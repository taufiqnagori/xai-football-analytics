"""
Quick script to check if backend is running
"""
import requests
import sys

try:
    response = requests.get("http://127.0.0.1:8000/health", timeout=2)
    if response.status_code == 200:
        print("✅ Backend is running!")
        print(f"Response: {response.json()}")
        sys.exit(0)
    else:
        print(f"❌ Backend returned status code: {response.status_code}")
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print("❌ Backend is NOT running!")
    print("\nTo start the backend, run:")
    print("  uvicorn backend.main:app --reload")
    print("\nOr double-click: run_backend.bat")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error checking backend: {e}")
    sys.exit(1)
