# models/director.py

class Director:
    def __init__(self, name, pronouns, image, role, chair, department):
        self.name = name
        self.pronouns = pronouns
        self.image = image
        self.role = role
        self.chair = chair
        self.department = department

    def __repr__(self):
        return f"Director(name='{self.name}', role='{self.role}', department='{self.department}')"

    def to_dict(self):
        return {
            "name": self.name,
            "pronouns": self.pronouns,
            "image": self.image,
            "role": self.role,
            "chair": self.chair,
            "department": self.department
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("Name"),
            pronouns=data.get("Pronouns"),
            image=data.get("Image"),
            role=data.get("Role"),
            chair=data.get("Chair"),
            department=data.get("Department")
        )
