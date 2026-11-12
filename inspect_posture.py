# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
posture = session.service("ALRobotPosture")
print("Posture service OK! Posture list:")
print(posture.getPostureList())
print("Current posture: {}".format(posture.getPosture()))
