# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
motion = session.service("ALMotion")

step_methods = [m for m in motion.getMethodList() if "step" in m.lower() or "walk" in m.lower() or "move" in m.lower()]
for m in sorted(step_methods):
    print(" - " + m)
