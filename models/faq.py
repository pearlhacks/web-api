# models/faq.py

from pydantic import BaseModel

class FAQ(BaseModel):
    question: str
    answer: str
    category: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data.get("Question", ""),
            answer=data.get("Answer", ""),
            category=data.get("Category", "")
        )
