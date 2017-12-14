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
        tips_arr = self.validate_tips(tips)
        self.tips_dao.add_tips_to_db(tips_arr)
        result = {"stock_list": tips_arr}
        return result

    def validate_tips(self, tips):
        if not tips:
            exceptions.InvalidRequestException("Please provide tips")
        tips_arr = []
        tips_request_arr = json.loads(tips)
        print("Request body json to update {}".format(tips_request_arr))
        items_to_validate = ["stock_name", "entry_price", "exit_price"]
        for tip in tips_request_arr:
            for item in items_to_validate:
                if item not in tip:
                    raise exceptions.InvalidRequestException(
                        "tip should contain {}". format(item))
            item_entity = entity.Tips(
                tip.get("stock_name"),
                tip.get("entry_price"),
                tip.get("exit_price"))
            tips_arr.append(item_entity.__dict__)
        return tips_arr

    def get_list_of_tips(self):
        tips_list = self.tips_dao.get_tips_from_db()
        items = tips_list["Items"]
        print("tips from DB {}".format(items))
        return {"items": items}

