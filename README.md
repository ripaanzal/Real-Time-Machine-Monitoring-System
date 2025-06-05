Real-Time Machine Monitoring System

A full-stack simulation and monitoring system that generates live machine data, collects it through a Flask-based supervisor server, and visualizes it via an interactive web dashboard and trend analytics. Also includes a secure API and command-line monitor client.

📂 Project Structure
├── machines.py             # Simulates 10 machines sending data
├── supervisor.py           # Flask backend to receive, store & serve data
├── requesting_server.py    # CLI tool to monitor any machine with API key
├── dashboard.html          # HTML dashboard for live machine status
├── trend.html              # HTML trend plot for temperature & pressure
├── machine_logs.jsonl      # JSONL log of all machine data
├── test_connection.py      # Script to test server API & auth

🚀 Features
- Simulates 10 machines sending random data every 3–6 seconds.
- Real-time data ingestion and storage via Flask.
- API key–protected monitoring interface for secure data access.
- Web dashboards for:
  Live machine status with auto-refresh.
  Temperature & pressure trends via Chart.js.
- Command-line tool for real-time machine monitoring.
- Historical logging in JSONL format.

📦 Requirements
- Python 3.7+
- Flask
- requests

🔧 Getting Started
1. Start the Supervisor Server
    python supervisor.py
Accessible at:
  - Dashboard: http://localhost:5000/dashboard
  - Trends: http://localhost:5000/trend

2. Start the Machine Simulator
    python machines.py
Simulates 10 machines (M1 to M10) sending data continuously.

3. Use the CLI Monitoring Tool
    python requesting_server.py
Then use commands:
  - monitor M1 — start monitoring a machine
  - stop — stop monitoring
  - exit — quit the CLI

4. Optional: Test the API
    python test_connection.py

📊 Dashboard & Trend Views
  - dashboard.html: Real-time status of all machines.
  - trend.html: Select a machine to view temperature & pressure trends.
  Powered by Chart.js.
