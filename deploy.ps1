# Track-it  Windows Deployer
Write-Host "🎯 Track-it (Windows)" -ForegroundColor Green

# Create directories
New-Item -ItemType Directory -Force -Path "data\tracked_files" | Out-Null
New-Item -ItemType Directory -Force -Path "tunnels" | Out-Null

# Create tunnel configs if missing
$ngrokPath = "tunnels\ngrok.yml"
if (-not (Test-Path $ngrokPath)) {
@"
version: "2"
authtoken: YOUR_NGROK_AUTHTOKEN_HERE
tunnels:
  tracker:
    addr: 8080
    proto: http
"@ | Out-File -FilePath $ngrokPath -Encoding utf8
}

$cloudflarePath = "tunnels\cloudflare.json"
if (-not (Test-Path $cloudflarePath)) {
@"
{
  "tunnel": "tracker-ID-FROM-cloudflared",
  "credentials-file": "/root/.cloudflared/YOUR_CREDENTIALS.json",
  "ingress": [
    {"hostname": "tracker.yourdomain.com", "service": "http://localhost:8080"},
    {"service": "http_status:404"}
  ]
}
"@ | Out-File -FilePath $cloudflarePath -Encoding utf8
}

# Install dependencies
pip3 install -r requirements.txt

# Create test files
"Sample invoice content" | Out-File -FilePath "data\test_invoice.txt" -Encoding utf8
@"
<html><body>Test HTML for preview tracking</body></html>
"@ | Out-File -FilePath "data\test.html" -Encoding utf8

Write-Host "🚀 Starting Local C2 Server..." -ForegroundColor Yellow
Write-Host "🌐 Open http://localhost:8080 after tunnel setup" -ForegroundColor Cyan

# Start C2
Start-Process python -ArgumentList "c2.py" -NoNewWindow

Start-Sleep 3
Write-Host "`n✅ Deployment Complete!" -ForegroundColor Green
Write-Host "`n📋 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Download ngrok: https://ngrok.com/download"
Write-Host "2. Run: ngrok http 8080  (or: ngrok start tracker  if using tunnels/ngrok.yml)"
Write-Host "3. Track: python track-it.py data\test.html tracked.html --url https://YOUR_NGROK_URL/beacon"
Write-Host "4. Dashboard: http://localhost:8080"