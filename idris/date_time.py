#!/usr/bin/env python3
import wave
from datetime import datetime


hour_mapping = {
    0: ['12', 'am'],
    1: ['1', 'am'],
    2: ['2', 'am'],
    3: ['3', 'am'],
    4: ['4', 'am'],
    5: ['5', 'am'],
    6: ['6', 'am'],
    7: ['7', 'am'],
    8: ['8', 'am'],
    9: ['9', 'am'],
    10: ['10', 'am'],
    11: ['11', 'am'],
    12: ['12', 'pm'],
    13: ['1', 'pm'],
    14: ['2', 'pm'],
    15: ['3', 'pm'],
    16: ['4', 'pm'],
    17: ['5', 'pm'],
    18: ['6', 'pm'],
    19: ['7', 'pm'],
    20: ['8', 'pm'],
    21: ['9', 'pm'],
    22: ['10', 'pm'],
    23: ['11', 'pm']
}

year = datetime.now().year
month = datetime.now().month
day = datetime.now().day
hour = datetime.now().hour
minute = datetime.now().minute

year_audio = '/home/fareed/Music/Date_Time/year.wav'
month_audio = f'/home/fareed/Music/Date_Time/month_{month}.wav'
day_audio = f'/home/fareed/Music/Date_Time/day_{day}.wav'
hour_audio = f'/home/fareed/Music/Date_Time/time_{hour_mapping[hour][0]}.wav'
minute_audio = f'/home/fareed/Music/Date_Time/minute_{minute}.wav' if minute != '0' else '/home/fareed/Music/Date_Time/o_clock.wav'

today = '/home/fareed/Music/Date_Time/today.wav'
now = '/home/fareed/Music/Date_Time/now.wav'


def idris_date_time():
    input_files = [today, day_audio, month_audio, year_audio, now, hour_audio, minute_audio, f'/home/fareed/Music/Date_Time/{hour_mapping[hour][1]}.wav']
    output_file = '/home/fareed/Music/records/datetime.wav'

    data = []
    for input_file in input_files:
        w = wave.open(input_file, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
        
    output = wave.open(output_file, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()

    return output_file