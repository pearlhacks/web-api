# models/schedule.py

from pydantic import BaseModel

class Schedule(BaseModel):
    event_name: str
    event_type: str
    date: str
    start_time: str
    duration: str
    location: str
    link: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            event_name=data.get("Event", ""),
            event_type=data.get("Type", ""),
            date=data.get("Date", ""),
            start_time=data.get("Start Time", ""),
            duration=data.get("Duration (Hour)", ""),
            location=data.get("Location", ""),
            link=data.get("Link", "")
        )
