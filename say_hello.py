# -*- coding: utf-8 -*-
import sys
import qi

ROBOT_IP = "169.254.46.177"
PORT = 9559

def main():
    print("Connecting to NAO at tcp://{}:{}...".format(ROBOT_IP, PORT))
    session = qi.Session()
    try:
        session.connect("tcp://{}:{}".format(ROBOT_IP, PORT))
        print("Connected successfully!")
    except Exception as e:
        print("Connection failed: {}".format(e))
        return

    # Check Text To Speech service
    try:
        tts = session.service("ALTextToSpeech")
        print("Obtained ALTextToSpeech service.")
        
        # Get volume and language
        try:
            vol = tts.getVolume()
            lang = tts.getLanguage()
            print("Current Language: {}, Volume: {}".format(lang, vol))
            if vol < 0.5:
                tts.setVolume(0.7)
        except Exception as e:
            print("Notice getting TTS properties: {}".format(e))

        message = "Merhaba, baglanti basarili. Ben NAO!"
        print("Making robot say: '{}'...".format(message))
        tts.say(message)
        print("Speech completed successfully!")

    except Exception as e:
        print("TTS Error: {}".format(e))

    # Also check robot battery & system info if available
    try:
        battery = session.service("ALBattery")
        charge = battery.getBatteryCharge()
        print("Battery charge: {}%".format(charge))
    except Exception as e:
        print("Could not get battery: {}".format(e))

    try:
        system = session.service("ALSystem")
        robot_name = system.robotName()
        print("Robot name: {}".format(robot_name))
    except Exception as e:
        print("Could not get robot name: {}".format(e))

if __name__ == "__main__":
    main()
