import urllib.request

base = "http://169.254.46.177"
paths = [
    "/libs/qimessaging/2/qimessaging.js",
    "/libs/qimessaging/1.0/qimessaging.js",
    "/js/config.js",
    "/api"
]

for p in paths:
    try:
        url = base + p
        resp = urllib.request.urlopen(url, timeout=3)
        print(f"{p}: status {resp.status}, length {len(resp.read())}")
    except Exception as e:
        print(f"{p}: error {e}")
