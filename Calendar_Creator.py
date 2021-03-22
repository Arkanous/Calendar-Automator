import datetime
from pprint import pprint
from Google_Authenticator import Create_Service

# Converts regular date to Google calendar readable date
def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + "Z"
    return dt

# Creates the message your event has
def Create_Calendar (service, calendar_id, hour_adjustment):
    # What the event says
    event_body = {
        "start": {
            "dateTime": convert_to_RFC_datetime(2021, 3, 14, 12 + hour_adjustment, 30),
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": convert_to_RFC_datetime(2021, 3, 14, 14 + hour_adjustment, 30),
            "timeZone": "America/Los_Angeles",
        },
        "summary": "Do Python",
        "description": "I have no idea what I\'m doing",
        "colorId": 5,
        "status": "confirmed",
        "transparency": "opaque",
        "visibility": "private",
        "location": "Seattle, WA",
        "organizer": {
            "id": None,
            "email": "Antbrolonio@gmail.com",
            "displayName": "Tony",
            "self": True
        },
        "attendees": [
            {
                "displayName": "Tony",
                "comment": "Why is this so complicated",
                "email": "Antbrolonio@gmail.com",
                "optional": False,
                "organizer": True,
                "responseStatus": "accepted",
            },
        ],

        # Unessesary fuctions I decided not to include

        # 'recurrence': [
        #     'RRULE:FREQ=DAILY;COUNT=1'
        # ],
        # 'reminders': {
        #     'useDefault': False,
        #     'overrides': [
        #     {'method': 'email', 'minutes': 24 * 60},
        #     {'method': 'popup', 'minutes': 10},
        #     ],
        # },
    }

    # Creates the event
    maxAttendees = 50
    sendNotifications = True
    sendUpdates = "none"
    supportsAttachments = True
    response = service.events().insert(
        calendarId = calendar_id,
        maxAttendees = maxAttendees,
        sendNotifications = sendNotifications,
        sendUpdates = sendUpdates,
        supportsAttachments = supportsAttachments,
        body = event_body,
    ).execute()
    # pprint(response)

    # Returns the event
    return response
    #response["id"]

# Delete an event
def Delete_Calendar(service, calendar_id, event):
    event_id = event["id"]
    service.events().delete(calendarId = calendar_id, eventId = event_id).execute()