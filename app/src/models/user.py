from src.models import db
from src.models.base import BaseModel



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
