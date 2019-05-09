import uuid
from app.product import Product

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
        items = self._map_items(items)
        return items

    def _map_items(self, items):
        results = []
        for item in items:
            sale = self._map_item(item)
            results.append(sale)
        return results

    def _map_item(self, item):

        product = Product(
            item['name'],
            price=item['price']
        )
        product.id = item['product_id']

        sale = Sale(
            product,
            quantity=item['quantity']
        )
        sale.id = item['id']
        return sale
