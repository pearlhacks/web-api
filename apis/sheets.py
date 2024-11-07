# apis/sheets.py

import os
from flask import Blueprint, jsonify
from apis import sheets
from dotenv import load_dotenv

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from models.schedule import Schedule
from models.resources import Resource
from models.sponsors import Sponsor
from models.directors import Director
from models.faq import FAQ

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
load_dotenv()
SHEET_ID = os.getenv('SHEET_ID')

# Cache variables
_schedules = None
_resources = None
_sponsors = None
_directors = None
_faqs = None


def get_sheets_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=5000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    return service


def read_sheet_data(page):
    service = get_sheets_service()
    RANGE_NAME = f'{page}!A1:D10'  # Adjust the range as needed

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print(f'No data found in sheet {page}.')
        return []
    else:
        headers = values[0]
        data = [dict(zip(headers, row)) for row in values[1:]]
        return data


def getSchedule():
    global _schedules
    if _schedules is None:
        data = read_sheet_data('schedule')
        _schedules = [Schedule.from_dict(item) for item in data]
    return _schedules


def getResource():
    global _resources
    if _resources is None:
        data = read_sheet_data('resources')
        _resources = [Resource.from_dict(item) for item in data]
    return _resources


def getSponsor():
    global _sponsors
    if _sponsors is None:
        data = read_sheet_data('sponsors')
        _sponsors = [Sponsor.from_dict(item) for item in data]
    return _sponsors


def getDirector():
    global _directors
    if _directors is None:
        data = read_sheet_data('directors')
        _directors = [Director.from_dict(item) for item in data]
    return _directors


def getFAQ():
    global _faqs
    if _faqs is None:
        data = read_sheet_data('faq')
        _faqs = [FAQ.from_dict(item) for item in data]
    return _faqs
