# models/resource.py

from pydantic import BaseModel

class Prize(BaseModel):
    category: str
    type: str 
    prizes: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            category =data.get("category", ""),
            type=data.get("type", ""),
            prizes=data.get("prizes", ""),
        )
