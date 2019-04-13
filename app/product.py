import uuid

class EmptyProduct:
    """

    """
    def __init__(self):
        self.id = uuid.UUID(int=0)
        self.name = ''
        self.price = ''
        self.quantity = ''


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
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def update(self, item_id, *, name, price, quantity):
        for item in self.items:
            if item.id == item_id:
                item.name = name
                item.price = int(price)
                item.quantity = int(quantity)
                break

    def remove_by_id(self, item_id):
        item = list(filter(lambda o: item_id == o.id, self.items))[0]
        self.items.remove(item)

    def search_by_name(self, name):
        return list(filter(lambda o: name.lower() in o.name.lower(), self.items))

    def search_by_id(self, item_id):
        return list(filter(lambda o: item_id == o.id, self.items))[0]

    def sort_items(self, sort_field, sort_order):
        self.items.sort(key=lambda x: getattr(x, sort_field), reverse=(sort_order == 'desc'))
