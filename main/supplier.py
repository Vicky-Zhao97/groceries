from flask import (Blueprint, render_template,
                   request, flash, redirect, url_for, g)
from main.db import call_proc_db
from werkzeug.exceptions import abort
import pymysql

supplier_bp = Blueprint('supplier', __name__, url_prefix='/supplier')


@supplier_bp.route('/<company>')
def home(company):
    supplier = get_supplier(company=company)
    check = request.args.get('check') == '1'
    if supplier is not None:
        products = []
        res = call_proc_db('supplier_product', {company})
        if res is not None:
            products = res
        back = ""
        if check:
            check_supplier(company=company)
            back = "user.manager_login"
        else:
            back = "user.home"
        return render_template('supplier.html', back=back, supplier=supplier, products=products, auth=check)


@supplier_bp.route('/<company>/edit', methods=('GET', 'POST'))
def edit(company):
    check_supplier(company=company)
    supplier = get_supplier(company=company)
    if request.method == 'POST':
        supplier_dict = (request.form['phone'],
                         request.form['address'], company)
        res = call_proc_db("supplier_edit", supplier_dict)
        if res is not None:
            return redirect(url_for('supplier.home', company=company, check='1'))

        flash("Something wrong.")

    return render_template('editSupplier.html', supplier=supplier)


def check_supplier(company):
    if g.manager['company'] != company:
        abort(403)


def get_supplier(company):
    res = call_proc_db('find_supplier', {company})
    if res is not None and len(res) != 0:
        return res[0]
    return None
