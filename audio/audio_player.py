# -*- coding: utf-8 -*-
import os
import sys
import time
import socket
import threading
import SimpleHTTPServer
import SocketServer
import urllib
from core.connection import get_connection

class SilentHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
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
        pass

class AudioPlayer(object):
    """
    Plays sound files (mp3, wav) on NAO robot by streaming via local temporary HTTP server.
    """
    def __init__(self, connection=None, sounds_dir=None):
        self.connection = connection if connection else get_connection()
        if sounds_dir is None:
            sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
        self.sounds_dir = sounds_dir
        self._audio = None

    @property
    def audio(self):
        if self._audio is None:
            self._audio = self.connection.get_service("ALAudioPlayer")
        return self._audio

    def _get_lan_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            target_ip = self.connection.ip if self.connection.ip != "127.0.0.1" else "192.168.1.1"
            s.connect((target_ip, 9559))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            s.close()

    def play_sound(self, sound_file, duration=7, volume=1.0):
        """
        Plays sound file located in sounds/ or given by absolute path.
        """
        if not os.path.isabs(sound_file):
            abs_path = os.path.join(self.sounds_dir, sound_file)
        else:
            abs_path = sound_file

        if not os.path.isfile(abs_path):
            print("[Audio] Error: Sound file not found: {}".format(abs_path))
            return False

        # Allocate ephemeral port
        temp_sock = socket.socket()
        temp_sock.bind(("", 0))
        port = temp_sock.getsockname()[1]
        temp_sock.close()

        file_dir = os.path.dirname(abs_path)
        base_name = os.path.basename(abs_path)

        old_cwd = os.getcwd()
        os.chdir(file_dir)
        try:
            server = ThreadedHTTPServer(("", port), SilentHandler)
            srv_thread = threading.Thread(target=server.serve_forever)
            srv_thread.daemon = True
            srv_thread.start()

            lan_ip = self._get_lan_ip()
            url = "http://{}:{}/{}".format(lan_ip, port, urllib.quote(base_name))
            print("[Audio] Streaming audio: {}".format(url))
            self.audio.playWebStream(url, float(volume), 0.0)

            time.sleep(duration)
            try:
                self.audio.stopAll()
            except Exception:
                pass
            print("[Audio] Sound finished.")
            return True
        except Exception as e:
            print("[Audio] Error playing sound: {}".format(e))
            return False
        finally:
            try:
                server.shutdown()
            except Exception:
                pass
            os.chdir(old_cwd)

    def stop_all(self):
        try:
            self.audio.stopAll()
        except Exception as e:
            print("[Audio] Error stopping audio: {}".format(e))
