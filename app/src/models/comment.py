from src.models import db
from src.models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = "comment"

    country_name = db.Column(db.String(4096), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="comments")

    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    article = db.relationship("Article", back_populates="comments")