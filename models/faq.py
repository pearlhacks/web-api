# models/faq.py

class FAQ:
    def __init__(self, answer, category, question):
        self.answer = answer
        self.category = category
        self.question = question

    def __repr__(self):
        return f"FAQ(question='{self.question}', category='{self.category}')"

    def to_dict(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data.get('Question'),
            answer=data.get('Answer'),
            category=data.get('Category')
        )
