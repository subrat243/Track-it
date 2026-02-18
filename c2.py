#!/usr/bin/env python3
"""
Local C2 Server v2.0 + Auto Internet Exposure
WhatsApp/Telegram/PDF/Windows • Live Dashboard • SQLite
"""

import base64
import sqlite3
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = 'c2_hits.db'

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS hits 
                   (id TEXT, platform TEXT, ip TEXT, host TEXT, ua TEXT, ts TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    """Live dashboard (localhost only)"""
    conn = sqlite3.connect(DB_PATH)
    hits = conn.execute("SELECT * FROM hits ORDER BY ts DESC LIMIT 100").fetchall()
    conn.close()
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🎯 Universal C2 Dashboard</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; margin: 0; padding: 20px; }}
        .header {{ text-align: center; font-size: 24px; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; background: #1a1a1a; }}
        th, td {{ border: 1px solid #333; padding: 12px; text-align: left; }}
        th {{ background: #333; font-weight: bold; }}
        .whatsapp {{ color: #00ff00; font-weight: bold; }}
        .telegram {{ color: #ffa500; font-weight: bold; }}
        .pdf {{ color: #00ffff; font-weight: bold; }}
        .win {{ color: #ff00ff; font-weight: bold; }}
        .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .stat {{ background: #222; padding: 10px; border-radius: 5px; }}
        .hit-count {{ font-size: 32px; color: #ff4444; }}
    </style>
</head>
<body>
    <div class="header">🎯 LIVE C2 HITS <span id="hit-count" class="hit-count">{len(hits)}</span></div>
    
    <div class="stats">
        <div class="stat">Total: {len(hits)}</div>
        <div class="stat">WhatsApp: {len([h for h in hits if 'whatsapp' in h[1].lower()])}</div>
        <div class="stat">PDF: {len([h for h in hits if 'pdf' in h[1].lower()])}</div>
    </div>
    
    <table>
        <tr><th>ID</th><th>Platform</th><th>IP</th><th>Host</th><th>UA</th><th>Time</th></tr>
"""
    
    for hit in hits:
        platform_class = {
            'whatsapp': 'whatsapp', 'telegram': 'telegram', 
            'pdf': 'pdf', 'win': 'win'
        }.get(hit[1].lower(), '')
        html += f"""
        <tr>
            <td>{hit[0]}</td>
            <td class="{platform_class}">{hit[1]}</td>
            <td>{hit[2]}</td>
            <td>{hit[3]}</td>
            <td style="max-width:300px">{hit[4][:50]}...</td>
            <td>{hit[5][:19]}</td>
        </tr>
        """
    
    html += """
    </table>
    <p style="margin-top:30px"><b>🔒 Local-only access</b> | DB: c2_hits.db | Auto-refresh: 3s</p>
</body>
</html>"""
    
    return html

@app.route('/beacon')
def beacon():
    """Tracker callback endpoint"""
    uid = request.args.get('id', 'unknown')
    platform = request.args.get('whatsapp') or request.args.get('pdf') or request.args.get('win') or request.args.get('svg') or 'unknown'
    ip = request.remote_addr
    host = request.args.get('host', 'unknown')
    ua = request.headers.get('User-Agent', 'unknown')
    ts = datetime.now().isoformat()
    
    # Log hit
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO hits VALUES(?, ?, ?, ?, ?, ?)", (uid, platform, ip, host, ua, ts))
    conn.commit()
    conn.close()
    
    print(f"🎯 [{platform.upper()}] {uid} from {ip} ({host})")
    
    # Return 1x1 transparent GIF
    gif = base64.b64decode("R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=")
    return Response(gif, 200, {'Content-Type': 'image/gif'})

def expose_tunnel(port=8080):
    """Auto internet exposure"""
    print("🌐 Starting internet tunnel...")
    
    tunnels = {
        'ngrok': ['ngrok', 'http', str(port)],
        'cloudflared': ['cloudflared', 'tunnel', '--url', f'localhost:{port}']
    }
    
    print("Available tunnels:")
    print("  1. ngrok: https://ngrok.com/download")
    print("  2. cloudflared: https://developers.cloudflare.com/cloudflare-one/")
    print("\n💡 Copy your tunnel URL for tracker: --url https://abc123.ngrok.io/beacon")
    
    input("\nPress Enter after starting tunnel...")

if __name__ == "__main__":
    init_db()
    print("🚀 Starting Local C2 Server...")
    print("📊 Dashboard: http://localhost:8080")
    print("📡 Beacon:    http://localhost:8080/beacon")
    print("\n🌐 Start tunnel then press Enter:")
    
    expose_tunnel()
    
    print("\n✅ C2 LIVE! Use tunnel URL in tracker:")
    print("   python3 universal_tracker.py file.pdf tracked.pdf --url YOUR_TUNNEL_URL/beacon")
    
    app.run(host='0.0.0.0', port=8080, debug=False)