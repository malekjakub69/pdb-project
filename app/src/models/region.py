from src.models import db
from src.models.base import BaseModel


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
