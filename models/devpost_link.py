# models/devpost_link.py

from pydantic import BaseModel
from typing import Optional

class DevpostLink(BaseModel):
    """
    Represents a Devpost-specific resource link.

    Attributes:
        title (str): The title of the Devpost project or event.
        img_url (str): The URL to an image representing the Devpost resource.
        url (str): The actual Devpost link.
    """
    title: str
    img_url: str
    url: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title", ""),
            img_url=data.get("img_url", ""),
            url=data.get("url", "")
        )
