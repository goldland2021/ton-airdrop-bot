from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "ok",
            "service": "TON Airdrop Bot",
            "version": "1.0.0",
            "endpoint": self.path,
            "timestamp": "2026-02-19T19:15:00Z"
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            response = {
                "status": "received",
                "message": "Webhook processed",
                "data_received": True
            }
        except:
            response = {
                "status": "error",
                "message": "Invalid JSON"
            }
        
        self.wfile.write(json.dumps(response).encode())
        return