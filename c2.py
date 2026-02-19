#!/usr/bin/env python3
"""
Local C2 Server v2.2 - Header + ID Tracking
Custom headers • Live Dashboard • SQLite
Usage: python3 c2.py
Dashboard: http://localhost:4444
"""

import base64
import os
import sqlite3
from datetime import datetime
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_DIR = os.environ.get('DATA_DIR', 'data')
DB_PATH = os.path.join(DATA_DIR, 'c2_hits.db')

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS hits 
                   (id TEXT, header TEXT, ip TEXT, ua TEXT, ts TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    hits = conn.execute("SELECT * FROM hits ORDER BY ts DESC LIMIT 100").fetchall()
    conn.close()
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>C2 Dashboard - Header + ID</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body {{ font-family: 'Courier New'; background: #0a0a0a; color: #00ff00; padding: 20px; }}
        .header {{ text-align: center; font-size: 24px; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; background: #1a1a1a; }}
        th, td {{ border: 1px solid #333; padding: 12px; }}
        th {{ background: #333; }}
        .header-col {{ background: #444; color: #ffaa00; font-weight: bold; }}
        .hit-count {{ color: #ff4444; font-size: 32px; }}
        .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .stat {{ background: #222; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">🎯 LIVE HITS <span class="hit-count">{len(hits)}</span></div>
    <div class="stats">
        <div class="stat">Total: {len(hits)}</div>
        <div class="stat">Unique IDs: {len(set([h[0] for h in hits]))}</div>
    </div>
    <table>
        <tr><th>ID</th><th>HEADER</th><th>IP</th><th>UA</th><th>TIME</th></tr>
"""
    for hit in hits:
        html += f"""
        <tr>
            <td style="color: #00ffff; font-weight: bold;">{hit[0]}</td>
            <td class="header-col">{hit[1] or '-'}</td>
            <td>{hit[2]}</td>
            <td style="max-width:300px">{(hit[3] or '')[:60]}{'...' if len((hit[3] or '')) > 60 else ''}</td>
            <td>{hit[4][:19]}</td>
        </tr>"""
    
    html += "</table><p><b>🔒 Local-only</b> | DB: {DB_PATH}</p></body></html>"
    return html

@app.route('/beacon')
def beacon():
    uid = request.args.get('id', 'unknown')
    header = request.args.get('header', '')
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'unknown')
    ts = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO hits VALUES(?, ?, ?, ?, ?)", (uid, header, ip, ua, ts))
    conn.commit()
    conn.close()
    
    print(f"🎯 [{header or 'LINK'}] ID:{uid} IP:{ip}")
    
    gif = base64.b64decode("R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=")
    return Response(gif, 200, {'Content-Type': 'image/gif'})

if __name__ == "__main__":
    init_db()
    print("🚀 C2 Server v2.2 - Header + ID Tracking")
    print("📊 Dashboard: http://localhost:4444")
    print("🔗 Beacon endpoint: /beacon?id=xxx&header=target")
    print("\n💡 Usage: python3 beacon.py --url https://tunnel/beacon --header meesho")
    app.run(host='0.0.0.0', port=4444, debug=False)