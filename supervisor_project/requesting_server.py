import requests
import time
import threading
from datetime import datetime

SUPERVISOR_URL = "http://localhost:5000"
API_KEY = "secure-key-123"  # Should match one of the keys in supervisor

class MachineMonitor:
    def __init__(self):
        self.monitored_machine = None
        self.monitoring_active = False
        self.available_machines = ["M1", "M2", "M3", "M4", "M5", 
                                  "M6", "M7", "M8", "M9", "M10"]

    def get_machine_data(self, machine_id):
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{SUPERVISOR_URL}/api/machines/{machine_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[{datetime.now()}] Error fetching {machine_id}: {response.text}")
                return None
                
        except Exception as e:
            print(f"[{datetime.now()}] Connection error: {str(e)}")
            return None

    def monitor_machine(self, interval=2):
        """Continuously monitor the selected machine"""
        while self.monitoring_active:
            data = self.get_machine_data(self.monitored_machine)
            if data:
                print(f"\n[{datetime.now()}] {self.monitored_machine} Status:")
                print(f"  Status: {data['status']}")
                print(f"  Temperature: {data['temperature']}")
                print(f"  Pressure: {data['pressure']}")
            else:
                print(f"\n[{datetime.now()}] Could not retrieve data for {self.monitored_machine}")
            
            time.sleep(interval)

    def start_monitoring(self, machine_id):
        """Start monitoring a specific machine"""
        if machine_id.upper() in self.available_machines:
            if self.monitoring_active:
                self.stop_monitoring()
            
            self.monitored_machine = machine_id.upper()
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(
                target=self.monitor_machine,
                daemon=True
            )
            self.monitor_thread.start()
            print(f"\nStarted continuous monitoring for {self.monitored_machine}")
        else:
            print(f"Error: {machine_id} is not a valid machine ID")

    def stop_monitoring(self):
        """Stop the current monitoring"""
        if self.monitoring_active:
            self.monitoring_active = False
            self.monitor_thread.join()
            print(f"\nStopped monitoring {self.monitored_machine}")
            self.monitored_machine = None

    def user_interface(self):
        """Handle user commands"""
        print("\nMachine Monitoring System")
        print("Available machines:", ", ".join(self.available_machines))
        print("\nAvailable commands:")
        print("  'monitor <machine_id>' - Continuously monitor a specific machine")
        print("  'stop' - Stop current monitoring")
        print("  'exit' - Quit the program")
        
        while True:
            user_input = input("\nEnter command: ").strip().lower()
            
            if user_input == 'exit':
                if self.monitoring_active:
                    self.stop_monitoring()
                print("Exiting program...")
                break
            elif user_input == 'stop':
                if self.monitoring_active:
                    self.stop_monitoring()
                else:
                    print("No active monitoring to stop")
            elif user_input.startswith('monitor '):
                machine_id = user_input[8:].upper()
                self.start_monitoring(machine_id)
            else:
                print("Invalid command. Try 'monitor <machine_id>', 'stop', or 'exit'")

if __name__ == '__main__':
    monitor = MachineMonitor()
    monitor.user_interface()