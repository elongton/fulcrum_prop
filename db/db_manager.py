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
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print('create_table error: ')
        print(e)

# def add_update_fulcrum_value_row(conn, insert_fulcrum_values_sql):
#     try:
#         c = conn.cursor()
#         c.execute(insert_fulcrum_values_sql, )


def init():
    conn = create_connection('db/fulcrumprop.db')
    if conn is not None:
        create_table(conn, sql_create_fulcrum_values_table)
    else:
        print("Error! cannot create the database connection.")
