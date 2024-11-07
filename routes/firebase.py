# routes/firebase.py

from fastapi import APIRouter
from apis.firebase_storage import list_photos_in_folder

firebase_router = APIRouter()

@firebase_router.get("/firebase/photos/about")
def get_about_photos():
    photos = list_photos_in_folder()
    return {"photos": photos}
