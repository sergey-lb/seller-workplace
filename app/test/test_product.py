import uuid

from app.product import Product, ProductManager, EmptyProduct


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
    manager = ProductManager()
    product = Product('Сплит-система Comfee MSAFA-07HRN1-QC2', price=12_990, quantity=1)

    manager.add(product)

    assert len(manager.items) == 1
    assert product in manager.items


def test_product_manager_update():
    manager = ProductManager()
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
    manager = ProductManager()
    product = Product('Сплит-система Comfee MSAFA-07HRN1-QC2', price=12_990, quantity=1)

    manager.add(product)
    manager.remove_by_id(product.id)

    assert len(manager.items) == 0


def test_product_manager_search_by_name():
    product_manager = ProductManager()

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

    expected = [lg_p_07, lg_pm_09]

    results = product_manager.search_by_name('lg')

    assert expected == results


def test_product_manager_search_by_id():
    product_manager = ProductManager()

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

    assert result == lg_pm_09


def test_product_manager_sort_items():
    product_manager = ProductManager()

    product_a = Product(
        'А',
        price=10,
        quantity=1
    )

    product_b = Product(
        'Б',
        price=1,
        quantity=100
    )

    product_c = Product(
        'В',
        price=100,
        quantity=10
    )

    product_manager.add(product_b)
    product_manager.add(product_a)
    product_manager.add(product_c)

    expected_name_asc = [product_a, product_b, product_c]
    expected_name_desc = [product_c, product_b, product_a]
    expected_price_asc = [product_b, product_a, product_c]
    expected_price_desc = [product_c, product_a, product_b]
    expected_quantity_asc = [product_a, product_c, product_b]
    expected_quantity_desc = [product_b, product_c, product_a]

    product_manager.sort_items('name', 'asc')
    assert expected_name_asc == product_manager.items

    product_manager.sort_items('name', 'desc')
    assert expected_name_desc == product_manager.items

    product_manager.sort_items('price', 'asc')
    assert expected_price_asc == product_manager.items

    product_manager.sort_items('price', 'desc')
    assert expected_price_desc == product_manager.items

    product_manager.sort_items('quantity', 'asc')
    assert expected_quantity_asc == product_manager.items

    product_manager.sort_items('quantity', 'desc')
    assert expected_quantity_desc == product_manager.items
