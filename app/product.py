import uuid


class EmptyProduct:
    """

    """
    def __init__(self):
        self.id = uuid.UUID(int=0)
        self.name = ''
        self.price = 0
        self.quantity = 0


class Product:
    """

    """
    def __init__(
            self,
            name,
            *,
            price=0,
            quantity=0
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = int(price)
        self.quantity=int(quantity)


class ProductManager:
    def __init__(self, db):
        self.db = db
        self.table = 'products'

    def add(self, item):
        self.db.insert(self.table, item)

    def update(self, item_id, *, name, price, quantity):
        item = {
            'id': item_id,
            'name': name,
            'price': price,
            'quantity': quantity
        }
        self.db.update(self.table, item)

    def remove_by_id(self, item_id):
        self.db.mark_deleted(self.table, item_id)

    def get_all(self, sorting=None):
        items = self.db.find_all(self.table, sorting)
        items = self._map_items(items)
        return items

    def search_by_name(self, name, sorting=None):
        items = self.db.find_by_column_like(self.table, column='name', value=name, sorting=sorting)
        items = self._map_items(items)
        return items

    def search_by_id(self, item_id):
        item = self.db.find(self.table, item_id)
        item = self._map_item(item)
        return item

    def _map_items(self, items):
        results = []
        for item in items:
            product = self._map_item(item)
            results.append(product)
        return results

    def _map_item(self, item):
        product = Product(
            item['name'],
            price=item['price'],
            quantity=item['quantity']
        )
        product.id = item['id']
        return product
