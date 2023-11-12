from src.models.base import BaseIdModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from typing import List
from sqlalchemy.orm import relationship
from src.models.user import User

class Region(BaseIdModel):
    __tablename__ = "region"

    iso_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    country_name: Mapped[str] = mapped_column(String(255), nullable=False)


    users: Mapped[List["User"]] = relationship(back_populates="region")
