# models/resource.py

from pydantic import BaseModel

class Resource(BaseModel):
    category: str
    img_url: str
    title: str
    resource_type: str  # Renamed from 'type' to 'resource_type'
    url: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            category=data.get("category", ""),
            img_url=data.get("img_url", ""),
            title=data.get("title", ""),
            resource_type=data.get("types", ""),  # Access 'Type' from the sheet
            url=data.get("url", "")
        )
