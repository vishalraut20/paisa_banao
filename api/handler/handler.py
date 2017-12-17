import json
from service import request_service
from http import HTTPStatus
import logging

logger = logging.getLogger(__name__)


def add_tips(event, context):
    tip_service = request_service.RequestService()
    request_param = event["body"]
    result = tip_service.validate_and_add_tip(request_param)
    return {
        "statusCode": HTTPStatus.OK.value,
        "body": json.dumps(result)
    }


def get_list_of_tips(event, context):
    tip_service = request_service.RequestService()
    result = tip_service.get_list_of_tips()
    return {
        "statusCode": HTTPStatus.OK.value,
        "body": json.dumps(result)
    }

def get_tip_by_id(event, context):
    tip_service = request_service.RequestService()
    result = tip_service.get_tip_by_id(event["pathParam"]["tip_id"])
    return {
        "statusCode": HTTPStatus.OK.value,
        "body": json.dumps(result)
    }

def delete_tip_by_id(event, context):
    tip_service = request_service.RequestService()
    tip_service.remove_tip_by_id(event["pathParam"]["tip_id"])
    return{
        "statusCode": HTTPStatus.OK.value
    }