import os
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


SHEET_ID = '16YJSaBwjpGRq81ryZ-Z284HkgKwYvg2MHjkBpD0IaJk'


# Function to authenticate and build the Sheets API service
def get_sheets_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=5000)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the service
    service = build('sheets', 'v4', credentials=creds)
    return service


# Function to read data from the Google Sheet
def read_sheet_data():
    service = get_sheets_service()
    RANGE_NAME = 'faq!A1:D10'

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            print(f'{row}')



def update_sheet_data():
    service = get_sheets_service()
    RANGE_NAME = 'Sheet1!A1'
    # Example data to write into the sheet
    # values = [
    #     ["Name", "Age", "City"],
    #     ["Ishan", "18", "Chapel Hill"],
    #     ["Alex", "21", "Raleigh"]
    # ]
    body = {
        'values': values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=RANGE_NAME,
        valueInputOption="RAW", body=body).execute()

    print(f'{result.get("updatedCells")} cells updated.')


def add_event_data():
    service = get_sheets_service()
    RANGE_NAME = 'Sheet1!A1'  # Adjust this to the range where you want to start inputting data

    # Define the data to add to the sheet (in rows)
    values = [
        ["Question", "Answer"],  # Column headers
        ["When am I able to park?", "Parking is free for all Pearl Hacks attendees in the Bell Tower Deck starting at 5 pm on Friday, February 14th. If you arrive at UNC before 5 pm on Friday, parking options are limited."],
        ["Where am I able to park?", "Bell Tower Deck, Cobb Parking Deck - Both locations on campus are available for parking."],
        ["How can I get reimbursed?", "To be considered for reimbursement, fill out the Google Form before Pearl Hacks and demo your project to receive gas reimbursements."],
        ["How will my reimbursement be given to me?", "Reimbursements are given in the form of Amazon gift cards based on distance from Pearl Hacks."],
        ["Who can I contact on the weekend of Pearl Hacks?", "There will be a dedicated channel in the Pearl Hacks Discord for travel and parking questions."],
        ["What if I don’t have a car to get to Pearl Hacks?", "Carpooling is encouraged, and participants can fill out a form to find a group to travel with."]
    ]

    body = {
        'values': values
    }

    # Send the update request
    result = service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=RANGE_NAME,
        valueInputOption="RAW", body=body).execute()

    print(f'{result.get("updatedCells")} cells updated.')

if __name__ == '__main__':
    read_sheet_data()

