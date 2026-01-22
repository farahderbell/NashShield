#!/usr/bin/env python
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print(f"Python: {sys.executable}")
print(f"Working dir: {os.getcwd()}")

try:
    from backend.app import app
    print("✓ App loaded successfully")
    print(f"Starting Flask server on http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
