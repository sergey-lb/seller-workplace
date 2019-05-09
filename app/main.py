import csv
import io
import os
import uuid
from pathlib import Path

import waitress
from flask import Flask, render_template, request, url_for, make_response
from werkzeug.utils import redirect

from app.db import Db
from app.product import Product, ProductManager, EmptyProduct
from app.sale import Sale, SaleManager

DATABASE_URL = str(Path(__file__).parent) + '/../db.sqlite'


def start():
    app = Flask(__name__)

    db = Db(DATABASE_URL)

    product_manager = ProductManager(db)
    sale_manager = SaleManager(db)

    product_saved = False

    sale_alert = None;

    sort_field='name'
    sort_order='asc'

    @app.route('/')
    def index():
        nonlocal sort_field, sort_order

        sort_field = request.args.get('sort_field')
        if sort_field not in ['name', 'price', 'quantity']:
            sort_field = 'name'

        sort_order = request.args.get('sort_order')
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        sorting = {
            'column': sort_field,
            'order': sort_order.upper()
        }

        search = request.args.get('search')
        if search:
            products = product_manager.search_by_name(search, sorting)
        else:
            products = product_manager.get_all(sorting)
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
        sales = sale_manager.get_all()
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

        product_manager.update(
            product.id,
            name=product.name,
            quantity=product.quantity,
            price=product.price
        )

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
        for line in reader:
            if line[0] != '':
                product_manager.update(
                    line[0],
                    name = line[1],
                    price = line[2],
                    quantity = line[3]
                )
            else:
                product_manager.add(Product(
                    line[1],
                    price=line[2],
                    quantity=line[3]
                ))
        return redirect(url_for('index'))

    @app.route('/products/export')
    def products_export():
        content = io.StringIO()
        writer = csv.writer(content, delimiter=';')
        sorting = {
            'column': sort_field,
            'order': sort_order.upper()
        }
        products = product_manager.get_all(sorting)
        for product in products:
            writer.writerow([
                product.id,
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
