import json

from marshmallow import validates
from src.models import db
from src.models.base import BaseModel


class Article(BaseModel):
    __tablename__ = "article"

    title = db.Column(db.String(255), nullable=False)
    perex = db.Column(db.String(512), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    tags = db.Column(db.Text(), nullable=True)

    max_comments = db.Column(db.Integer, nullable=False, default=10)
    comments_count = db.Column(db.Integer, nullable=False, default=0)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="articles")

    comments = db.relationship(
        "Comment",
        back_populates="article",
        cascade="all,delete",
    )

    likes = db.relationship(
        "Like",
        back_populates="article",
        cascade="all,delete",
    )

    reads = db.relationship(
        "Read",
        back_populates="article",
        cascade="all,delete",
    )

    @property
    def can_add_comment(self):
        return len(self.comments) < self.max_comments

    def get_full_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "perex": self.perex,
            "tags": json.loads(self.tags) if self.tags else [],
            "content": self.content,
            "author_id": self.author_id,
            "max_comments": self.max_comments,
            "comments_count": self.comments_count,
            "comments": [comment.get_dict() for comment in self.comments],
            "likes": [like.get_dict() for like in self.likes],
            "reads": [read.get_dict() for read in self.reads],
        }

    def get_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "perex": self.perex,
            "tags": json.loads(self.tags) if self.tags else [],
            "content": self.content,
            "author_id": self.author_id,
            "max_comments": self.max_comments,
            "comments_count": self.comments_count,
            "comments": [comment.id for comment in self.comments],
            "likes": [like.id for like in self.likes],
            "reads": [read.id for read in self.reads],
        }
