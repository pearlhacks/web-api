# firebase_storage.py

import os
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the service account key JSON file path
service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize the app with a service account, granting admin privileges
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
    })

bucket = storage.bucket()


def list_photos_in_about_folder():
    # List all blobs (files) in the '/about' folder
    blobs = bucket.list_blobs(prefix='about/')  # Prefix with folder name

    photo_urls = []
    for blob in blobs:
        if not blob.name.endswith('/'):  # Ignore folder itself
            # Generate a signed URL for each blob
            url = blob.generate_signed_url(expiration=3600)  # URL valid for 1 hour
            photo_urls.append(url)

    return photo_urls


if __name__ == '__main__':
    photos = list_photos_in_about_folder()
    print("Photos in '/about' folder:")
    for photo_url in photos:
        print(photo_url)
