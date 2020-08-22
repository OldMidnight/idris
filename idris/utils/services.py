#!/usr/bin/env python3
import os
import wave
import calendar
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from idris.date_time import hour_mapping

CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
gcloud_json_credentials_path = os.environ['GCLOUD_JSON_CREDENTIALS_PATH']
service_account = os.environ['GCLOUD_SERVICE_ACCOUNT']

class MissingDetailsException(Exception):
    pass

def update_date_with_time(date, trigger_args):
    if 'p.m.' in trigger_args:
        time = trigger_args[trigger_args.index('p.m.') - 1].split(':')
        if len(time) == 2:
            return date.replace(hour=int(time[0]) + 12, minute=int(time[1]), second=0, microsecond=0)
        else:
            return date.replace(hour=int(time[0]) + 12, second=0, microsecond=0)
    elif 'a.m.' in trigger_args:
        time = trigger_args[trigger_args.index('a.m.') - 1].split(':')
        if len(time) == 2:
            return date.replace(hour=int(time[0]), minute=int(time[1]), second=0, microsecond=0)
        else:
            return date.replace(hour=int(time[0]), minute=0, second=0, microsecond=0)
    else:
        raise MissingDetailsException()

def format_events(event):
    time_array = event['start']['dateTime'].split('T')[1].split(':')[:2] # [hour, minute]
    return time_array

class CalendarService():
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(gcloud_json_credentials_path, scopes=CALENDAR_SCOPES)
        self.service = build('calendar', 'v3', credentials=self.credentials)
        self.trigger_map = {
            'create an event': self.create_event
        }

    def handle_trigger(self, trigger, trigger_args, event_name=None):
        try:
            self.trigger_map[trigger](trigger_args, event_name=event_name)
        except:
            raise

    def idris_calendar_brief(self):
        events = list(map(format_events, self.get_events()))

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
            w = wave.open(input_file, 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()

        output = wave.open(output_file, 'wb')
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()

        return output_file

    def get_events(self):
        now = datetime.now()
        now_iso = now.isoformat() + 'Z' # 'Z' indicates UTC time
        day_end = datetime(now.year, now.month, now.day, 23, 59, 59).isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='fareedidris20@gmail.com', timeMin=now_iso, timeMax=day_end, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def create_event(self, trigger_args, event_name=None):
        current_date = datetime.now()
        days = {
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
            'Sunday': 7
        }
        if 'tomorrow' in trigger_args:
            date = current_date + timedelta(days=1)
        elif 'next' in trigger_args:
            if trigger_args[trigger_args.index('next') + 1] == 'week':
                date = current_date + timedelta(days=7)
            elif trigger_args[trigger_args.index('next') + 1] == 'month':
                date = current_date + timedelta(month=1)
            elif trigger_args[trigger_args.index('next') + 1] in days:
                i = 0
                current_day = current_date.isoweekday()
                while current_day != days[trigger_args[trigger_args.index('next') + 1]]:
                    if current_day == 7:
                        current_day = 1
                    else:
                        current_day += 1
                    i += 1
                date = current_date + timedelta(days=i)
            else:
                raise MissingDetailsException()
        else:
            date = current_date

        if 'from' in trigger_args and 'to' in trigger_args:
            start_date_details = trigger_args[:trigger_args.index('to')]
            end_date_details = trigger_args[trigger_args.index('to'):]

            start_date = update_date_with_time(date, start_date_details)
            end_date = update_date_with_time(date, end_date_details)
        elif 'at' in trigger_args:
            start_date = update_date_with_time(date, trigger_args)
            end_date = start_date.replace(hour=int(start_date.hour) + 1)
        else:
            raise MissingDetailsException()

        if event_name:
            event_name_list = event_name.split()
            if len(event_name_list) > 2 and event_name_list[:2] == ['call', 'it']:
                summary = ' '.join(event_name_list[2:]).capitalize()
            else:
                summary = event_name.capitalize()
        elif 'call' in trigger_args:
            if trigger_args[trigger_args.index('call') + 1] == 'it':
                summary = ' '.join(trigger_args[trigger_args.index('call') + 1:]).capitalize()
            else:
                raise MissingDetailsException('summary')
        elif 'called' in trigger_args:
            summary = ' '.join(trigger_args[trigger_args.index('called') + 1:]).capitalize()
        else:
            raise MissingDetailsException('summary')

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_date.isoformat(),
                'timeZone': 'Europe/Dublin'
            },
            'end': {
                'dateTime': end_date.isoformat(),
                'timeZone': 'Europe/Dublin'
            }
        }
        self.service.events().insert(calendarId='fareedidris20@gmail.com', body=event).execute()
        print('Event Created')