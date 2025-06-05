# machines.py
import requests
import random
import time
import threading

supervisor_url = "http://127.0.0.1:5000/upload"

def generate_data(machine_id):
    return {
        "machine_id": machine_id,
        "temperature": round(random.uniform(60, 100), 2),
        "pressure": round(random.uniform(1000, 1100), 2),
        "status": random.choice(["running", "idle", "error"])
    }

def machine_task(machine_id):
    while True:
        data = generate_data(machine_id)
        try:
            response = requests.post(supervisor_url, json=data)
            print(f"[{machine_id}] Sent data | Response: {response.status_code}")
        except Exception as e:
            print(f"[{machine_id}] Error: {e}")
        time.sleep(random.randint(3, 6))  # Different sleep times

# Launch 10 threads for 10 machines
for i in range(1, 11):
    machine_id = f"M{i}"
    t = threading.Thread(target=machine_task, args=(machine_id,))
    t.daemon = True  # Optional: auto-close when main thread ends
    t.start()

# Keep main thread alive
while True:
    time.sleep(1)
