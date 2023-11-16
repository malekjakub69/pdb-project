import json
from flask_restful import Resource

from src.models.user import User


class HealthCheckResource(Resource):
    def get(self):
        return "ok", 200


class HealthCheckDatabaseResource(Resource):
    """
    Resource for checking the health of the database.
    Attempts to create a new role, retrieve it, and delete it.
    Returns a success message if the database is working properly.
    """

    def get(self):
        try:
            new_user = User(first_name="test", last_name="test2", email="test@test.cz")
            new_user.save()

            user = User.query.filter_by(email="test@test.cz").first()

            user.delete()

        except Exception as e:
            output = str(e)
            return output, 400

        return json.dumps("Db works"), 200
