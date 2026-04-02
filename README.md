# APHFS

## Authenticated Python HTTP File Server

A lightweight Python HTTP server built on top of http.server that serves files from a directory with Basic Authentication protection.

This is useful for quickly sharing files over a network while restricting access with a username and password.

## Features
* Serve static files from a configurable directory
* HTTP Basic Authentication (username & password)
* Minimal dependencies (uses only Python standard library)
* Custom IP and port binding
* Simple and easy to modify

## Requirements
* Python 3.x (no external libraries required)
* (Optional) Ngrok or Cloudflare Tunnel for public access

## Configuration

Edit the following variables in the script:
```bash
SERVE_DIR = os.path.expanduser("~/shared")
USERNAME = ""
PASSWORD = ""
```

### Parameters
| Variable    | Description                   |
| ----------- | ----------------------------- |
| `SERVE_DIR` | Directory to serve files from |
| `USERNAME`  | Username for authentication   |
| `PASSWORD`  | Password for authentication   |

### Important:
You must set USERNAME and PASSWORD before running the server.

## Usage

Run the script from the terminal:
``` bash
python3 serve_auth.py <IP> [PORT]
```

## Authentication

This server uses HTTP Basic Authentication:
* Browser will prompt for username/password
* Credentials are encoded in Base64 (not encrypted)

## Security Warning
* Basic Auth is not secure over HTTP
* Use behind HTTPS or a secure network
* Do NOT expose to the public internet without additional protection

### Arguments
| Argument | Description                                                     |
| -------- | --------------------------------------------------------------- |
| `<IP>`   | IP address to bind the server to (e.g., `127.0.0.1`, `0.0.0.0`) |
| `[PORT]` | Optional port (default: `8000`)                                 |

### Example
```bash
python3 serve_auth.py 0.0.0.0 8080
```
Output:
```diff
Serving /home/user/shared at http://0.0.0.0:8080 (with auth)
```

## How It Works

### Core Components
```diff
AuthHandler
```
Custom request handler that extends:
```python
SimpleHTTPRequestHandler
```
Handles:
* Authentication checks
* GET and HEAD requests

## Authentication Flow
1. Client sends request
2. Server checks Authorization header
3. If missing or invalid:
  * Responds with 401 Unauthorized
  * Prompts for credentials
4. If valid:
  * Serves requested file

## Key Methods
```diff
is_authenticated()
```
* Extracts and decodes credentials
* Compares with configured username/password
```diff
do_AUTHHEAD()
```
* Sends authentication challenge to client
```diff
do_GET() / do_HEAD()
```
* Enforces authentication before serving content

## Directory Serving
The server always serves files from:
```python
SERVE_DIR
```
Even if accessed from different paths, it ensures:
```python
os.chdir(SERVE_DIR)
```

## Testing
### Access via browser:
```diff
http://<IP>:<PORT>
```
You should see a login prompt.

### Access via curl:
```bash
curl -u username:password http://<IP>:<PORT>
```

## Customization Ideas
* Add HTTPS support (e.g., using ssl)
* Logging access attempts
* Rate limiting / brute-force protection
* Multiple user support
* File upload support

## Troubleshooting
### Problem: Authentication not working
* Ensure USERNAME and PASSWORD are set
* Check for whitespace issues
* Verify Base64 decoding errors in logs

### Problem: Files not showing
* Confirm SERVE_DIR exists
* Check permissions
* Ensure correct working directory

## License

This project uses only Python’s standard library and is free to use and modif
