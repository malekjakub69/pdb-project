from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    from src.models.user import User
    from src.models.article import Article
    from src.models.comment import Comment
    from src.models.like import Like
    from src.models.read import Read
    from src.models.region import Region
