from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys, os, base64

# CONFIG
SERVE_DIR = os.path.expanduser("~/shared")
USERNAME = ""
PASSWORD = ""

class AuthHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Protected"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def is_authenticated(self):
        auth_header = self.headers.get('Authorization')

        if auth_header is None:
            return False
        
        try:
            method, encoded = auth_header.split(" ", 1)
            if method != "Basic":
                return False

            # Ensure encoded is bytes
            if isinstance(encoded, str):
                encoded_bytes = encoded.encode("utf-8")
            else:
                encoded_bytes = encoded
            
            decoded = base64.b64decode(encoded_bytes).decode("utf-8").strip()

            expected = f"{USERNAME}:{PASSWORD}"  # Replace 'username:password' with your own
            
            # print("Received: ",decoded)
            # print("Expected: ", expected)

            return decoded == expected
        except Exception as e:
            print("ERROR: ",e)
            return False

    def do_GET(self):
        # print("RAW Authorization header: ", self.headers.get("Authorization"))
        if not self.is_authenticated():
            self.do_AUTHHEAD()
            self.wfile.write(b'Authentication required')
            os.chdir(SERVE_DIR) # Ensure server serves the correct directory
            return
        super().do_GET()

    def do_HEAD(self):
        if not self.is_authenticated():
            self.do_AUTHHEAD()
            return
        super().do_HEAD()

if len(sys.argv) < 2:
    print("Usage: python3 serve_auth.py <IP> [PORT]")
    sys.exit(1)

bind_ip = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

httpd = HTTPServer((bind_ip, port), AuthHandler)
print(f"Serving {SERVE_DIR} at http://{bind_ip}:{port} (with auth)")
httpd.serve_forever()
