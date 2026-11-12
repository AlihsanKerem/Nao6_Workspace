# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
cm = session.service("ALConnectionManager")

services = cm.services()
print("Services count: {}".format(len(services)))
for i, s in enumerate(services):
    print("Item {}: type={}, val={}".format(i, type(s), repr(s)[:150]))
