# -*- coding: utf-8 -*-
"""
NAO6 Canlı Servis ve Metot Keşif Aracı (Robot Inspector)
Kullanım:
    python inspect_robot.py                   -> Robottaki tüm aktif servisleri listeler
    python inspect_robot.py ALMotion          -> ALMotion servisinin tüm fonksiyonlarını listeler
    python inspect_robot.py ALMotion moveTo   -> moveTo fonksiyonunun yardımını/parametrelerini gösterir
"""

import sys
import os
import core.connection as cc

def main():
    try:
        conn = cc.get_connection()
        session = conn.connect()
    except Exception as e:
        print("[Inspector] HATA: Robota veya simulasyona baglanilamadi: {}".format(e))
        print("Lutfen Choregraphe sanal robotunun calistigindan emin olun.")
        sys.exit(1)

    args = sys.argv[1:]

    # 1. Hic arguman verilmediyse: Tum servisleri listele
    if len(args) == 0:
        print("\n" + "="*60)
        print("  NAO6 AKTIF SERVISLERI (Toplam {})".format(len(session.services())))
        print("="*60)
        services = sorted(session.services(), key=lambda x: x["name"])
        for idx, s in enumerate(services, 1):
            print("{:3d}. {}".format(idx, s["name"]))
        print("="*60)
        print("\nBir servisi incelemek icin:")
        print("  nao_python.bat inspect_robot.py <ServisAdi>")
        print("Ornek:")
        print("  nao_python.bat inspect_robot.py ALTextToSpeech\n")
        return

    service_name = args[0]
    try:
        service = session.service(service_name)
    except Exception as e:
        print("[Inspector] HATA: '{}' servisi alinamadi: {}".format(service_name, e))
        return

    # 2. Servis adi verildi ama metot adi verilmediyse: Metotlari listele
    if len(args) == 1:
        print("\n" + "="*60)
        print("  {} SERVISI METOTLARI".format(service_name))
        print("="*60)
        try:
            methods = sorted(service.getMethodList())
            for idx, m in enumerate(methods, 1):
                print("{:3d}. {}".format(idx, m))
            print("="*60)
            print("Toplam {} metot bulundu.".format(len(methods)))
            print("\nBir metodun detaylarini gormek icin:")
            print("  nao_python.bat inspect_robot.py {} <MetotAdi>".format(service_name))
        except Exception as e:
            print("Metot listesi alinamadi: {}".format(e))
        return

    # 3. Hem servis hem metot adi verildiyse: Metot yardimini goster
    method_name = args[1]
    print("\n" + "="*60)
    print("  {}.{}() DETAYLARI".format(service_name, method_name))
    print("="*60)
    try:
        help_info = service.getMethodHelp(method_name)
        if isinstance(help_info, (list, tuple)):
            # [method_name, [arg1_desc, arg2_desc], return_desc, docstring]
            for item in help_info:
                print(item)
        else:
            print(help_info)
    except Exception as e:
        print("Metot yardimi alinamadi: {}".format(e))
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
