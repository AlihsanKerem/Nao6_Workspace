# -*- coding: utf-8 -*-
import qi

def test_mdns():
    print("Testing connection to NAO via hostname 'nao.local:9559'...")
    session = qi.Session()
    try:
        session.connect("tcp://nao.local:9559")
        print("SUCCESS! Connected via 'nao.local'!")
        tts = session.service("ALTextToSpeech")
        tts.say("İsim çözümleme başarılı.")
    except Exception as e:
        print("Connection via nao.local failed: {}".format(e))

if __name__ == "__main__":
    test_mdns()
