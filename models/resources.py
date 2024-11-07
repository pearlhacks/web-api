# models/resource.py

class Resource:
    def __init__(self, category, img_url, title, types, url):
        self.category = category
        self.img_url = img_url
        self.title = title
        self.types = types
        self.url = url

    def __repr__(self):
        return f"Resource(title='{self.title}', category='{self.category}', types='{self.types}')"

    def to_dict(self):
        return {
            "category": self.category,
            "img_url": self.img_url,
            "title": self.title,
            "types": self.types,
            "url": self.url
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            category=data.get("category"),
            img_url=data.get("img_url"),
            title=data.get("title"),
            types=data.get("types"),
            url=data.get("url")
        )
