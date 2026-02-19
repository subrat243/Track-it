#!/usr/bin/env python3
"""
Beacon Link Generator v2.0
Generate tracking links with custom header/ID
Usage: python3 beacon.py --url https://tunnel/beacon --header meesho_supplier
"""

import argparse
import hashlib
import os
from datetime import datetime

def generate_beacon_link(base_url, header=""):
    """Generate tracking beacon with header/ID"""
    timestamp = str(int(datetime.now().timestamp()))
    uid = hashlib.md5((header + timestamp + str(os.urandom(8))).encode()).hexdigest()[:10]
    beacon_url = f"{base_url.rstrip('/')}/beacon?id={uid}&header={header}"
    
    print("\n" + "="*50)
    print("🎯 BEACON LINK READY")
    print("="*50)
    print(f"🔗 LINK: {beacon_url}")
    print(f"🆔 ID:   {uid}")
    print(f"📝 Header: {header}")
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate C2 Beacon Link")
    parser.add_argument("--url", "-u", required=True, help="Tunnel URL (https://abc.ngrok.io)")
    parser.add_argument("--header", "-h", default="", help="Tracker header/label (e.g. 'meesho_supplier')")
    args = parser.parse_args()
    
    generate_beacon_link(args.url, args.header)