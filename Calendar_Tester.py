from Google_Authenticator import Create_Service
from Calendar_Creator import Create_Calendar
from Calendar_Creator import Delete_Calendar
from Calendar_Info import Event_List
from Calendar_Info import ToDo_List_Import
from Map_Sender import Distance_Calc
from datetime import date
from datetime import datetime, timedelta
import time
import pprint
from dateutil.parser import parse as dtparse

CLIENT_SECRET_FILE = "client_secret_file.json"
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

calendar_id = "s6vmosdmoet0lvmpncnjvmum5c@group.calendar.google.com"
# Creates service to access the desired API
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Creates a calendar
event = Create_Calendar(service, calendar_id, 0)

# Check to see if the service has worked
event_info = Event_List(service, calendar_id)

x = Distance_Calc("Mercer Island", "Bellevue")

print(dtparse(event["start"]["dateTime"]) - timedelta(hours=0, minutes = (x / 60 + 10)))

ToDo_List_Import(service, calendar_id, "1k9Uqb0GXT646koLk99M2f6WmLixEO5614dnUk5sDdTU")

# Delets the calendar
Delete_Calendar(service, calendar_id, event)

print(x)