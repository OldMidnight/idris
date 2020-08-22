#!/usr/bin/env python3
TRIGGERS = ['hey Idris', 'hey interest', 'hey address']

#  Structure: {trigger_string: aknowledgement_response_index}
DEBREIEF_TRIGGERS = {
    'debrief me': 0,
    "what's going on": 1,
    "what's going on today": 1,
    "what's happening today": 1
    }

GRATITUDE_TRIGGERS = ['thanks', 'awesome thanks']

CALENDAR_EVENT_TRIGGERS = ['create an event']

def recognise_trigger(transcript, triggers):
    transcript_list = transcript.split()
    trigger_found = False
    i = 0
    while i < len(triggers) and trigger_found == False:
        recognise_list = triggers[i].split()
        temp_transcript_list = transcript_list
        while len(temp_transcript_list) >= len(recognise_list) and trigger_found == False:
            if temp_transcript_list[:len(recognise_list)] == recognise_list:
                trigger_found = True
            else:
                temp_transcript_list = temp_transcript_list[len(recognise_list):]
        i += 1
    return [trigger_found, triggers[i-1], transcript_list]