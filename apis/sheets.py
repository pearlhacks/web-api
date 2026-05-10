# apis/sheets.py

import os
import time
from flask import Blueprint, jsonify
from apis import sheets
from apis.firebase_storage import generate_signed_url
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
from models.prizes import Prize

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
load_dotenv()
SHEET_ID = os.getenv('SHEET_ID')

# Cache TTL in seconds (default: 5 minutes)
CACHE_TTL_SECONDS = int(os.getenv('CACHE_TTL_SECONDS', 300))

# Cache variables - now stores data with timestamp
_cache = {
    'schedules': {'data': None, 'timestamp': None},
    'resources': {'data': None, 'timestamp': None},
    'sponsors': {'data': None, 'timestamp': None},
    'directors': {'data': None, 'timestamp': None},
    'faqs': {'data': None, 'timestamp': None},
    'prizes': {'data': None, 'timestamp': None}
}

def get_sheets_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    return service


def read_sheet_data(page):
    service = get_sheets_service()
    RANGE_NAME = f'{page}!A1:X99'  # Adjust the range as needed

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


def is_cache_expired(cache_key):
    """Check if cache for the given key is expired or doesn't exist"""
    cache_entry = _cache.get(cache_key)
    if cache_entry['data'] is None or cache_entry['timestamp'] is None:
        return True

    elapsed_time = time.time() - cache_entry['timestamp']
    return elapsed_time > CACHE_TTL_SECONDS


def invalidate_cache(cache_key=None):
    """
    Invalidate cache for a specific key or all caches if no key is provided.

    Args:
        cache_key: Specific cache to invalidate (e.g., 'schedules', 'resources')
                   If None, invalidates all caches

    Returns:
        List of invalidated cache keys
    """
    global _cache

    if cache_key is None:
        # Invalidate all caches
        invalidated = []
        for key in _cache.keys():
            _cache[key] = {'data': None, 'timestamp': None}
            invalidated.append(key)
        return invalidated
    else:
        # Invalidate specific cache
        if cache_key in _cache:
            _cache[cache_key] = {'data': None, 'timestamp': None}
            return [cache_key]
        else:
            return []


def getSchedule():
    global _cache
    if is_cache_expired('schedules'):
        data = read_sheet_data('schedule')
        _cache['schedules']['data'] = [Schedule.from_dict(item) for item in data]
        _cache['schedules']['timestamp'] = time.time()
    return _cache['schedules']['data']


def getResource():
    global _cache
    if is_cache_expired('resources'):
        data = read_sheet_data('resources')
        _cache['resources']['data'] = [Resource.from_dict(item) for item in data]
        _cache['resources']['timestamp'] = time.time()
    return _cache['resources']['data']


def getSponsor():
    global _cache
    if is_cache_expired('sponsors'):
        data = read_sheet_data('sponsors')
        _cache['sponsors']['data'] = [Sponsor.from_dict(item) for item in data]
        _cache['sponsors']['timestamp'] = time.time()
    return _cache['sponsors']['data']


def getFAQ():
    global _cache
    if is_cache_expired('faqs'):
        data = read_sheet_data('faq')
        _cache['faqs']['data'] = [FAQ.from_dict(item) for item in data]
        _cache['faqs']['timestamp'] = time.time()
    return _cache['faqs']['data']

def getPrizes():
    global _cache
    if is_cache_expired('prizes'):
        data = read_sheet_data('prizes')
        _cache['prizes']['data'] = [Prize.from_dict(item) for item in data]
        _cache['prizes']['timestamp'] = time.time()
    return _cache['prizes']['data']

def getDirector():
    global _cache
    if is_cache_expired('directors'):
        data = read_sheet_data('directors')
        directors_list = []
        for item in data:
            director = Director.from_dict(item)
            if director.image:
                image_file_path = f"{director.image}"  # Assuming the image field contains the filename
                image_url = generate_signed_url(image_file_path)
                director.image_url = image_url
            else:
                director.image_url = None
            directors_list.append(director)
        _cache['directors']['data'] = directors_list
        _cache['directors']['timestamp'] = time.time()
    return _cache['directors']['data']