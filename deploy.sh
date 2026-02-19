#!/bin/bash
# Track-it 1-Click Deploy

echo "🎯 Track-it Deployer"
echo "======================================="

# Create directories
mkdir -p data tunnels

# Create tunnel configs
if [ ! -f "tunnels/ngrok.yml" ]; then
  cat > tunnels/ngrok.yml << 'EOF'
version: "2"
authtoken: YOUR_NGROK_AUTHTOKEN_HERE
tunnels:
  tracker:
    addr: 4444
    proto: http
EOF
fi

if [ ! -f "tunnels/cloudflare.json" ]; then
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
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages

# Start C2
echo "🚀 Starting Local C2 Server..."
echo "🌐 Open http://localhost:4444 after tunnel setup"
python3 c2.py &

# Wait for C2
sleep 3

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Start tunnel: ngrok http 4444  (or: ngrok start tracker  if using tunnels/ngrok.yml)"
echo "2. Track: python3 track-it.py --url https://abc.ngrok.io --header 'identifier'"
echo "3. Dashboard: http://localhost:4444"
echo ""
echo "Press Ctrl+C to stop C2"
wait