#!/usr/bin/env python3
import wave
from idris.utils.services import CalendarService
from idris.date_time import hour_mapping

calendar = CalendarService()

def format_events(event):
    time_array = event['start']['dateTime'].split('T')[1].split(':')[:2] # [hour, minute]
    return time_array

def idris_calendar_brief():
    events = list(map(format_events, calendar.get_events()))

    if len(events) == 0:
        events_no_audio = '/home/fareed/Music/Calendar/none.wav'
    elif len(events) > 10:
        events_no_audio = '/home/fareed/Music/Numbers/lots.wav'
    else:
        events_no_audio = f'/home/fareed/Music/Numbers/{len(events)}.wav'

    you_have_audio = '/home/fareed/Music/Calendar/you_got.wav'
    events_today_audio = '/home/fareed/Music/Calendar/events_today.wav'
    next_event_audio = '/home/fareed/Music/Calendar/next_event.wav'

    if len(events) > 0:
        next_event = events[0]
        hour = int(next_event[0])
        hour_audio = f'/home/fareed/Music/Date_Time/time_{hour_mapping[hour][0]}.wav'
        minute_audio = f'/home/fareed/Music/Date_Time/minute_{next_event[1]}.wav' if next_event[1] != '0' else '/home/fareed/Music/Date_Time/o_clock.wav'
        input_files = [you_have_audio, events_no_audio, events_today_audio, next_event_audio, hour_audio, minute_audio, f'/home/fareed/Music/Date_Time/{hour_mapping[hour][1]}.wav']
    else:
        input_files = [you_have_audio, events_no_audio, events_today_audio]
    output_file = '/home/fareed/Music/records/calendar_debrief.wav'

    data = []
    for input_file in input_files:
        print(input_file)
        w = wave.open(input_file, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(output_file, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()

    return output_file
