#!/usr/bin/env python3
import os
import speech_recognition as sr
from playsound import playsound
from time import sleep
from random import randint
from idris.utils.timer import RepeatingTimer
from idris.utils.triggers import *
from idris.utils.responses import *
from idris.utils.services import gcloud_json_credentials_path, MissingDetailsException, CalendarService, TTSService
from idris.debrief import debrief

def debrief_trigger_filter(debrief):
    return debrief

class Idris():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        self.recognizer.energy_threshold = 500
        self.mic = sr.Microphone()
        self.idris_triggered = False
        self.idris_reset_trigger = RepeatingTimer(20, self.reset_idris_trigger_state)
        self.stop_listening = None
        self.playing_response = False
        self.calendar = CalendarService()
        self.tts = TTSService()
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
        if recognise_trigger(transcript, TRIGGERS)[0] and confidence >= 0.5 and not self.idris_triggered:
            self.play_response(TRIGGER_RESPONSE)
        # IF TRIGGER WORD IS CALLED AGAIN BUT IDRIS IS STILL LISTENING
        elif recognise_trigger(transcript, TRIGGERS)[0] and confidence >= 0.5 and self.idris_triggered:
            self.play_response(LISTENING_RESPONSE)
        # DEBRIEF TRIGGER
        elif recognise_trigger(transcript, list(map(debrief_trigger_filter, DEBREIEF_TRIGGERS)))[0] and confidence >= 0.8 and self.idris_triggered:
            self.play_response(ACKNOWLEDGEMENT_RESPONSES[DEBREIEF_TRIGGERS[transcript]], True)
            self.speak(text=debrief(self.calendar))
        # GRATITUDE TRIGGER
        elif recognise_trigger(transcript, GRATITUDE_TRIGGERS)[0] and confidence >= 0.8 and self.idris_triggered:
            self.play_response(GRATITUDE_RESPONSES[randint(0,1)])
        # CALENDAR TRIGGER
        elif recognise_trigger(transcript, CALENDAR_EVENT_TRIGGERS)[0] and confidence >= 0.8 and self.idris_triggered:
            calendar_args = recognise_trigger(transcript, CALENDAR_EVENT_TRIGGERS)
            try:
                self.calendar.handle_trigger(calendar_args[1], calendar_args[2])
                self.play_response(EVENT_CREATED_RESPONSE)
            except MissingDetailsException as e:
                if e.args[0] == 'summary':
                    self.play_response(EVENT_NAME_RESPONSE, dont_reset=True)
                    print('listening for event name...')
                    with self.mic as source: audio = self.recognizer.listen(source, phrase_time_limit=10)
                    try:
                        data = self.recognizer.recognize_google_cloud(audio_data=audio, credentials_json=self.credentials, show_all=True, preferred_phrases=['call it'])
                        try:
                            transcript = data['results'][0]['alternatives'][0]['transcript']
                        except KeyError as e:
                            transcript = ''
                        try:
                            self.calendar.handle_trigger(calendar_args[1], calendar_args[2], event_name=transcript)
                            self.play_response(EVENT_CREATED_RESPONSE)
                        except:
                            self.play_response(UNRECOGNIZED_RESPONSE)
                    except:
                        self.play_response(UNRECOGNIZED_RESPONSE)
                else:
                    self.play_response(UNRECOGNIZED_RESPONSE)

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
        while True:
            print('listening...')
            with self.mic as source: audio = self.recognizer.listen(source, phrase_time_limit=10)
            try:
                data = self.recognizer.recognize_google_cloud(audio_data=audio, credentials_json=self.credentials, show_all=True, preferred_phrases=TRIGGERS + list(map(debrief_trigger_filter, DEBREIEF_TRIGGERS)) + GRATITUDE_TRIGGERS)
                self.process_data(data)
            except:
                pass
            sleep(0.5)

    def speak(self, text=None, ssml=None, **kwargs):
        self.tts.synthesise(text, ssml)
        self.play_response(SYNTHESIZED_RESPONSE, kwargs)

    def reset_idris_trigger_state(self):
        self.idris_triggered = False

    def play_response(self, filename, dont_reset=False):
        print('playing response')
        # print(filename)
        self.playing_response = True
        playsound(filename)
        print('finished playing')
        if not dont_reset:
            self.idris_triggered = True
            self.idris_reset_trigger.start()

idris = Idris()
idris.listen()