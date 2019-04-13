import csv
import io
import os
import uuid

import waitress
from flask import Flask, render_template, request, url_for, make_response
from werkzeug.utils import redirect

from app.product import Product, ProductManager, EmptyProduct
from app.sale import Sale, SaleManager


def start():
    app = Flask(__name__)

    product_manager = ProductManager()

    product_manager.add(Product(
        'Сплит-система Comfee MSAFA-07HRN1-QC2',
        price=12_990,
        quantity=1
    ))

    product_manager.add(Product(
        'Сплит-система Haier HSU-09HTM03/R2',
        price=22_490,
        quantity=24
    ))

    product_manager.add(Product(
        'Сплит-система (инвертор) LG P07EP2',
        price=33_990,
        quantity=1
    ))

    product_manager.add(Product(
        'Сплит-система (инвертор) Haier AS09NA6HRA-S',
        price=27_990,
        quantity=24
    ))

    product_manager.add(Product(
        'Сплит-система (инвертор) Comfee MSAFA-09HRDN1-QC2F',
        price=22_990,
        quantity=2
    ))

    product_manager.add(Product(
        'Сплит-система (инвертор) LG PM09SP',
        price=34_990,
        quantity=6
    ))

    product_manager.add(Product(
        'Сплит-система Comfee MSAFB-12HRN1-QC2',
        price=20_990,
        quantity=1
    ))

    sale_manager = SaleManager()

    product_saved = False

    sale_alert = None;

    @app.route('/')
    def index():

        sort_field = request.args.get('sort_field')
        if sort_field not in ['name', 'price', 'quantity']:
            sort_field = 'name'

        sort_order = request.args.get('sort_order')
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        product_manager.sort_items(sort_field, sort_order)

        search = request.args.get('search')
        if search:
            products = product_manager.search_by_name(search)
        else:
            products = product_manager.items
            search=''

        empty_id = uuid.UUID(int=0)

        return render_template(
            'index.html',
            products=products,
            empty_id=empty_id,
            search=search,
            sort_field=sort_field,
            sort_order=sort_order
        )

    @app.route('/products/<product_id>/edit')
    def product_edit(product_id):
        nonlocal product_saved

        empty_id = str(uuid.UUID(int=0))
        if product_id == empty_id:
            product = EmptyProduct()
        else:
            product = product_manager.search_by_id(product_id)

        is_saved = product_saved
        product_saved = False
        return render_template('product-edit.html', product=product, is_saved=is_saved)

    @app.route('/products/<product_id>/save', methods=['POST'])
    def product_save(product_id):
        nonlocal product_saved

        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']

        empty_id = str(uuid.UUID(int=0))
        if product_id == empty_id:
            product = Product(name, price=price, quantity=quantity)
            product_manager.add(product)
            product_id=product.id
        else:
            product_manager.update(product_id, name=name, price=price, quantity=quantity)

        product_saved = True
        return redirect(url_for('product_edit', product_id=product_id))

    @app.route('/products/<product_id>/remove')
    def product_remove(product_id):
        product_manager.remove_by_id(product_id)
        return redirect(url_for('index'))

    @app.route('/products/<product_id>/sale')
    def product_sale(product_id):
        nonlocal sale_alert

        alert = sale_alert
        sale_alert = None

        product = product_manager.search_by_id(product_id)
        return render_template('product-sale.html', product=product, alert=alert)

    @app.route('/sales')
    def sales():
        sales = sale_manager.items
        return render_template('sales.html', sales=sales)

    @app.route('/sales/add', methods=['POST'])
    def sale_add():
        nonlocal sale_alert

        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        product = product_manager.search_by_id(product_id)

        if quantity == 0:
            sale_alert = {
                'class': 'danger',
                'msg': 'Кол-во должно быть больше 0'
            }
            return redirect(url_for('product_sale', product_id=product.id))

        if quantity > product.quantity:
            sale_alert = {
                'class': 'danger',
                'msg': 'Недостаточно товара на складе'
            }
            return redirect(url_for('product_sale', product_id=product.id))

        product.quantity -= quantity

        sale = Sale(
            product,
            quantity
        )
        sale_manager.add(sale)
        sale_alert = {
            'class': 'success',
            'msg': 'Продажа проведена'
        }

        return redirect(url_for('product_sale', product_id=product.id))

    @app.route('/products/import', methods=['POST'])
    def products_import():
        nonlocal product_manager
        if 'import-file' not in request.files:
            redirect(url_for('index'))

        importFile = request.files['import-file']
        content = io.StringIO(importFile.read().decode("utf8"))
        reader = csv.reader(content, delimiter=';')
        product_manager = ProductManager()
        for line in reader:
            product_manager.add(Product(
                line[0],
                price=line[1],
                quantity=line[2]
            ))
        return redirect(url_for('index'))

    @app.route('/products/export')
    def products_export():
        content = io.StringIO()
        writer = csv.writer(content, delimiter=';')
        products = product_manager.items
        for product in products:
            writer.writerow([
                product.name,
                product.price,
                product.quantity
            ])
        response = make_response(content.getvalue())
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'inline; filename=exported.csv'
        return response

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9876, debug=True)


if __name__ == '__main__':
    start()
