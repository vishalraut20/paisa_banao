import json
from exception import exceptions
from entity import entity
from dao import request_dao
import logging

logger = logging.getLogger(__name__)


class RequestService():

    def __init__(self):
         self.tips_dao = request_dao.RequestDao()

    def validate_and_add_tip(self, tips):
        tip_entity = self.validate_tips(tips)
        self.tips_dao.add_tips_to_db(tip_entity)
        return tip_entity

    def validate_tips(self, tips):
        if not tips:
            exceptions.InvalidRequestException("Please provide tips")
        tips_request = json.loads(tips)
        print("Request body json to update {}".format(tips_request))
        items_to_validate = ["stock_name", "entry_price", "exit_price"]
        for item in items_to_validate:
            if item not in tips_request:
                raise exceptions.InvalidRequestException(
                    "tip should contain {}". format(item))
        item_entity = entity.Tips(
            tips_request.get("stock_name"),
            tips_request.get("entry_price"),
            tips_request.get("exit_price"))
        return item_entity.__dict__

    def get_list_of_tips(self):
        tips_list = self.tips_dao.get_tips_from_db()
        items = tips_list["Items"]
        print("tips from DB {}".format(items))
        return {"items": items}

    def get_tip_by_id(self, tip_id):
        tip = self.tips_dao.get_tips_by_id_from_db(tip_id)
        return tip

    def remove_tip_by_id(self, tip_id):
        self.tips_dao.remove_tip(tip_id)
