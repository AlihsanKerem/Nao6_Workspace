# -*- coding: utf-8 -*-
import time
from core.connection import get_connection

class WifiManager(object):
    """
    Manages Wi-Fi connections via ALConnectionManager (supported on real robot).
    """
    def __init__(self, connection=None):
        self.connection = connection if connection else get_connection()
        self._cm = None

    @property
    def cm(self):
        if self._cm is None:
            self._cm = self.connection.get_service("ALConnectionManager")
        return self._cm

    def scan_wifi(self):
        """
        Scans for available Wi-Fi networks and returns a list of dictionaries.
        """
        if self.connection.mode == "simulation":
            print("[Network] Notice: Wi-Fi management is not supported in simulation mode.")
            return []
            
        print("[Network] Scanning Wi-Fi networks...")
        try:
            self.cm.scan("wifi")
            time.sleep(3)
            raw_services = self.cm.services()
            results = []
            for s in raw_services:
                d = dict(s)
                if d.get("Type") == "wifi":
                    results.append({
                        "name": d.get("Name"),
                        "security": d.get("Security"),
                        "strength": d.get("Strength"),
                        "state": d.get("State")
                    })
            return results
        except Exception as e:
            print("[Network] Error scanning Wi-Fi: {}".format(e))
            return []
