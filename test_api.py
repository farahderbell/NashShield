import requests
import time

time.sleep(1)
print("Testing API...")
try:
    r = requests.post('http://127.0.0.1:5001/simulate', json={'qA':0.2,'qB':0.2,'qC':0.2,'scenario':'classic'}, timeout=30)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
