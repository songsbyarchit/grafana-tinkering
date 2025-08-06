from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import threading
import time
import requests

app = Flask(__name__)

# Define a metric: count total HTTP requests to "/"
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()  # Increment every time this route is hit
    return "Hello from Render!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

def simulate_traffic():
    base_url = "https://grafana-tinkering.onrender.com"

    # Spike: 200 requests over 1 minute
    for i in range(200):
        threading.Thread(target=requests.get, args=(base_url,)).start()
        time.sleep(0.3)  # Adjust for spike density

    # Sustain: small spikes every 30s for 10 mins
    for _ in range(20):
        for _ in range(10):  # 10 mini-requests
            threading.Thread(target=requests.get, args=(base_url,)).start()
        time.sleep(30)

# Start traffic in background
threading.Thread(target=simulate_traffic).start()
