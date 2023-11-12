import json
from flask import session
from flask_restful import Resource

from src.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models import engine


class HealthCheckResource(Resource):
    def get(self):
        return "ok", 200


class HealthCheckDatabaseResource(Resource):
    def get(self):
        try:
            # to check database we will execut
            session = Session(engine)
            newUser = User(
                username="test",
                email="test@test.cz",
                first_name="test",
                last_name="test",
            )
            session.add(newUser)
            session.commit()

            user = session.execute(select(User).where(User.username == "test").first())

            session.delete(user)
            session.commit()

        except Exception as e:
            output = str(e)
            return output, 400

        return json.dumps(user.all()), 200
