import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Creates a service whit takes the client secret file, an api, the version of the api, and the scopes of the request
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    # Check parameters are correct
    print(client_secret_file, api_name, api_version, scopes, sep = "-")

    # Check scopes are correct
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)
    cred = None

    # Creates pickle file of given parameters
    pickle_file = f"token_{api_name}_{api_version}.pickle"

    # Check file is correct
    print(pickle_file)
    
    # Check to see if file exists
    if os.path.exists(pickle_file):
        # Open the pickle file as a token
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    # See if pickle file token is valid
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        # Open pickle file and login to the server
        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)

    # Build the service to the desired API
    try:
        service = build(api_name, api_version, credentials = cred)
        print(api_name, "service created successfully")
        return service
    except Exception as e:
        print(e)
        return None