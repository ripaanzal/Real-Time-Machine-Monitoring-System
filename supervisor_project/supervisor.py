from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import os
from functools import wraps

app = Flask(__name__)
machine_data_store = {}
LOG_FILE = "machine_logs.jsonl"

# Simple API key authentication (for production use a proper auth system)
API_KEYS = {
    "monitoring-server-1": "secure-key-123",
    "analytics-server": "secure-key-456"
}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key not in API_KEYS.values():
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Load machine_data_store from file if exists
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                machine_id = data.get("machine_id")
                if machine_id:
                    machine_data_store[machine_id] = data
            except json.JSONDecodeError:
                continue

@app.route('/upload', methods=['POST'])
def receive_data():
    data = request.get_json()
    machine_id = data.get('machine_id')
    if not machine_id:
        return jsonify({"error": "machine_id missing"}), 400

    data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    machine_data_store[machine_id] = data

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    return jsonify({"message": f"Data received from {machine_id}"}), 200

@app.route('/machine/<machine_id>')
def get_machine_data(machine_id):
    data = machine_data_store.get(machine_id)
    if not data:
        return jsonify({"error": "No data for this machine"}), 404
    return jsonify(data), 200

@app.route('/history/<machine_id>')
def get_history(machine_id):
    history = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if data.get("machine_id") == machine_id:
                        history.append({
                            "timestamp": data.get("timestamp"),
                            "temperature": data.get("temperature"),
                            "pressure": data.get("pressure"),
                        })
                except:
                    continue
    return jsonify(history)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", machines=machine_data_store)

# This should appear in your routes (usually near other @app.route definitions)
@app.route('/api/machines/<machine_id>', methods=['GET'])
@require_api_key
def get_machine_details(machine_id):
    data = machine_data_store.get(machine_id)
    if not data:
        return jsonify({"error": "Machine not found"}), 404
    
    response = {
        "machine_id": machine_id,
        "status": data.get("status"),
        "temperature": data.get("temperature"),
        "pressure": data.get("pressure"),
        "last_updated": data.get("timestamp")
    }
    return jsonify(response)

@app.route('/trend')
def trend_monitor():
    return render_template("trend.html", machines=machine_data_store)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)