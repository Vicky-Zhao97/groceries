from flask import (Blueprint, render_template,
                   request, flash, redirect, url_for, g)
from main.db import (query_db, insert_db, update_db, delete_db, call_proc_db)
from werkzeug.exceptions import abort
import pymysql

product_bp = Blueprint('product', __name__, url_prefix='/product')


@product_bp.route('/<product_id>')
def detail(product_id):
    product = getProduct(product_id=product_id)
    if product is not None:
        return render_template('product.html', product=product)


@product_bp.route('/edit/<product_id>', methods=('GET', 'POST'))
def edit(product_id):
    product = getProduct(product_id=product_id)
    company = g.manager['company']
    if product is None or product['company'] != company:
        abort(403)
    if request.method == 'POST':
        product_dict = (request.form['name'], request.form['desc'],
                        request.form['price'], request.form['origin'], product_id)
        res = call_proc_db('update_product', product_dict)
        if res is not None:
            return redirect(url_for('supplier.home', company=company, check='1'))
        flash("Something wrong")

    return render_template('editProduct.html', add=False, product=product)


@product_bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        company = g.manager['company']
        product_dict = (request.form['name'], request.form['desc'], request.form['price'],
                        request.form['origin'], request.form['genre'], company)
        res = call_proc_db('insert_product', product_dict)
        if res is not None:
            return redirect(url_for('supplier.home', company=company, check='1'))
        flash("Something wrong")

    return render_template('editProduct.html', add=True, product={})


@product_bp.route('/delete/<product_id>')
def delete(product_id):
    product = getProduct(product_id=product_id)
    company = g.manager['company']
    if product['company'] != company:
        abort(403)
    res = call_proc_db('delete_product', {product_id})
    if res is None:
        flash("Something wrong")

    return redirect(url_for('supplier.home', company=company, check='1'))


def getProduct(product_id):
    res = call_proc_db('find_product_by_id', {product_id})
    if res is not None and len(res) != 0:
        return res[0]
    return None
