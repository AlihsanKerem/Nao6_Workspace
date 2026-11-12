# -*- coding: utf-8 -*-
import os
import sys
import json
import qi

class RobotConnection(object):
    """
    Manages connection and qi.Session to NAO6 robot or Choregraphe simulation.
    """
    def __init__(self, config_path=None, mode=None):
        if config_path is None:
            # Root directory config.json
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config.json")
            
        self.config_path = config_path
        self.config = self._load_config()
        
        self.mode = mode if mode else self.config.get("mode", "simulation")
        env = self.config.get("environments", {}).get(self.mode, {})
        self.ip = env.get("ip", "127.0.0.1")
        self.port = env.get("port", 9559)
        
        self.session = None

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise IOError("Configuration file not found: {}".format(self.config_path))
        with open(self.config_path, "r") as f:
            return json.load(f)

    def connect(self):
        """
        Connects to the robot or simulation server.
        """
        print("[Core] Connecting to NAO in mode '{}' at tcp://{}:{}...".format(self.mode, self.ip, self.port))
        self.session = qi.Session()
        try:
            self.session.connect("tcp://{}:{}".format(self.ip, self.port))
            print("[Core] Connected successfully to {}!".format(self.mode))
            return self.session
        except Exception as e:
            print("[Core] Connection failed to tcp://{}:{}: {}".format(self.ip, self.port, e))
            raise

    def get_service(self, service_name):
        """
        Returns a NAOqi service instance from the active session.
        """
        if self.session is None or not self.session.isConnected():
            self.connect()
        try:
            return self.session.service(service_name)
        except Exception as e:
            print("[Core] Failed to obtain service '{}': {}".format(service_name, e))
            raise

    def close(self):
        if self.session and self.session.isConnected():
            self.session.close()
            print("[Core] Session closed.")


_default_connection = None

def get_connection(mode=None):
    global _default_connection
    if _default_connection is None:
        _default_connection = RobotConnection(mode=mode)
    return _default_connection
