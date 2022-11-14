"""audio_processing_sample.py"""
from HL_Engine_2 import HL_Engine_Audio_Speech

class AudioProcessing:
    """Audio Processing"""

    def __init__(self):
        self.processor=HL_Engine_Audio_Speech.AudioSpeechEngine()
    
    def speech_recognition_algo(self):
        """Speech recognition"""
        data=self.processor.speech_recognition()
        print(data)

    def sentimental_approach(self,word):
        """Sentimental Analysis"""
        score=self.processor.sentiment_analysis(word)
        print(score)

    def text_to_speech_save(self,data,location):
        """Text to speech"""
        self.processor.save_audio(data,location)

    def text_to_speech_algo(self,data):
        self.processor.read_text(data)



AP=AudioProcessing()
#   AP.speech_recognition_algo()
#   Words="Dr APJ Kalam is such a humble person, even though he was rich"
#   AP.sentimental_approach(Words)
#   AP.text_to_speech_save(Words,"Result.wav")
#   AP.text_to_speech_algo(Words)