# -*- coding: utf-8 -*-
import qi
import time

session = qi.Session()
session.connect("tcp://nao.local:9559")
cm = session.service("ALConnectionManager")

print("Scanning for Wi-Fi networks...")
try:
    cm.scan("wifi")
    time.sleep(3)
    services = cm.services()
    print("Found {} services:".format(len(services)))
    for s in services:
        d = dict(s)
        if d.get("Type") == "wifi":
            print(" - Wi-Fi: '{}' (Security: {}, Strength: {}%, State: {})".format(
                d.get("Name"), d.get("Security"), d.get("Strength"), d.get("State")
            ))
except Exception as e:
    print("Scan error: {}".format(e))
