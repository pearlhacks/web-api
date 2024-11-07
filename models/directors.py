# models/director.py

from pydantic import BaseModel
from typing import Optional

class Director(BaseModel):
    name: str
    pronouns: str
    image: str
    role: str
    chair: str
    department: str
    image_url: Optional[str] = None

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("Name", ""),
            pronouns=data.get("Pronouns", ""),
            image=data.get("Image", ""),
            role=data.get("Role", ""),
            chair=data.get("Chair", ""),
            department=data.get("Department", "")
        )
