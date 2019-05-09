import uuid


class Sale:
    """

    """
    def __init__(
            self,
            product,
            quantity=0
    ):
        self.id = str(uuid.uuid4())
        self.product_id = product.id
        self.name = product.name
        self.price = product.price
        self.quantity=quantity


class SaleManager:
    def __init__(self, db):
        self.db = db
        self.table = 'sales'

    def add(self, item):
        self.db.insert(self.table, item)

    def get_all(self):
        items = self.db.find_all(self.table)
        return items