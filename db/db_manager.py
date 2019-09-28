import sqlite3
from .schema import *
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print('create_connection error: ')
        print(e)

def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print('create_table error: ')
        print(e)

def insert_update_fulcrum_value_row(conn, items):
    insert_fulcrum_values_sql = ''' INSERT INTO fulcrum_values(calibration, throttleLow, throttleHigh) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(insert_fulcrum_values_sql, items)
    print(cur.lastrowid)
    return cur.lastrowid


def init():
    myvalues = (90.12, 4000, 6500)
    conn = create_connection('db/fulcrumprop.db')
    if conn is not None:
        create_table(conn, sql_create_fulcrum_values_table)
        insert_update_fulcrum_value_row(conn, myvalues)
    else:
        print("Error! cannot create the database connection.")
