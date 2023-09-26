from flask import (Blueprint, render_template,
                   request, flash, redirect, url_for, session, g)
from main.db import call_proc_db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.before_app_request
def load_logged_in_user():
    load_customer()
    load_manager()


@user_bp.route('/customer_login', methods=('GET', 'POST'))
def customer_login():
    if 'customer_username' in session and session['customer_username'] is not None:
        return redirect(url_for('user.home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        customer = call_proc_db('login_customer', (username, password))
        if customer is None or len(customer) == 0:
            error = "Incorrect information."
        else:
            session.clear()
            session['customer_username'] = customer[0]['username']
            load_customer()
            return redirect(url_for('user.home'))

        flash(error)

    return render_template('login_customer.html')


@user_bp.route('/customer_logout')
def customer_logout():
    session.clear()
    return redirect(url_for('hello'))


@user_bp.route('/customer_register', methods=('GET', 'POST'))
def customer_register():
    if request.method == 'POST':
        customer_dict = (request.form['username'],
                         request.form['password'],
                         request.form['fullname'],
                         request.form['phone'],
                         request.form['email'],
                         request.form['address'])
        res = call_proc_db('register_customer', customer_dict)
        if res is not None:
            return redirect(url_for("user.customer_login"))
        flash("Something wrong.")

    return render_template('register_customer.html')


@user_bp.route('/customer_edit', methods=('GET', 'POST'))
def customer_edit():
    if request.method == 'POST':
        customer_dict = (request.form['password'], request.form['fullname'],
                         request.form['phone'], request.form['email'],
                         request.form['address'], session['customer_username'])
        res = call_proc_db('edit_customer', customer_dict)
        if res is not None:
            load_customer()
            return redirect(url_for('user.home'))

        flash("Something wrong.")

    return render_template('customerProfile.html')


@user_bp.route('/home')
def home():
    product = request.args.get('product', '')
    genre = request.args.get('genre', '')
    supplier = request.args.get('supplier', '')
    products = []
    res = call_proc_db('search_product', (product, genre, supplier))
    if res is not None:
        products = res
    return render_template('home_customer.html', products=products)


@user_bp.route('/manager_register', methods=('GET', 'POST'))
def manager_register():
    if request.method == 'POST':
        manager_dict = (request.form['employeeID'], request.form['password'],
                        request.form['fullname'],
                        request.form['phone'],
                        request.form['email'],
                        request.form['company']
                        )
        res = call_proc_db("register_manager", manager_dict)
        if res is not None:
            return redirect(url_for("user.manager_login"))

        flash("Something wrong.")

    return render_template('managerRegister.html')


@user_bp.route('/manager_login', methods=('GET', 'POST'))
def manager_login():
    if 'employee_id' in session and session['employee_id'] is not None:
        return render_template('managerHome.html')

    if request.method == 'POST':
        id = request.form['employeeID']
        password = request.form['password']
        error = None
        manager = call_proc_db('login_manager', (id, password))
        if manager is None or len(manager) == 0:
            error = "Incorrect information."
        else:
            session.clear()
            session['employee_id'] = manager[0]['employee_id']
            load_manager()
            return render_template('managerHome.html')

        flash(error)

    return render_template('login_manager.html')


@user_bp.route('/manager_logout')
def manager_logout():
    session.pop('employee_id')
    return redirect(url_for('hello'))


@user_bp.route('/manager_edit', methods=('GET', 'POST'))
def manager_edit():
    if request.method == 'POST':
        manager_dict = (request.form['password'],
                        request.form['fullname'],
                        request.form['phone'],
                        request.form['email'],
                        session['employee_id']
                        )
        res = call_proc_db('edit_manager', manager_dict)
        if res is not None:
            load_manager()
            return render_template('managerHome.html')
        flash("Something wrong.")

    return render_template('editManager.html')


def load_customer():
    cusername = session.get('customer_username')
    if cusername is None:
        g.customer = None
    else:
        res = call_proc_db('customer_load', {cusername})
        if res is not None and len(res) != 0:
            g.customer = res[0]


def load_manager():
    memployeeId = session.get('employee_id')
    if memployeeId is None:
        g.manager = None
    else:
        res = call_proc_db('manager_load', {memployeeId})
        if res is not None and len(res) != 0:
            g.manager = res[0]
