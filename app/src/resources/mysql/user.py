from src.models.region import Region
from src.models.user import User
import json
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest


class SQLUsersResource(Resource):
    def get(self):
        users = User.get_items()
        return ({"users": [user.get_full_dict() for user in users]}, 200)


class SQLUserResource(Resource):
    def get(self, user_id: int):
        if not (user := User.get_by_id(user_id)):
            raise NotFound("entity_not_found")
        return ({"user": user.get_dict()}, 200)

    def post(self):
        data = request.get_json()

        if not data["email"] and not data["username"]:
            raise BadRequest("email_or_username_required")

        exist_user = User.get_by_email_or_login(data["email"] if data["email"] else data["username"])
        if exist_user:
            raise BadRequest("user_exist")

        if "region_id" in data and not Region.get_by_id(data["region_id"]):
            raise BadRequest("entity_not_found")

        user = User(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            region_id=data["region_id"] if "region_id" in data else None,
        )
        user.save()
        return ({"user": user.get_full_dict()}, 201)

    def delete(self, user_id: int):
        if not (user := User.get_by_id(user_id)):
            raise NotFound("entity_not_found")
        user.delete()
        return ({"message": "entity_deleted"}, 200)
