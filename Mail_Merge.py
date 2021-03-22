import os
import datetime
import time
import io
import pprint
from googleapiclient.http import MediaIoBaseDownload
from Google_Authenticator import Create_Service

CLIENT_SECRET_FILE = "client_secret_file.json"

# Google Docs
service_docs = Create_Service(
    CLIENT_SECRET_FILE,
    "docs", "v1",
    ["https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"]
)
time.sleep(2)

# Google Drive
service_drive = Create_Service(
    CLIENT_SECRET_FILE,
    "drive",
    "v3",
    ["https://www.googleapis.com/auth/drive"]
)
time.sleep(2)

# Google Sheets
service_sheets = Create_Service(
    CLIENT_SECRET_FILE,
    "sheets",
    "v4",
    ["https://www.googleapis.com/auth/spreadsheets"]
)
time.sleep(2)

document_id = "1_QysJOyyaZADogf1bz0wZ7iyoZ9edrQ7af6cJFl_4C4"
sheets_id = "1atCLbmLD4rhNuLPIqoOFAXrF_O9jYSNUyCsdDinJWrw"
folder_id = "11MAb_tV8p6OebQlA1tgDiuboWKki72R8" # None --> save in parent folder

responses = {}

# Load Google sheets
worksheet_name = "Projects"
responses["sheets"] = service_sheets.spreadsheets().values().get(
    spreadsheetId = sheets_id,
    range = worksheet_name,
    majorDimension = "ROWS"
).execute()

# Get the labels and the values for each label 
columns = responses["sheets"]["values"][0]
records = responses["sheets"]["values"][1:]

# Json representation of replacing one word with another plus special formating
def mapping(merge_field, value = ""):
    json_rep = {
        "replaceAllText": {
            "replaceText": value,
            "containsText": {
                "matchCase": "true",
                "text": "{{{{{0}}}}}".format(merge_field)
            }
        }
    }
    return json_rep

# Iterate each record and combine with the docs
for record in records:
    print("processing record {0}..." .format(record[2]))

    #Copy new doc file as new doc file
    document_title = "SOW for {0}".format(record[2])

    responses["docs"] = service_drive.files().copy(
        fileId = document_id,
        body = {
            "parents": [service_drive],
            "name": document_title
        }
    ).execute()
    new_document_id = responses["docs"]["id"]

    #update google docs document
    merge_fields_info = [mapping(columns[indx],value) for indx, value in enumerate(record)]

    service_docs.documents().batchUpdate(
        documentId = new_document_id,
        body = {
            "requests": merge_fields_info
        }
    ).execute()