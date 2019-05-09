from app.product import ProductManager, Product
from app.test import helpers


def test_db_invalid_table_exception():
    db = helpers.get_db()
    try:
        db.validate_table_or_column_name('#&^')
        assert False
    except:
        assert True


def test_db_find_by_column():
    db = helpers.get_db()

    product_manager = ProductManager(db)

    comfee_msafa_07 = Product(
        'Сплит-система Comfee MSAFA-07HRN1-QC2',
        price=12_990,
        quantity=1
    )
    product_manager.add(comfee_msafa_07)

    haier_hsu_09 = Product(
        'Сплит-система Haier HSU-09HTM03/R2',
        price=22_490,
        quantity=24
    )
    product_manager.add(haier_hsu_09)

    lg_p_07 = Product(
        'Сплит-система (инвертор) LG P07EP2',
        price=33_990,
        quantity=1
    )
    product_manager.add(lg_p_07)

    haier_as_09 = Product(
        'Сплит-система (инвертор) Haier AS09NA6HRA-S',
        price=27_990,
        quantity=24
    )
    product_manager.add(haier_as_09)

    comfee_msafa_09 = Product(
        'Сплит-система (инвертор) Comfee MSAFA-09HRDN1-QC2F',
        price=22_990,
        quantity=2
    )
    product_manager.add(comfee_msafa_09)

    lg_pm_09 = Product(
        'Сплит-система (инвертор) LG PM09SP',
        price=34_990,
        quantity=6
    )
    product_manager.add(lg_pm_09)

    comfee_msafb_12 = Product(
        'Сплит-система Comfee MSAFB-12HRN1-QC2',
        price=20_990,
        quantity=1
    )
    product_manager.add(comfee_msafb_12)

    expected = lg_p_07

    results = helpers.extract_ids(db.find_by_column(
        product_manager.table,
        column='name',
        value='Сплит-система (инвертор) LG P07EP2'
    ))

    assert expected.id in results


def test_db_delete():
    db = helpers.get_db()

    manager = ProductManager(db)
    product = Product('Сплит-система Comfee MSAFA-07HRN1-QC2', price=12_990, quantity=1)

    manager.add(product)
    before_deletion = manager.get_all()
    db.delete(manager.table, product.id)
    after_deletion = manager.get_all()

    assert len(before_deletion) == 1
    assert len(after_deletion) == 0


def test_db_update_with_object():
    db = helpers.get_db()

    manager = ProductManager(db)
    product = Product('Сплит-система Comfee MSAFA-07HRN1-QC2', price=12_990, quantity=1)

    manager.add(product)

    product.name = 'test name'
    product.price = 10
    product.quantity = 100

    db.update(manager.table, product)

    updated_product = manager.search_by_id(product.id)

    assert updated_product.name == product.name
    assert updated_product.price == product.price
    assert updated_product.quantity == product.quantity
