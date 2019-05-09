from app.sale import Sale, SaleManager
from app.product import Product
from app.test import helpers


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

    db = helpers.get_db()
    sale_manager = SaleManager(db)
    sale_manager.add(sale)

    results = helpers.extract_ids(sale_manager.get_all())

    assert len(results) == 1
    assert sale.id in results
