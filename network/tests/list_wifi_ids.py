# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
cm = session.service("ALConnectionManager")

for s in cm.services():
    d = dict(s)
    if d.get("Type") == "wifi":
        print("SSID: {}, ServiceId: {}".format(d.get("Name"), d.get("ServiceId")))
