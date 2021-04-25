from Google_Authenticator import Create_Service
from Calendar_Creator import convert_to_RFC_datetime
from Map_Sender import Distance_Calc
from datetime import date, datetime
from os import path
import datetime
import iso8601

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
    events = service.events().list(calendarId = calendar_id).execute()
    return events.get("items")

# Returns a map of each event linked to the distance from an address if the event is today
def Current_Event_Calculator(home, event_info):
    distances = {}
    for event in event_info:
        if (iso8601.parse_date(event["start"]["dateTime"]).day == date.today()):
            distances[event] = Distance_Calc(home, event["location"])
    return distances

def ToDo_List_Create():
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # To specify Google Sheets file basic settings and as well as configure default worksheets
    sheet_body = {
        'properties': {
            'title': 'To Do List',
            'locale': 'en_US', # optional
            'autoRecalc': 'ON_CHANGE', # calculation setting #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#RecalculationInterval
            'timeZone': 'America/Los_Angeles'
            }
        ,
        'sheets': [
            {
                'properties': {
                    'title': 'Body'
                }
            }
        ]
    }

    sheets_file = service.spreadsheets().create(body = sheet_body).execute()
    return steets_file

# Imports a calendar to a Google Sheets (Make it only look at the ones this week)
def ToDo_List_Import(calservice, calendar_id):

    events = Event_List(calservice, calendar_id)
    values = []
    worksheet_name = 'Body'
    
    sheetservice = Create_Service(
        "client_secret_file.json",
        "sheets",
        "v4",
        ["https://www.googleapis.com/auth/spreadsheets"]
    )

    if (path.exists("to_Do_List.txt")):
        list_File = open("to_Do_List.txt", "r")
        spreadsheet_id = list_File.readline()
    else:
        sheets = ToDo_List_Create()
        spreadsheet_id = sheets['spreadsheetId']
        f = open("to_Do_List.txt", "x")
        f.write(spreadsheet_id)
    try:
        request = sheetservice.spreadsheets().values().clear(
            spreadsheetId = spreadsheet_id, 
            range = worksheet_name
        ).execute()
    except: 
        sheets = ToDo_List_Create()
        spreadsheet_id = sheets['spreadsheetId']
        f = open("to_Do_List.txt", "w")
        f.write(spreadsheet_id)

    for event in events: 
        if (iso8601.parse_date(event["start"]["dateTime"]).day == date.today()):
            values.append((event["summary"], event["start"]["dateTime"], event["end"]["dateTime"], event["location"]))

    value_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }

    sheetservice.spreadsheets().values().update(
        spreadsheetId = spreadsheet_id,
        valueInputOption = 'USER_ENTERED',
        range = worksheet_name, 
        body = value_range_body
    ).execute()