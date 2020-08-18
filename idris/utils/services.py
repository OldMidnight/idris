#!/usr/bin/env python3
import os
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
gcloud_json_credentials_path = os.environ['GCLOUD_JSON_CREDENTIALS_PATH']
service_account = os.environ['GCLOUD_SERVICE_ACCOUNT']

class CalendarService():
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(gcloud_json_credentials_path, scopes=CALENDAR_SCOPES)
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_events(self):
        now = datetime.utcnow()
        now_iso = now.isoformat() + 'Z' # 'Z' indicates UTC time
        day_end = datetime(now.year, now.month, now.day, 23, 59, 59).isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='fareedidris20@gmail.com', timeMin=now_iso, timeMax=day_end, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
