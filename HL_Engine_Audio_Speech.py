"""
HL_Engine_sR.py
Author:Akhil P Jacob
HLDynamic-Integrations
"""
import pygame
import pyttsx3
import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS
from playsound import playsound as play_music
from HL_Engine_2.HL_CommonDependency import *


class AudioSpeechEngine:
    """SpeechEngine System"""

    def speech_recognition(self):
        """Speech Recognition System"""
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                display_message(SAY_SOMETHING)
                audio = r.listen(source)
            try:
                display_message("HLEngine:You said: " + r.recognize_google(audio))
                content = r.recognize_google(audio)
                return content
            except sr.UnknownValueError:
                return COULD_NOT_UNDERSTAND
            except sr.RequestError as e:
                return COULD_NOT_CREATE_REQUEST.format(e)
        except:
            return False

    def sentiment_analysis(self, param):
        """Sentimental Analysis"""
        try:
            blob1 = TextBlob(param)
            polarity_score = blob1.sentiment.polarity
            return polarity_score
        except:
            return False

    def sound_player(self, sound_file_path):
        """Play sound"""
        try:
            play_music(sound_file_path)
        except:
            return False

    def save_audio(self, text_data, location):
        """Save to Audio"""
        try:
            language = "en"
            object = gTTS(text=text_data, lang=language, slow=False)
            object.save(location)
        except:
            return False

    def read_text(self, text_data):
        """Read text data"""
        try:
            engine = pyttsx3.init()
            engine.getProperty("rate")
            engine.setProperty("rate", RATE_OF_SPEECH)
            engine.say(text_data)
            engine.runAndWait()
        except:
            return False
