import sqlite3
from .schema import *
from .throttle_angle_values import FulcrumValues
from sqlite3 import Error

class DBManager(FulcrumValues):
    def __init__(self):
        self.conn = self.create_connection('database/db/fulcrumprop.db')
        self.cur = self.conn.cursor()
        super().__init__(self.conn)
        self.create_table(sql_create_fulcrum_values_table)
        self.cleanup_fulcrum_values_table()

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print('create_connection error: ')
            print(e)
        return conn

    def create_table(self, create_table_sql):
        try:
            self.cur.execute(create_table_sql)
        except Error as e:
            print('create_table error: ')
            print(e)

    # def init():
    #     if conn is not None:
            
    #         cleanup_fulcrum_values_table(conn)
    #     else:
    #         print("Error! cannot create the database connection.")

