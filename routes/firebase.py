# routes/firebase.py

from fastapi import APIRouter, HTTPException, Path
from apis.firebase_storage import list_photos_in_folder

firebase_router = APIRouter()


@firebase_router.get("/firebase/photos/{folder_name}")
def get_photos_from_folder(
        folder_name: str = Path(..., title="Folder Name", description="Name of the folder in Firebase Storage")
):
    if not folder_name.isalnum() and not all(c in "-_" for c in folder_name):
        raise HTTPException(status_code=400, detail="Invalid folder name.")

    photos = list_photos_in_folder(folder_name)
    if not photos:
        raise HTTPException(status_code=404, detail=f"No photos found in folder '{folder_name}'.")
    return {"photos": photos}
