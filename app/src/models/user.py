from typing import Type
from src.models import db
from src.models.base import BaseModel, T
from sqlalchemy import or_


class User(BaseModel):
    __tablename__ = "user"

    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey("region.id"), nullable=True)
    region = db.relationship("Region", back_populates="users")

    articles = db.relationship("Article", back_populates="author")

    comments = db.relationship("Comment", back_populates="author")

    likes = db.relationship("Like", back_populates="user")

    reads = db.relationship("Read", back_populates="user")

    @classmethod
    def get_by_email_or_login(cls: Type[T], id_string: str) -> T:
        id_string = id_string.lower()
        user = cls.query.filter(or_(User.email == id_string, User.username == id_string)).first()
        return user

    def get_full_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "region_id": self.region_id,
            "articles": [article.get_dict() for article in self.articles],
            "comments": [comment.get_dict() for comment in self.comments],
            "likes": [like.get_dict() for like in self.likes],
            "reads": [read.get_dict() for read in self.reads],
        }

    def get_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "region_id": self.region_id,
            "articles_id": [article.id for article in self.articles],
            "comments": [comment.id for comment in self.comments],
            "likes": [like.id for like in self.likes],
            "reads": [read.id for read in self.reads],
        }
