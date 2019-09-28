import sqlite3
from .schema import *
from .fulcrum_values import cleanup_fulcrum_values_table
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print('create_connection error: ')
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print('create_table error: ')
        print(e)

def init():
    conn = create_connection('db/fulcrumprop.db')
    if conn is not None:
        create_table(conn, sql_create_fulcrum_values_table)
        cleanup_fulcrum_values_table()
    else:
        print("Error! cannot create the database connection.")

    # conn.commit()





################
### NOT USED ###
################

