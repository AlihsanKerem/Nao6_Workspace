# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
motion = session.service("ALMotion")
print("Move config:")
print(motion.getMoveConfig("Default"))
