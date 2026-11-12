# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
cm = session.service("ALConnectionManager")

print("Services and technologies:")
try:
    print("Technologies:", cm.technologies())
    print("State:", cm.state())
    services = cm.services()
    print("Available Wi-Fi services:")
    for s in services:
        name = s.get("Name", "")
        tech = s.get("Type", "")
        state = s.get("State", "")
        print(" - [{}] {} (State: {})".format(tech, name, state))
except Exception as e:
    print("Error:", e)
