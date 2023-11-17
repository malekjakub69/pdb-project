from typing import TypeVar
from werkzeug.exceptions import InternalServerError

from src.models import db

T = TypeVar("T", bound="BaseModel")


class BaseModel(db.Model):
    """
    Base model for all database models.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise InternalServerError(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            raise InternalServerError(str(e))
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)