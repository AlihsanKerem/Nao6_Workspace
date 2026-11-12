# -*- coding: utf-8 -*-
"""
NAO6 Ana Kontrol Programi
Simulasyon (Choregraphe) veya Gercek Robot uzerinde modul entegrasyonu.
"""
import sys
import time

from core import RobotConnection
from speech import Speaker
from motion import MotionController
from audio import AudioPlayer
from network import WifiManager

class NaoRobot(object):
    def __init__(self, mode=None):
        self.connection = RobotConnection(mode=mode)
        self.speaker = Speaker(connection=self.connection)
        self.motion = MotionController(connection=self.connection)
        self.audio = AudioPlayer(connection=self.connection)
        self.network = WifiManager(connection=self.connection)

    def connect(self):
        return self.connection.connect()

    def demo_sequence(self):
        """
        Ornek gosterim senaryosu:
        1. Konusma
        2. Ayaga kalkma
        3. Adim atma
        4. Oturma / Dinlenme
        """
        print("\n=== NAO6 Demo Baslatiliyor ===")
        
        # 1. Konusma
        self.speaker.say("Merhaba! Ben NAO, sistemlerim hazir.")
        time.sleep(1)

        # 2. Motorlari ac ve ayaga kalk
        self.motion.wake_up()
        self.motion.stand_init()
        time.sleep(1)

        # 3. Yuru
        self.speaker.say("Simdi adim atiyorum.")
        self.motion.walk() # motion_config.json'daki mesafeyi kullanir
        time.sleep(1)

        # 4. Dinlenme moduna gec
        self.speaker.say("Gorev tamamlandi, dinlenmeye geciyorum.")
        self.motion.rest()
        print("=== Demo Tamamlandi ===\n")

def main():
    print("=" * 50)
    print("NAO6 Robot Yonetim Sistemi")
    print("=" * 50)
    
    # Komut satiri argumani ile mod secilebilir (python main.py simulation / real)
    mode = None
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    robot = NaoRobot(mode=mode)
    
    try:
        robot.connect()
    except Exception as e:
        print("\n[UYARI] Baglanti saglanamadi!")
        if robot.connection.mode == "simulation":
            print("Choregraphe uygulamasinda 'Connect to virtual robot' acik mi?")
            print("config.json dosyasindaki port Choregraphe'deki port ile eslesiyor mu?")
        else:
            print("Robot acik ve ayni agda mi? (IP: {})".format(robot.connection.ip))
        return

    # Ornek senaryoyu calistir
    try:
        robot.demo_sequence()
    except Exception as e:
        print("[Hata] Senaryo sirasinda hata olustu: {}".format(e))
    finally:
        robot.connection.close()

if __name__ == "__main__":
    main()
