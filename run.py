#!/usr/bin/env python3
"""
Simple Flask runner for NashShield with Real Quota-Share Formula
"""
import os
import sys
import webbrowser
from time import sleep

# Add project to path
sys.path.insert(0, r'c:\Users\User1\NashShield')

# Import and run app
from backend.app import app

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🛡️  NASHIELD - Real Quota-Share Insurance Simulation")
    print("="*70)
    print("\n📍 Starting Flask server...")
    print("🌐 URL: http://127.0.0.1:5001")
    print("\n💡 Real Formula: Profit = Retention × (Premium - Claims)")
    print("="*70 + "\n")
    
    # Start Flask
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=False,
        use_reloader=False
    )
