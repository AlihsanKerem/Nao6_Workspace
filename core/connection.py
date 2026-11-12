# -*- coding: utf-8 -*-
import os
import sys
import json
import subprocess
import qi

class RobotConnection(object):
    """
    Manages connection and qi.Session to NAO6 robot or Choregraphe simulation.
    Supports auto-detecting Choregraphe's dynamic virtual robot port on Windows.
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

    def _save_config(self):
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print("[Core] Warning: Failed to save updated config: {}".format(e))

    def detect_simulation_port(self):
        """
        Automatically detects the listening port of Choregraphe's virtual robot (naoqi-bin).
        Returns the port number as an int, or None if not found.
        """
        # Method 1: PowerShell Get-NetTCPConnection (fast and accurate on Windows)
        try:
            ps_script = (
                "$p = (Get-Process naoqi-bin -ErrorAction SilentlyContinue).Id; "
                "if ($p) { "
                "  $port = (Get-NetTCPConnection -OwningProcess $p -State Listen -ErrorAction SilentlyContinue | "
                "           Select-Object -ExpandProperty LocalPort -First 1); "
                "  if ($port) { Write-Output $port } "
                "}; exit 0"
            )
            p = subprocess.Popen(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, _ = p.communicate()
            out = out.strip()
            if out and out.isdigit():
                return int(out)
        except Exception:
            pass

        # Method 2: Fallback via netstat -ano
        try:
            ps_pid = 'powershell -NoProfile -Command "(Get-Process naoqi-bin -ErrorAction SilentlyContinue).Id"'
            out_pid = subprocess.check_output(ps_pid, shell=True).strip()
            if out_pid:
                pids = set(out_pid.split())
                netstat_out = subprocess.check_output("netstat -ano -p tcp", shell=True)
                for line in netstat_out.splitlines():
                    parts = line.split()
                    if len(parts) >= 5 and parts[0] == "TCP" and parts[3] == "LISTENING":
                        if parts[4] in pids:
                            local_addr = parts[1]
                            return int(local_addr.rsplit(":", 1)[-1])
        except Exception:
            pass

        return None

    def connect(self):
        """
        Connects to the robot or simulation server.
        """
        # If simulation mode and port is set to 'auto' or 0, detect automatically
        is_auto = (self.mode == "simulation" and 
                   (str(self.port).lower() == "auto" or not self.port or self.port == 0))
        
        if is_auto:
            print("[Core] Auto-detecting Choregraphe virtual robot port...")
            detected = self.detect_simulation_port()
            if detected:
                print("[Core] Auto-detected virtual robot on port {}.".format(detected))
                self.port = detected
            else:
                print("[Core] Warning: Could not detect running virtual robot (naoqi-bin). Falling back to 9559.")
                self.port = 9559

        print("[Core] Connecting to NAO in mode '{}' at tcp://{}:{}...".format(self.mode, self.ip, self.port))
        self.session = qi.Session()
        try:
            self.session.connect("tcp://{}:{}".format(self.ip, self.port))
            print("[Core] Connected successfully to {}!".format(self.mode))
            return self.session
        except Exception as e:
            # If in simulation mode and connection failed, try auto-detecting the dynamic port
            if self.mode == "simulation" and not is_auto:
                print("[Core] Connection failed to tcp://{}:{}. Searching for active virtual robot...".format(self.ip, self.port))
                detected = self.detect_simulation_port()
                if detected and detected != self.port:
                    print("[Core] Found virtual robot running on port {}! Retrying connection...".format(detected))
                    self.port = detected
                    try:
                        self.session = qi.Session()
                        self.session.connect("tcp://{}:{}".format(self.ip, self.port))
                        print("[Core] Connected successfully to simulation on port {}!".format(self.port))
                        # Update config.json so next time it is already current
                        if self.config.get("environments", {}).get("simulation", {}).get("port") != "auto":
                            self.config["environments"]["simulation"]["port"] = self.port
                            self._save_config()
                            print("[Core] Updated config.json simulation port to {}.".format(self.port))
                        return self.session
                    except Exception as retry_err:
                        print("[Core] Retry connection failed on port {}: {}".format(self.port, retry_err))

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
