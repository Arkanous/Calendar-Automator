import datetime
from pprint import pprint
from Google_Authenticator import Create_Service
from Calendar_Creator import convert_to_RFC_datetime
from Map_Sender import Distance_Calc

# Gets all the calendars that the account has
def Calendar_List(service):
    response = service.calendarList().list(
        maxResults = 250,
        showDeleted = False,
        showHidden = False
    ).execute()
    calendarItems = response.get("items")
    nextPageToken = response.get("nextPageToken")

    while nextPageToken: 
        response = service.calendarList().list(
            maxResults = 250,
            showDelete = False,
            showHidden = False,
            pageToken = nextPageToken
        ).execute()
        calendarItems.extend(response.get("items"))
        nextPageToken = response.get("nextPageToken")
    return response.get("items")

# Gets the list of events in the calendar in the last page of the pagetoken
def Event_List(service, calendar_id):
    events = service.events().list(calendarId=calendar_id).execute()
    return events.get("items")

# def Event_List(service, calendar_id):
#     page_token = None
#     while True:
#         events = service.events().list(calendarId=calendar_id, pageToken = page_token).execute()
#         for event in events.get("items"):
#             print (event["location"])
#             print (event["start"]["dateTime"])
#         page_token = events.get("nextPageToken")
#         if not page_token:
#             break
#     return events.get("items")

# Returns a map of each event linked to the distance from an address if the event is today
def Current_Event_Calculator(home, event_info):
    distances = {}
    for event in event_info:
        if (event["start"]["dateTime"].day == datetime.Today):
            distances[event] = Distance_Calc(home, event["location"])
    return distances