from src.models.region import Region
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest
from src.broker.broker import publish_to_queue
from src.broker.wrapper import TransferObject

class SQLRegionsResource(Resource):
    def get(self):
        regions = Region.get_items()
        return ({"regions": [region.get_full_dict() for region in regions]}, 201)


class SQLRegionResource(Resource):
    def get(self, region_id: int):
        if not (region := Region.get_by_id(region_id)):
            raise NotFound("entity_not_found")
        return ({"user": region.get_dict()}, 200)

    def post(self):
        data = request.get_json()

        if not data["iso_code"]:
            raise BadRequest("iso_code_required")

        exists_region = Region.get_by_iso_code(data["iso_code"])
        if exists_region:
            raise BadRequest("region_exists")

        region = Region(
            iso_code=data["iso_code"],
            country_name=data["country_name"]
        )
        region.save()

        transfer_object = TransferObject('insert', 'region', region.get_full_dict())
        publish_to_queue(transfer_object.to_dict(), 'region')

        return ({"user": region.get_full_dict()}, 201)

    def delete(self, region_id: int):
        if not (region := Region.get_by_id(region_id)):
            raise NotFound("entity_not_found")
        region.delete()

        transfer_object = TransferObject('delete', 'region', {'id': region_id})
        publish_to_queue(transfer_object.to_dict(), 'region')

        return "entity_deleted", 204