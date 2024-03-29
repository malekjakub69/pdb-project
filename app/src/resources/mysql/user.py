from src.models.region import Region
from src.models.user import User
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest
from src.broker.wrapper import TransferObject
from src.broker.broker import publish_to_queue

# class SQLUsersResource(Resource):
#     def get(self):
#         users = User.get_items()
#         return ({"users": [user.get_full_dict() for user in users]}, 200)


class SQLUserResource(Resource):
    # def get(self, user_id: int):
    #     if not (user := User.get_by_id(user_id)):
    #         raise NotFound("entity_not_found")
    #     return ({"user": user.get_dict()}, 200)

    def post(self):
        data = request.get_json()

        if not data["email"] and not data["username"]:
            raise BadRequest("email_or_username_required")

        exist_user = False
        if(data['email']):   
            exist_user = User.get_by_email_or_login(data["email"])
        if(data['username'] and not exist_user):
            exist_user = User.get_by_email_or_login(data["username"])

        if exist_user:
            raise BadRequest("user_exist")

        region_id = data.get("region_id")
        region_iso_code = data.get("region_iso_code")

        if region_id and not Region.get_by_id(region_id):
            raise BadRequest("region_not_found")

        if region_iso_code:
            region = Region.get_by_iso_code(region_iso_code)
            if not region:
                raise BadRequest("region_not_found")
            region_id = region.id

        user = User(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            region_id=region_id if region_id else None,
        )
        user.save()

        transfer_object = TransferObject('insert', 'user', user.get_full_dict())
        publish_to_queue(transfer_object.to_dict(), 'user')

        return ({"user": user.get_full_dict()}, 201)

    def delete(self, user_id: int):
        if not (user := User.get_by_id(user_id)):
            raise NotFound("entity_not_found")
        
        transfer_object = TransferObject('delete', 'user', {'id': user_id})
        publish_to_queue(transfer_object.to_dict(), 'user')

        user.delete()
        return ({"message": "entity_deleted"}, 200)
