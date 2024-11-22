# routes/sheet.py

from fastapi import APIRouter, HTTPException
from apis import sheets
from apis.sheets import getDevpostLinks # add getLinks after making getLinks()
from typing import List
#from models.resource_link import ResourceLink
from models.devpost_link import DevpostLink
from models.directors import Director
from models.schedule import Schedule
from models.resources import Resource
from models.sponsors import Sponsor
from models.faq import FAQ

sheet_router = APIRouter()

@sheet_router.get("/sheet/directors", response_model=dict)
def get_directors():
    directors = sheets.getDirector()
    data = [director.to_dict() for director in directors]
    return {"directors": data}

@sheet_router.get("/sheet/schedules", response_model=dict)
def get_schedules():
    schedules = sheets.getSchedule()
    data = [schedule.to_dict() for schedule in schedules]
    return {"schedules": data}

@sheet_router.get("/sheet/resources", response_model=dict)
def get_resources():
    resources = sheets.getResource()
    data = [resource.to_dict() for resource in resources]
    return {"resources": data}

@sheet_router.get("/sheet/sponsors", response_model=dict)
def get_sponsors():
    sponsors = sheets.getSponsor()
    data = [sponsor.to_dict() for sponsor in sponsors]
    return {"sponsors": data}

@sheet_router.get("/sheet/faqs", response_model=dict)
def get_faqs():
    faqs = sheets.getFAQ()
    data = [faq.to_dict() for faq in faqs]
    return {"faqs": data}

# @sheet_router.get("/sheet/links", response_model=List[ResourceLink])
# def get_resource_links():
#     """
#     Endpoint to retrieve general resource links.
#     """
#     links = getLinks()
#     if not links:
#         raise HTTPException(status_code=404, detail="No resource links found.")
#     return links

@sheet_router.get("/sheet/devpost_links", response_model=List[DevpostLink])
def get_devpost_resource_links():
    """
    Endpoint to retrieve Devpost-specific resource links.
    """
    devpost_links = getDevpostLinks()
    if not devpost_links:
        raise HTTPException(status_code=404, detail="No Devpost resource links found.")
    return devpost_links