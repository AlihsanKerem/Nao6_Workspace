# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
cm = session.service("ALConnectionManager")

print("ALConnectionManager methods:")
for m in sorted(cm.getMethodList()):
    print(" - " + m)
