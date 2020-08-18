#!/usr/bin/env python3
import os
import speech_recognition as sr
import simpleaudio as sa
from time import sleep
from random import randint
from idris.utils.timer import RepeatingTimer
from idris.utils.triggers import *
from idris.utils.responses import *
from idris.utils.services import gcloud_json_credentials_path
from idris.date_time import idris_date_time
from idris.idris_calendar import idris_calendar_brief

def debrief_trigger_filter(debrief):
    return debrief

class Idris():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.idris_triggered = False
        self.idris_reset_trigger = RepeatingTimer(20, self.reset_idris_trigger_state)
        self.stop_listening = None
        self.playing_response = False
        with open(gcloud_json_credentials_path, 'r') as f:
            self.credentials = f.read()

    def process_data(self, data):
        try:
            transcript = data['results'][0]['alternatives'][0]['transcript']
            confidence = data['results'][0]['alternatives'][0]['confidence']
        except KeyError as e:
            transcript = ''
            confidence = 0

        # print(transcript)
        # print(confidence)
        # print(self.idris_triggered)

        # INITIAL TRIGGER
        if transcript in TRIGGERS and confidence >= 0.5 and not self.idris_triggered:
            self.play_response(TRIGGER_RESPONSE)
        # IF TRIGGER WORD IS CALLED AGAIN BUT IDRIS IS STILL LISTENING
        elif transcript in TRIGGERS and confidence >= 0.5 and self.idris_triggered:
            self.play_response(LISTENING_RESPONSE)
        # DEBRIEF TRIGGER
        elif transcript in DEBREIEF_TRIGGERS and confidence >= 0.8 and self.idris_triggered:
            self.play_response(ACKNOWLEDGEMENT_RESPONSES[DEBREIEF_TRIGGERS[transcript]], True)
            self.play_response(idris_date_time())
            self.play_response(idris_calendar_brief())
        # GRATITUDE TRIGGER
        elif transcript in GRATITUDE_TRIGGERS and confidence >= 0.8 and self.idris_triggered:
            self.play_response(GRATITUDE_RESPONSES[randint(0,1)])

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
        while True:
            print('listening...')
            with self.mic as source: audio = self.recognizer.listen(source)
            try:
                data = self.recognizer.recognize_google_cloud(audio_data=audio, credentials_json=self.credentials, show_all=True, preferred_phrases=TRIGGERS + list(map(debrief_trigger_filter, DEBREIEF_TRIGGERS)) + GRATITUDE_TRIGGERS)
                self.process_data(data)
            except:
                pass
            sleep(0.5)

    def reset_idris_trigger_state(self):
        self.idris_triggered = False

    def play_response(self, filename, dont_reset=False):
        print('playing response')
        # print(filename)
        self.playing_response = True
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        print('finished playing')
        if not dont_reset:
            self.idris_triggered = True
            self.idris_reset_trigger.start()

idris = Idris()
idris.listen()