from Calendar_Info import Event_List
from Calendar_Info import Current_Event_Calculator
from Google_Authenticator import Create_Service
from Map_Sender import Notification_Email
from datetime import datetime, timedelta
from dateutil.parser import parse as dtparse
import time

CLIENT_SECRET_FILE = "client_secret_file.json"
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Creates service to access the Google Calendar
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

calendar_id = "s6vmosdmoet0lvmpncnjvmum5c@group.calendar.google.com"

events = Event_List(service, calendar_id)
home = input("What is your address? ")
distances = Current_Event_Calculator(home, events)
times = {}
for event in distances:
    times[event] = dtparse(event["start"]["dateTime"]) - timedelta(hours=0, minutes = (distances[event] / 60 + 10))

while True:
    for event in distances:
        if (times[event] >= datetime.now()):
            print(event["summary"])
            Notification_Email("Antyolonio@gmail.com", "Antbrolonio@gmail.com", event["summary"])
            del distances[event]
    if not distances:
        break
    time.sleep(300)