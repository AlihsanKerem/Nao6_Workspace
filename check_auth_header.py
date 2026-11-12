import urllib.request
import urllib.error

url = "http://169.254.46.177/libs/qimessaging/2/qimessaging.js"
try:
    urllib.request.urlopen(url, timeout=3)
except urllib.error.HTTPError as e:
    print("Code:", e.code)
    print("Headers:", dict(e.headers))
