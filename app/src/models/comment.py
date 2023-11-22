from src.models import db
from src.models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = "comment"

    country_name = db.Column(db.String(4096), nullable=False)
    comment = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="comments")

    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    article = db.relationship("Article", back_populates="comments")

    def get_full_dict(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "author": self.author.get_dict(),
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "article": self.article.get_dict(),
            "country_name": self.country_name,
        }

    def get_dict(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "author_id": self.author_id,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "article_id": self.article_id,
            "country_name": self.country_name,
        }
