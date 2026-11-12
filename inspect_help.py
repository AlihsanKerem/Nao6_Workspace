# -*- coding: utf-8 -*-
import qi
import json

session = qi.Session()
session.connect("tcp://nao.local:9559")
audio = session.service("ALAudioPlayer")
print("playWebStream help:")
print(audio.getMethodHelp("playWebStream"))
print("\nplayFile help:")
print(audio.getMethodHelp("playFile"))
print("\nplayFileFromPosition help:")
print(audio.getMethodHelp("playFileFromPosition"))
