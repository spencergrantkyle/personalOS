# logging_server.py
from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)
LOGS = []  # In-memory log, newest last

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Automation Server</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; }
    h1 { color: #2c3e50; }
    .log-entry { padding: 6px; border-bottom: 1px solid #ddd; }
    .time { color: #888; font-size: 0.9em; }
    pre { background: #f4f4f4; padding: 6px; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Automation Server Status</h1>
  <p>✅ Listening for requests on <code>/trigger</code></p>
  <h2>Recent Requests</h2>
  {% for entry in logs %}
    <div class="log-entry">
      <div class="time">{{ entry['time'] }}</div>
      <pre>{{ entry['data'] }}</pre>
    </div>
  {% else %}
    <p>No requests received yet.</p>
  {% endfor %}
</body>
</html>
"""

@app.route("/")
def home():
    # Show last 20 logs
    return render_template_string(HTML_PAGE, logs=LOGS[-20:])

@app.route("/trigger", methods=["POST", "GET"])
def trigger():
    data = request.get_json(force=True, silent=True) or request.args or {}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOGS.append({"time": timestamp, "data": data})
    print(f"[{timestamp}] Received: {data}")  # Log to console too
    return jsonify({"status": "logged", "received": data, "at": timestamp})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)