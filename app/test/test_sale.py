from app.sale import Sale, SaleManager
from app.product import Product


def test_create_sale():
    product = Product(
        'Сплит-система Comfee MSAFA-07HRN1-QC2',
        price=12_990,
        quantity=100
    )
    quantity = 10

    sale = Sale(
        product,
        quantity
    )

    assert sale.product_id == product.id
    assert sale.name == product.name
    assert sale.price == product.price
    assert sale.quantity == quantity


def test_sale_manager_add():
    product = Product(
        'Сплит-система Comfee MSAFA-07HRN1-QC2',
        price=12_990,
        quantity=100
    )
    quantity = 10

    sale = Sale(
        product,
        quantity
    )

    sale_manager = SaleManager()
    sale_manager.add(sale)

    assert len(sale_manager.items) == 1
    assert sale in sale_manager.items
