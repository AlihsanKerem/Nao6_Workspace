import urllib.request
import re

url = "http://169.254.46.177/"
try:
    resp = urllib.request.urlopen(url, timeout=5)
    content = resp.read().decode('utf-8', errors='ignore')
    print("Page Title/Preview:")
    print(content[:1500])
except Exception as e:
    print("Error:", e)
