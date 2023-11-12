from src.models.base import BaseIdModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import List
from src.models.article import Article
from src.models.comment import Comment
from src.models.like import Like
from src.models.read import Read



class User(BaseIdModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)

    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    region: Mapped["Region"] = relationship(back_populates="users")

    articles: Mapped[List["Article"]] = relationship(back_populates="author")

    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

    likes: Mapped[List["Like"]] = relationship(back_populates="user")

    reads: Mapped[List["Read"]] = relationship(back_populates="user")