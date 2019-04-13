class Sale:
    """

    """
    def __init__(
            self,
            product,
            quantity=0
    ):
        self.name = product.name
        self.price = product.price
        self.quantity=quantity


class SaleManager:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
