import uuid
from datetime import datetime

class Tips:
    def __init__(self, stock_name, entry_price, exit_price):
        self.stock_name = stock_name
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.id = str(uuid.uuid4())
        self.time = str(datetime.now())