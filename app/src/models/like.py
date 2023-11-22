from src.models import db
from src.models.base import BaseModel


class Like(BaseModel):
    __tablename__ = "like"

    timestamp = db.Column(db.DateTime, default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="likes")

    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    article = db.relationship("Article", back_populates="likes")

    def get_full_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "user": self.user.get_dict(),
            "article": self.article.get_dict(),
        }

    def get_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "user_id": self.user_id,
            "article_id": self.article_id,
        }
