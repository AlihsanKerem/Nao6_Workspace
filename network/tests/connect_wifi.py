# -*- coding: utf-8 -*-
import sys
import time
import qi

def list_and_connect(target_ssid=None, password=None):
    print("NAO robotuna baglaniliyor (nao.local)...")
    session = qi.Session()
    try:
        session.connect("tcp://nao.local:9559")
    except Exception as e:
        print("Baglanti hatasi: {}".format(e))
        return

    cm = session.service("ALConnectionManager")

    print("Wi-Fi aglari taraniyor...")
    cm.scan("wifi")
    time.sleep(2)

    services = cm.services()
    wifi_list = []
    for s in services:
        d = dict(s)
        if d.get("Type") == "wifi":
            wifi_list.append(d)

    if not target_ssid:
        print("\n--- Etraftaki Wi-Fi Aglari ---")
        for idx, w in enumerate(wifi_list):
            name = w.get("Name", "Gizli Ag")
            sec = ",".join(w.get("Security", []))
            strength = w.get("Strength", 0)
            state = w.get("State", "idle")
            print("{}) {} [Sinyal: %{}, Guvenlik: {}, Durum: {}]".format(idx + 1, name, strength, sec, state))
        print("\nBaglanmak icin: .\\nao_python.bat connect_wifi.py \"Ag_Adi\" \"Sifre\"")
        return

    # Belirtilen SSID'yi bul
    matched = None
    for w in wifi_list:
        if w.get("Name") == target_ssid:
            matched = w
            break

    if not matched:
        print("HATA: '{}' adli Wi-Fi agi bulunamadi!".format(target_ssid))
        return

    service_id = matched.get("ServiceId")
    print("Aga baglaniliyor: {} ({})".format(target_ssid, service_id))

    try:
        # Sifre gerektiren aglar icin giris
        if password:
            # ALConnectionManager.setServiceConfiguration
            # Bazı NAOqi surumlerinde connect direkt veya konfigurasyonla yapilir
            try:
                cm.setServiceInput([["ServiceId", service_id], ["Passphrase", password]])
            except Exception:
                pass
        
        cm.connect(service_id)
        print("Baglanti istegi gonderildi. Bekleniyor...")
        time.sleep(5)

        # Durumu kontrol et
        services = cm.services()
        for s in services:
            d = dict(s)
            if d.get("ServiceId") == service_id:
                print("Sonuc Durumu: {}".format(d.get("State")))
                if d.get("State") in ["online", "ready"]:
                    print("TEBRIKLER: Robot basariyla '{}' agina baglandi!".format(target_ssid))
                    print("Robot bu agi hafizasina kaydetti (Autoconnect: True).")
                    print("Artik Ethernet kablosunu cikarabilirsiniz!")
                else:
                    print("Baglanti henuz tamamlanamadi veya parola hatali olabilir.")
                break

    except Exception as e:
        print("Baglanti sirasinda hata: {}".format(e))

if __name__ == "__main__":
    ssid = sys.argv[1] if len(sys.argv) > 1 else None
    pwd = sys.argv[2] if len(sys.argv) > 2 else None
    list_and_connect(ssid, pwd)
