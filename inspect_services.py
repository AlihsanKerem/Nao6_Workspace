# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
services = session.services()
print("Services count: {}".format(len(services)))
for s in sorted([s["name"] for s in services]):
    if "File" in s or "Package" in s or "System" in s or "Audio" in s:
        print(" - " + s)
