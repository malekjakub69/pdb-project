from src.models import db
from src.models.base import BaseModel, T
from typing import Type


class Region(BaseModel):
    __tablename__ = "region"

    iso_code = db.Column(db.String(3), unique=True, nullable=False)
    country_name = db.Column(db.String(255), nullable=False)

    users = db.relationship("User", back_populates="region")

    def get_full_dict(self):
        return {
            "id": self.id,
            "iso_code": self.iso_code,
            "country_name": self.country_name,
            "users": [user.get_dict() for user in self.users],
        }

    def get_dict(self):
        return {
            "id": self.id,
            "iso_code": self.iso_code,
            "country_name": self.country_name,
        }

    @classmethod
    def get_by_iso_code(cls: Type[T], id_string: str) -> T:
        id_string = id_string.lower()
        region = cls.query.filter(Region.iso_code == id_string).first()
        return region
