# -*- coding: utf-8 -*-
import os
import json
from core.connection import get_connection

class MotionController(object):
    """
    Controls NAO's motion and postures (ALMotion, ALRobotPosture).
    Fully supported in Choregraphe simulation 3D view and on real robot.
    """
    def __init__(self, connection=None, config_path=None):
        self.connection = connection if connection else get_connection()
        
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "motion_config.json")
        self.config = self._load_config(config_path)
        
        self._motion = None
        self._posture = None

    def _load_config(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {
            "default_step_distance": 0.125,
            "default_speed": 0.5,
            "postures": {"init": "StandInit", "sit": "Sit"}
        }

    @property
    def motion(self):
        if self._motion is None:
            self._motion = self.connection.get_service("ALMotion")
        return self._motion

    @property
    def posture(self):
        if self._posture is None:
            self._posture = self.connection.get_service("ALRobotPosture")
        return self._posture

    def wake_up(self):
        """Stiffens motors and readies the robot."""
        print("[Motion] Waking up robot motors...")
        self.motion.wakeUp()

    def rest(self):
        """Relaxes motors to rest position."""
        print("[Motion] Setting robot to rest...")
        self.motion.rest()

    def go_to_posture(self, posture_name="StandInit", speed=None):
        """Moves robot to requested posture (StandInit, Sit, Crouch, etc.)."""
        spd = speed if speed is not None else self.config.get("default_speed", 0.5)
        print("[Motion] Going to posture: '{}' (speed: {})...".format(posture_name, spd))
        return self.posture.goToPosture(posture_name, spd)

    def stand_init(self):
        return self.go_to_posture("StandInit")

    def sit(self):
        return self.go_to_posture("Sit")

    def walk(self, x=None, y=0.0, theta=0.0):
        """
        Moves the robot by x (forward/back in meters), y (lateral), theta (rotation in radians).
        Blocking call: returns after movement finishes.
        """
        if x is None:
            x = self.config.get("default_step_distance", 0.125)
        print("[Motion] Moving robot: x={}m, y={}m, theta={}rad...".format(x, y, theta))
        self.motion.moveTo(x, y, theta)
        print("[Motion] Movement complete.")

    def stop_move(self):
        """Emergency stop for current movement."""
        self.motion.stopMove()
