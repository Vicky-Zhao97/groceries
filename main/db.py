import pymysql
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host=current_app.config['MYSQL_HOST'],
                               user=current_app.config['MYSQL_USER'],
                               password=current_app.config['MYSQL_PASSWORD'],
                               database=current_app.config['MYSQL_DATABSE'],
                               cursorclass=pymysql.cursors.DictCursor)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    results = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()
    return results


def insert_db(table, data):
    db = get_db()
    cursor = db.cursor()
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = "INSERT INTO {} ({}) VALUES ({})".format(
        table, columns, placeholders)
    cursor.execute(sql, list(data.values()))
    db.commit()
    cursor.close()


def update_db(table, data, condition):
    db = get_db()
    cursor = db.cursor()
    placeholders = ', '.join(['{}=%s'.format(k) for k in data.keys()])
    sql = "UPDATE {} SET {} WHERE {}".format(table, placeholders, condition)
    cursor.execute(sql, list(data.values()))
    db.commit()
    cursor.close()


def delete_db(table, condition):
    db = get_db()
    cursor = db.cursor()
    sql = "DELETE FROM {} WHERE {}".format(table, condition)
    cursor.execute(sql)
    db.commit()
    cursor.close()


def call_proc_db(proc_name, args=()):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.callproc(proc_name, args)
        result = cursor.fetchall()
        db.commit()
        cursor.close()
        return result
    except pymysql.err.Error as e:
        print(str(e))
        return None
