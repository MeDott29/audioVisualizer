from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def guess_type(self, path):
        if path.endswith('.wav'):
            return 'audio/wav'
        return SimpleHTTPRequestHandler.guess_type(self, path)

# Set up the server
port = 8001
handler = CORSRequestHandler
server = HTTPServer(('0.0.0.0', port), handler)
print(f'Serving at http://localhost:{port}')
server.serve_forever()