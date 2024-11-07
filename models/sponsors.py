# models/sponsor.py

class Sponsor:
    def __init__(self, img_url, name, tier, url):
        self.img_url = img_url
        self.name = name
        self.tier = tier
        self.url = url

    def __repr__(self):
        return f"Sponsor(name='{self.name}', tier='{self.tier}')"

    def to_dict(self):
        return {
            "img_url": self.img_url,
            "name": self.name,
            "tier": self.tier,
            "url": self.url
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            img_url=data.get("img_url"),
            name=data.get("name"),
            tier=data.get("tier"),
            url=data.get("url")
        )
