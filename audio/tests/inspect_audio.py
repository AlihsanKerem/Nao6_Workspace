# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://nao.local:9559")
audio = session.service("ALAudioPlayer")
methods = audio.getMethodList()
print("ALAudioPlayer methods:")
for m in sorted(methods):
    print(" - " + m)
