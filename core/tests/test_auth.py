import urllib.request
import base64

url = "http://169.254.46.177/libs/qimessaging/2/qimessaging.js"
req = urllib.request.Request(url)
auth = base64.b64encode(b"nao:nao").decode('ascii')
req.add_header("Authorization", f"Basic {auth}")

try:
    resp = urllib.request.urlopen(req, timeout=3)
    print("Basic auth nao:nao SUCCESS! Status:", resp.status)
    content = resp.read(500)
    print("Content preview:", content[:100])
except Exception as e:
    print("Basic auth nao:nao failed:", e)
