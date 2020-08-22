#!/usr/bin/env python3
from datetime import datetime

hour_mapping = {
    0: ['12', 'A.M'],
    1: ['1', 'A.M'],
    2: ['2', 'A.M'],
    3: ['3', 'A.M'],
    4: ['4', 'A.M'],
    5: ['5', 'A.M'],
    6: ['6', 'A.M'],
    7: ['7', 'A.M'],
    8: ['8', 'A.M'],
    9: ['9', 'A.M'],
    10: ['10', 'A.M'],
    11: ['11', 'A.M'],
    12: ['12', 'P.M'],
    13: ['1', 'P.M'],
    14: ['2', 'P.M'],
    15: ['3', 'P.M'],
    16: ['4', 'P.M'],
    17: ['5', 'P.M'],
    18: ['6', 'P.M'],
    19: ['7', 'P.M'],
    20: ['8', 'P.M'],
    21: ['9', 'P.M'],
    22: ['10', 'P.M'],
    23: ['11', 'P.M']
}

def ordinal(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def date_format(dt,f):
    return dt.strftime(f).replace("{th}", ordinal(dt.day))

def idris_date_time():
    time = datetime.now()
    time_format = '%M past %I' if time.minute != 0 else "%I O'clock" 
    return f"Today is {date_format(time, '%A the {th} of %B. It is now ' + time_format)}."

def debrief(calendar):
    return f'{idris_date_time()} {calendar.idris_calendar_brief()}'