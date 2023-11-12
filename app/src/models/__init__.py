from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://mysql:mySuperSecurePassword@db:3306/mySQLdb", echo=True)

class BaseModel(DeclarativeBase):
    pass

from src.models.user import User
from src.models.article import Article
from src.models.comment import Comment
from src.models.like import Like
from src.models.read import Read
from src.models.region import Region
