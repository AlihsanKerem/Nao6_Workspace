# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
fm = session.service("ALFileManager")
for m in sorted(fm.getMethodList()):
    print(" - " + m)
