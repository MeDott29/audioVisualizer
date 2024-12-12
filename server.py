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
        # Add proper MIME types for media files
        if path.endswith('.wav'):
            return 'audio/wav'
        elif path.endswith('.mp4'):
            return 'video/mp4'
        # Add support for partial content (important for video streaming)
        elif path.endswith('.m4v'):
            return 'video/mp4'
        return SimpleHTTPRequestHandler.guess_type(self, path)

    def do_GET(self):
        # Handle range requests for video streaming
        try:
            # Get file size
            path = self.translate_path(self.path)
            if os.path.isfile(path):
                file_size = os.path.getsize(path)
                
                # Check for Range header
                range_header = self.headers.get('Range')
                if range_header:
                    # Parse range header
                    try:
                        range_match = range_header.replace('bytes=', '').split('-')
                        range_start = int(range_match[0])
                        range_end = int(range_match[1]) if range_match[1] else file_size - 1
                    except (ValueError, IndexError):
                        self.send_error(400, "Invalid range header")
                        return

                    # Send partial content
                    self.send_response(206)
                    self.send_header('Content-Range', f'bytes {range_start}-{range_end}/{file_size}')
                    self.send_header('Accept-Ranges', 'bytes')
                    self.send_header('Content-Length', str(range_end - range_start + 1))
                    self.send_header('Content-Type', self.guess_type(path))
                    self.end_headers()

                    with open(path, 'rb') as f:
                        f.seek(range_start)
                        self.wfile.write(f.read(range_end - range_start + 1))
                    return

            # If no range header or file doesn't exist, handle normally
            SimpleHTTPRequestHandler.do_GET(self)
            
        except Exception as e:
            self.send_error(500, str(e))

# Set up the server
port = 8001
handler = CORSRequestHandler
server = HTTPServer(('0.0.0.0', port), handler)
print(f'Serving at http://localhost:{port}')
server.serve_forever()