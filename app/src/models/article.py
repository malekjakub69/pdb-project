from src.models.base import BaseIdModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import List
from src.models.comment import Comment
from src.models.like import Like
from src.models.read import Read

class Article(BaseIdModel):
    __tablename__ = "article"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    perex: Mapped[str] = mapped_column(String(512), nullable=False)
    content: Mapped[str] = mapped_column(String(65535), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="articles")

    comments: Mapped[List["Comment"]] = relationship(back_populates="article")

    likes: Mapped[List["Like"]] = relationship(back_populates="article")

    reads: Mapped[List["Read"]] = relationship(back_populates="article")