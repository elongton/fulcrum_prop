class FulcrumValues:
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def retrieve_fulcrum_values(self, row=None):
        if row == None:
            retrieve_sql = ''' SELECT * FROM fulcrum_values'''
            self.cur.execute(retrieve_sql)
        else:
            retrieve_sql = ''' SELECT * FROM fulcrum_values WHERE id=? '''
            self.cur.execute(retrieve_sql, row)
        return self.cur.fetchall()

    def insert_fulcrum_values_row(self, values):
        insert_sql = ''' INSERT INTO fulcrum_values(calibration, throttleLow, throttleHigh) VALUES(?,?,?) '''
        self.cur.execute(insert_sql, values)
        self.conn.commit()

    def delete_fulcrum_values(self, row=None):
        if row == None:  #deletes all rows with ID > 1
            delete_sql = ''' DELETE FROM fulcrum_values WHERE id>1 '''
            self.cur.execute(delete_sql)
        else: #delets row at id=row
            delete_sql = ''' DELETE FROM fulcrum_values WHERE id=? '''
            self.cur.execute(delete_sql,row)
        self.conn.commit()

    def cleanup_fulcrum_values_table(self):
        fulcrum_value_rows = self.retrieve_fulcrum_values()
        if len(fulcrum_value_rows) > 1:
            self.delete_fulcrum_values()
            print('deleted all rows with ID > 1')
            pass
        elif len(fulcrum_value_rows) < 1:
            self.insert_fulcrum_values_row((0, 0, 0))
            print('added fulcrum_values row to table')
        else:
            pass