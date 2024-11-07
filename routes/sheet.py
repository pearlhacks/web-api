# routes/sheet.py

from fastapi import APIRouter
from apis import sheets
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
