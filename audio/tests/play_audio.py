# -*- coding: utf-8 -*-
import os
import sys
import time
import socket
import threading
import SimpleHTTPServer
import SocketServer
import urllib
import qi

class SilentHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # HTTP loglarini sessizlestir
        pass

    def finish(self, *args, **kwargs):
        try:
            if not self.wfile.closed:
                self.wfile.flush()
                self.wfile.close()
        except socket.error:
            pass
        try:
            self.rfile.close()
        except Exception:
            pass

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def handle_error(self, request, client_address):
        # Istemci (NAO) dinlemeyi bitirip soketi kapattiginda olusan 10054'u yut
        pass

def get_lan_ip(target_ip="169.254.46.177"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((target_ip, 9559))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def play_sound(file_name, duration=None, volume=1.0):
    abs_path = os.path.abspath(file_name)
    if not os.path.isfile(abs_path):
        print("HATA: Dosya bulunamadi -> " + abs_path)
        return False

    temp_sock = socket.socket()
    temp_sock.bind(("", 0))
    port = temp_sock.getsockname()[1]
    temp_sock.close()

    file_dir = os.path.dirname(abs_path)
    base_name = os.path.basename(abs_path)

    old_cwd = os.getcwd()
    os.chdir(file_dir)

    server = ThreadedHTTPServer(("", port), SilentHandler)
    srv_thread = threading.Thread(target=server.serve_forever)
    srv_thread.daemon = True
    srv_thread.start()

    lan_ip = get_lan_ip()
    url = "http://{}:{}/{}".format(lan_ip, port, urllib.quote(base_name))

    print("[1/3] Ses akisi hazirlandi: " + url)
    print("[2/3] NAO robotuna baglaniliyor (nao.local)...")
    
    try:
        session = qi.Session()
        session.connect("tcp://nao.local:9559")
        audio = session.service("ALAudioPlayer")
        print("[3/3] Robot ses dosyasini caliyor: " + base_name)
        
        # playWebStream(url, volume, pan)
        audio.playWebStream(url, float(volume), 0.0)

        # Sure belirtilmediyse dosya boyutuna gore makul bir sure bekle (en az 6 saniye)
        wait_time = duration if duration else 7
        print("Ses caliniyor ({} saniye bekleniyor)...".format(wait_time))
        time.sleep(wait_time)

        try:
            audio.stopAll()
        except Exception:
            pass

        print("Basariyla tamamlandi!")
        return True

    except Exception as e:
        print("Calma sirasinda hata olustu: {}".format(e))
        return False
    finally:
        try:
            server.shutdown()
        except Exception:
            pass
        os.chdir(old_cwd)

if __name__ == "__main__":
    target = "Cat Laughing Meme Sound Effect..mp3"
    dur = None
    if len(sys.argv) > 1:
        target = sys.argv[1]
    if len(sys.argv) > 2:
        dur = float(sys.argv[2])
    play_sound(target, duration=dur, volume=1.0)
