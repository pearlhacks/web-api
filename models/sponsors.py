# models/sponsor.py

from pydantic import BaseModel

class Sponsor(BaseModel):
    img_url: str
    name: str
    tier: str
    url: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            img_url=data.get("img_url", ""),
            name=data.get("name", ""),
            tier=data.get("tier", ""),
            url=data.get("url", "")
        )
