import socket
import urllib.request

ip = "169.254.46.177"

# Check SSH banner
try:
    s = socket.socket()
    s.settimeout(3.0)
    s.connect((ip, 22))
    banner = s.recv(1024)
    print("SSH banner:", banner.decode('utf-8', errors='ignore').strip())
    s.close()
except Exception as e:
    print("SSH banner error:", e)

# Check HTTP 80
try:
    req = urllib.request.urlopen(f"http://{ip}", timeout=3.0)
    print("HTTP 80 status:", req.status)
    print("HTTP 80 headers:", dict(req.getheaders()))
    body = req.read(500)
    print("HTTP 80 body preview:", body[:200])
except Exception as e:
    print("HTTP 80 error:", e)
