# -*- coding: utf-8 -*-
import os
import json
from core.connection import get_connection

class Speaker(object):
    """
    Controls NAO's speech (TTS - Text To Speech).
    Works in both real robot and Choregraphe simulation.
    """
    def __init__(self, connection=None, config_path=None):
        self.connection = connection if connection else get_connection()
        
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "speech_config.json")
        self.config = self._load_config(config_path)
        
        self._tts = None

    def _load_config(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {"language": "Turkish", "volume": 0.75}

    @property
    def tts(self):
        if self._tts is None:
            self._tts = self.connection.get_service("ALTextToSpeech")
            # Apply initial config
            try:
                lang = self.config.get("language")
                if lang:
                    available = self._tts.getAvailableLanguages()
                    if lang in available:
                        self._tts.setLanguage(lang)
                vol = self.config.get("volume")
                if vol is not None:
                    self._tts.setVolume(float(vol))
            except Exception as e:
                print("[Speech] Warning applying initial config: {}".format(e))
        return self._tts

    def say(self, message):
        """
        Speaks the given message.
        """
        print("[Speech] Saying: '{}'".format(message))
        self.tts.say(message)

    def set_volume(self, volume):
        """
        Sets volume between 0.0 and 1.0.
        """
        self.tts.setVolume(float(volume))

    def set_language(self, language):
        """
        Sets language (e.g. 'Turkish', 'English').
        """
        self.tts.setLanguage(language)
