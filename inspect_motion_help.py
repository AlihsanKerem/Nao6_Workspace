# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
motion = session.service("ALMotion")
print("setFootSteps help:")
print(motion.getMethodHelp("setFootSteps"))
print("\nsetFootStepsWithSpeed help:")
print(motion.getMethodHelp("setFootStepsWithSpeed"))
print("\nmoveTo help:")
print(motion.getMethodHelp("moveTo"))
