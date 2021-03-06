from entity import entity
import boto3
import os


class RequestDao:

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(os.environ["DATABASE_NAME"])

    def add_tips_to_db(self, tip):
        print("tip to store is {}".format(tip))
        self.table.put_item(Item=tip)

    def get_tips_from_db(self):
        return self.table.scan()

    def get_tips_by_id_from_db(self, tip_id):
        return self.table.get_item(Key={'id': tip_id})

    def remove_tip_by_id(self, tip_id):
        self.table.delete_item(Key={'id': tip_id})