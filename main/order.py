from flask import (Blueprint, session, render_template,
                   redirect, url_for, flash)
from main.db import call_proc_db

order_bp = Blueprint('order', __name__, url_prefix='/order')


@order_bp.route('/addCart/<product_id>')
def addCart(product_id):
    cusername = session.get('customer_username')
    res = call_proc_db("add_cart", (cusername, product_id))
    if res is not None:
        return redirect(url_for('order.cart'))

    flash("Add wrong!")
    return redirect(url_for('product.detail', product_id))


@order_bp.route('/cart')
def cart():
    cusername = session.get('customer_username')
    order = ()
    products = []
    res = call_proc_db('get_cart', {cusername})
    if res is not None and len(res) != 0:
        order = res[0]
        res2 = call_proc_db(
            'get_order_detail', (str(order.get('order_id'))))
        if res2 is not None:
            products = res2
    return render_template('cart.html', order=order, products=products)


@order_bp.route('/deleteCartProduct/<product_id>')
def deleteCartProduct(product_id):
    cusername = session.get('customer_username')
    cartres = call_proc_db('get_cart', {cusername})
    res = None
    if cartres is not None or len(cartres) != 0:
        cart = cartres[0]
        res = call_proc_db('delete_cart_product',
                           (cart.get('order_id'), product_id))
    if res is None:
        flash("Delete failed.")

    return redirect(url_for('order.cart'))


@order_bp.route('/updateCart/<product_id>/<quantity>')
def updateCart(product_id, quantity):
    cusername = session.get('customer_username')
    cartres = call_proc_db('get_cart', {cusername})
    res = None
    if cartres is not None or len(cartres) != 0:
        cart = cartres[0]
        res = call_proc_db('update_cart_product',
                           (cart.get('order_id'), product_id, quantity))
    if res is None:
        flash("Update failed.")

    return redirect(url_for('order.cart'))


@order_bp.route('/placeOrder')
def placeOrder():
    cusername = session.get('customer_username')
    res = call_proc_db('place_order', {cusername})
    if res is not None:
        return redirect(url_for('user.home'))

    flash("Something wrong.")
    return redirect(url_for('order.cart'))


@order_bp.route('/customer')
def customer():
    cusername = session.get('customer_username')
    orders = []
    res = call_proc_db('get_customer_orders', {cusername})
    if res is not None:
        orders = res
    return render_template('order.html', orders=orders)


@order_bp.route('/detail/<order_id>')
def detail(order_id):
    order = ()
    products = []
    res1 = call_proc_db('get_order', {order_id})
    if res1 is not None:
        order = res1[0]
        res2 = call_proc_db('get_order_detail', (str(order.get('order_id'))))
        if res2 is not None:
            products = res2
    return render_template('order_detail.html', order=order, products=products)


@order_bp.route('/delete/<customer>/<order_id>')
def delete(customer, order_id):
    error = None
    if customer != session['customer_username']:
        error = "Can not delete."
    if error is None:
        call_proc_db('delete_order', {order_id})

    return redirect(url_for('order.customer'))
