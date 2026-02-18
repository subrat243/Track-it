#!/bin/bash
# Track-it 1-Click Deploy

echo "🎯 Track-it Deployer"
echo "======================================="

# Create directories
mkdir -p data/tracked_files tunnels

# Create tunnel configs
if [ ! -f "tunnels/ngrok.yml" ]; then
  cat > tunnels/ngrok.yml << 'EOF'
version: "2"
authtoken: YOUR_NGROK_AUTHTOKEN_HERE
tunnels:
  tracker:
    addr: 8080
    proto: http
EOF
fi

if [ ! -f "tunnels/cloudflare.json" ]; then
  cat > tunnels/cloudflare.json << 'EOF'
{
  "tunnel": "tracker-ID-FROM-cloudflared",
  "credentials-file": "/root/.cloudflared/YOUR_CREDENTIALS.json",
  "ingress": [
    {"hostname": "tracker.yourdomain.com", "service": "http://localhost:8080"},
    {"service": "http_status:404"}
  ]
}
EOF
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create sample files
echo "📄 Creating test files..."
echo "Sample invoice content" > data/test_invoice.pdf.txt
echo '<html><body>Test HTML</body></html>' > data/test.html

# Start C2
echo "🚀 Starting Local C2 Server..."
echo "🌐 Open http://localhost:8080 after tunnel setup"
python3 c2.py &

# Wait for C2
sleep 3

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Start tunnel: ngrok http 8080  (or: ngrok start tracker  if using tunnels/ngrok.yml)"
echo "2. Track: python3 track-it.py data/test.html tracked.html --url https://YOUR_NGROK_URL/beacon"
echo "3. Dashboard: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop C2"
wait