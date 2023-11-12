
from src.models import BaseModel

from sqlalchemy.orm import Mapped
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column


class BaseIdModel(BaseModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)