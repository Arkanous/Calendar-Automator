from Google_Authenticator import Create_Service
from Calendar_Creator import Create_Calendar
from Calendar_Creator import Delete_Calendar
from Calendar_Info import Event_List

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

# Delets the calendar
Delete_Calendar(service, calendar_id, event)