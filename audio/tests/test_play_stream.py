# -*- coding: utf-8 -*-
import qi
import socket
import threading
import SimpleHTTPServer
import SocketServer
import time
import os

PORT = 8888
AUDIO_FILE = "Cat Laughing Meme Sound Effect..mp3"

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("NAO requested URL: {}".format(self.path))
        if "/sound.mp3" in self.path:
            try:
                with open(AUDIO_FILE, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()
                self.wfile.write(data)
                print("Successfully sent {} bytes of sound.mp3 to NAO!".format(len(data)))
                return
            except Exception as e:
                print("Error serving file: {}".format(e))
        self.send_error(404, "File Not Found")

    def log_message(self, format, *args):
        print("HTTP: " + (format % args))

def get_local_ip(target_ip="169.254.46.177"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((target_ip, 9559))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def main():
    local_ip = get_local_ip()
    print("Local IP towards NAO: {}".format(local_ip))

    server = SocketServer.TCPServer(("", PORT), CustomHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()
    print("HTTP Server started on port {}".format(PORT))

    print("Connecting to NAO via qi...")
    session = qi.Session()
    session.connect("tcp://nao.local:9559")
    audio = session.service("ALAudioPlayer")

    url = "http://{}:{}/sound.mp3".format(local_ip, PORT)
    print("Calling audio.playWebStream('{}', 1.0, 0.0)...".format(url))
    try:
        # volume: 1.0, pan: 0.0 (center)
        res = audio.playWebStream(url, 1.0, 0.0)
        print("playWebStream return/task id: {}".format(res))
    except Exception as e:
        print("playWebStream call error: {}".format(e))

    # Wait for the audio to finish playing (e.g., 10 seconds)
    print("Waiting for playback...")
    time.sleep(10)
    print("Stopping / finishing...")
    try:
        audio.stopAll()
    except Exception:
        pass
    server.shutdown()
    print("Finished.")

if __name__ == "__main__":
    main()
