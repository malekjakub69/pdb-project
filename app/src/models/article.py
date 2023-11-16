from src.models import db
from src.models.base import BaseModel




class Article(BaseModel):
    __tablename__ = "article"

    title = db.Column(db.String(255), nullable=False)
    perex = db.Column(db.String(512), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="articles")

    comments = db.relationship("Comment", back_populates="article")

    likes = db.relationship("Like", back_populates="article")

    reads = db.relationship("Read", back_populates="article")
