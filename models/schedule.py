# models/schedule.py

class Schedule:
    def __init__(self, event_name, event_type, date, start_time, duration, location, link):
        self.event_name = event_name
        self.event_type = event_type
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.location = location
        self.link = link

    def __repr__(self):
        return f"Schedule(event_name='{self.event_name}', date='{self.date}', start_time='{self.start_time}')"

    def to_dict(self):
        return {
            "event_name": self.event_name,
            "event_type": self.event_type,
            "date": self.date,
            "start_time": self.start_time,
            "duration": self.duration,
            "location": self.location,
            "link": self.link
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            event_name=data.get("Event"),
            event_type=data.get("Type"),
            date=data.get("Date"),
            start_time=data.get('Start Time'),
            duration=data.get("Duration (Hour)"),
            location=data.get("Location"),
            link=data.get("Link")
        )
