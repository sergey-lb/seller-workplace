import uuid

from app.product import Product, ProductManager, EmptyProduct
from app.test import helpers


def test_create_empty_product():
    product = EmptyProduct()
    empty_id = uuid.UUID(int=0)

    assert product.id == empty_id
    assert product.name == ''
    assert product.price == 0
    assert product.quantity == 0


def test_create_product():
    name = 'Сплит-система Comfee MSAFA-07HRN1-QC2'
    data = {
        'price': 12_990,
        'quantity': 1
    }

    product = Product(name, **data)

    assert product.name == name
    for key, val in data.items():
        assert getattr(product, key) == val


def test_product_manager_add():

    db = helpers.get_db()

    manager = ProductManager(db)
    product = Product('Сплит-система Comfee MSAFA-07HRN1-QC2', price=12_990, quantity=1)

    manager.add(product)

    items = manager.get_all()
    assert len(items) == 1
    assert product.id == items[0].id
    assert product.name == items[0].name
    assert product.price == items[0].price
    assert product.quantity == items[0].quantity


def test_product_manager_update():
    db = helpers.get_db()

    manager = ProductManager(db)
    product = Product('Сплит-система Comfee MSAFA-07HRN1-QC2', price=12_990, quantity=1)

    data = {
        'name': 'test name',
        'price': 10,
        'quantity': 100
    }

    manager.add(product)
    manager.update(product.id, **data)

    updated_product = manager.search_by_id(product.id)

    assert updated_product.name == data['name']
    assert updated_product.price == data['price']
    assert updated_product.quantity == data['quantity']


def test_product_manager_remove_by_id():
    db = helpers.get_db()

    manager = ProductManager(db)
    product = Product('Сплит-система Comfee MSAFA-07HRN1-QC2', price=12_990, quantity=1)

    manager.add(product)
    manager.remove_by_id(product.id)

    assert len(manager.get_all()) == 0


def test_product_manager_search_by_name():
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

    expected = [lg_p_07.id, lg_pm_09.id]
    expected.sort()

    results = helpers.extract_ids(product_manager.search_by_name('lg'))
    results.sort()

    assert expected == results


def test_product_manager_search_by_id():
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

    result = product_manager.search_by_id(lg_pm_09.id)

    assert result.id == lg_pm_09.id


def test_product_manager_sorting():
    db = helpers.get_db()

    product_manager = ProductManager(db)

    product_a = Product(
        'АА',
        price=10,
        quantity=1
    )

    product_b = Product(
        'БА',
        price=1,
        quantity=100
    )

    product_c = Product(
        'ВА',
        price=100,
        quantity=10
    )

    product_manager.add(product_b)
    product_manager.add(product_a)
    product_manager.add(product_c)

    sorting_name_asc = {'column': 'name', 'order': 'ASC'}
    sorting_name_desc = {'column': 'name', 'order': 'DESC'}
    sorting_price_asc = {'column': 'price', 'order': 'ASC'}
    sorting_price_desc = {'column': 'price', 'order': 'DESC'}
    sorting_quantity_asc = {'column': 'quantity', 'order': 'ASC'}
    sorting_quantity_desc = {'column': 'quantity', 'order': 'DESC'}

    expected_name_asc = [product_a.id, product_b.id, product_c.id]
    expected_name_desc = [product_c.id, product_b.id, product_a.id]
    expected_price_asc = [product_b.id, product_a.id, product_c.id]
    expected_price_desc = [product_c.id, product_a.id, product_b.id]
    expected_quantity_asc = [product_a.id, product_c.id, product_b.id]
    expected_quantity_desc = [product_b.id, product_c.id, product_a.id]

    items = helpers.extract_ids(product_manager.get_all(sorting_name_asc))
    assert expected_name_asc == items
    items = helpers.extract_ids(product_manager.search_by_name('А', sorting_name_asc))
    assert expected_name_asc == items

    items = helpers.extract_ids(product_manager.get_all(sorting_name_desc))
    assert expected_name_desc == items
    items = helpers.extract_ids(product_manager.search_by_name('А', sorting_name_desc))
    assert expected_name_desc == items

    items = helpers.extract_ids(product_manager.get_all(sorting_price_asc))
    assert expected_price_asc == items
    items = helpers.extract_ids(product_manager.search_by_name('А', sorting_price_asc))
    assert expected_price_asc == items

    items = helpers.extract_ids(product_manager.get_all(sorting_price_desc))
    assert expected_price_desc == items
    items = helpers.extract_ids(product_manager.search_by_name('А', sorting_price_desc))
    assert expected_price_desc == items

    items = helpers.extract_ids(product_manager.get_all(sorting_quantity_asc))
    assert expected_quantity_asc == items
    items = helpers.extract_ids(product_manager.search_by_name('А', sorting_quantity_asc))
    assert expected_quantity_asc == items

    items = helpers.extract_ids(product_manager.get_all(sorting_quantity_desc))
    assert expected_quantity_desc == items
    items = helpers.extract_ids(product_manager.search_by_name('А', sorting_quantity_desc))
    assert expected_quantity_desc == items
