#!/usr/bin/env python3
import os
import speech_recognition as sr
import simpleaudio as sa

TRIGGERS = ['hey Idris', 'hey interest', 'hey address']
TRIGGER_RESPONSE = '/home/fareed/Music/init_trigger_response.wav'

gcloud_json_credentials_path = os.environ['GCLOUD_JSON_CREDENTIALS_PATH']


with open(gcloud_json_credentials_path, 'r') as f:
    credentials = f.read()

r = sr.Recognizer()

def get_audio_transcription(audio_filepath):
    with sr.Microphone() as source:
        print('listenting...')
        audio = r.listen(source)
        print('Stopped Listening.')
    return r.recognize_google_cloud(audio_data=audio, credentials_json=credentials, show_all=True, preferred_phrases=['hey Idris'])

def play_response(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

data = get_audio_transcription('/home/fareed/Music/hey_idris.wav')
transcript = data['results'][0]['alternatives'][0]['transcript']
confidence = data['results'][0]['alternatives'][0]['confidence']

if transcript in TRIGGERS and confidence >= 0.8:
    play_response(TRIGGER_RESPONSE)