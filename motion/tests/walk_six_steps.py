# -*- coding: utf-8 -*-
import sys
import time
import qi

def walk_six_steps(distance=0.125):
    """
    NAO robotunun guvenli sekilde yaklasik 6 adim (25 cm) ileri yurumesini saglar.
    NAO'nun tek adim boyutu varsayilan olarak ~4 cm (0.04 m) dir.
    24-25 cm ileri hareket (moveTo), dengeli ZMP planlamasi ile 6 adim atip ayaklari birlestirir.
    """
    print("NAO robotuna baglaniliyor (nao.local)...")
    session = qi.Session()
    try:
        session.connect("tcp://nao.local:9559")
    except Exception as e:
        print("Baglanti hatasi: {}".format(e))
        return False

    motion = session.service("ALMotion")
    posture = session.service("ALRobotPosture")
    tts = session.service("ALTextToSpeech")

    print("[1/4] Robot motorlari aktiflestiriliyor (wakeUp)...")
    motion.wakeUp()

    print("[2/4] Yuruyus baslangic durusuna geciliyor (StandInit)...")
    posture.goToPosture("StandInit", 0.5)

    print("[3/4] Robot konusuyor ve yuruyuse basliyor...")
    tts.say("Alti adim ileri yuruyorum.")

    # moveTo(x, y, theta): x ileri mesafe (metre), y yanal (metre), theta donus (radyan)
    # Bu cagri bloklayicidir; adimlar bitene kadar bekler.
    print("Yuruyus basladi (Hedef: {} metre ileri)...".format(distance))
    motion.moveTo(distance, 0.0, 0.0)

    print("[4/4] Adimlar tamamlandi.")
    tts.say("Yuruyus tamamlandi, durdum.")
    print("Robot durdu ve dengede bekliyor.")
    return True

if __name__ == "__main__":
    # Varsayilan olarak 0.25m (~6 adim)
    dist = 0.125
    if len(sys.argv) > 1:
        try:
            dist = float(sys.argv[1])
        except ValueError:
            pass
    walk_six_steps(dist)
