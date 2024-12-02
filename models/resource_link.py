# models/resource_link.py

from pydantic import BaseModel
from typing import List

class ResourceLink(BaseModel):
    category: str
    links: List[str]

    def to_dict(self):
        return self.dict()
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            category=data.get("category", ""),
            links=data.get("links", [])
        )
    
    