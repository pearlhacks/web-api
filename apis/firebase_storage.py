# apis/firebase_storage.py
import datetime
import os
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    if not firebase_admin._apps:
        service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not service_account_path:
            raise ValueError("Service account key path not found in environment variables.")

        # reinit with a fresh app
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': os.getenv('NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET')
        })

def generate_signed_url(file_path):
    initialize_firebase()
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    
    if not blob.exists():
        print(f"File {file_path} does not exist in Firebase Storage.")
        return None

    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600)

    url = blob.generate_signed_url(expiration=expiration_time)
    print(f"Generated URL: {url}")
    return url

def list_photos_in_folder(folder_name):
    initialize_firebase()
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=f'{folder_name}/')

    photo_urls = []
    for blob in blobs:
        if not blob.name.endswith('/'):
            url = blob.generate_signed_url(expiration=3600)
            photo_urls.append(url)

    return photo_urls
