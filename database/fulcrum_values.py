class FulcrumValues:
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def retrieve_fulcrum_values(self, id=None):
        if id == None:
            retrieveSQL = ''' SELECT * FROM fulcrum_values'''
            self.cur.execute(retrieveSQL)
            return self.cur.fetchall()
        else:
            retrieveSQL = ''' SELECT * FROM fulcrum_values WHERE id=? '''
            self.cur.execute(retrieveSQL, str(id))
            fulcrumValues = list(self.cur.fetchall()[0])
            del fulcrumValues[0] # remove the index
            return fulcrumValues

    def insert_fulcrum_values_row(self, values):
        insertSQL = ''' INSERT INTO fulcrum_values(calibration, throttleLow, throttleHigh) VALUES(?,?,?) '''
        self.cur.execute(insertSQL, values)
        self.conn.commit()

    def delete_fulcrum_values(self, id=None):
        if id == None:  #deletes all rows with id > 1
            deleteSQL = ''' DELETE FROM fulcrum_values WHERE id>1 '''
            self.cur.execute(deleteSQL)
        else: #delets row at id
            deleteSQL = ''' DELETE FROM fulcrum_values WHERE id=? '''
            self.cur.execute(deleteSQL, str(id))
        self.conn.commit()

    def cleanup_fulcrum_values_table(self):
        fulcrumValueRows = self.retrieve_fulcrum_values()
        if len(fulcrumValueRows) > 1:
            self.delete_fulcrum_values()
            print('deleted all rows with ID > 1')
            pass
        elif len(fulcrumValueRows) < 1:
            self.insert_fulcrum_values_row((0, 0, 0))
            print('added fulcrum_values row to table')
        else:
            pass

    def update_calibration(self, calibrationValue):
        updateSQL = '''UPDATE fulcrum_values 
                        SET calibration=?
                        WHERE id=1'''
        self.cur.execute(updateSQL, (str(calibrationValue),))
        self.conn.commit()

    def update_throttle_limits(self, throttleLow, throttleHigh):
        updateSQL = '''UPDATE fulcrum_values 
                        SET throttleLow=?, throttleHigh=?
                        WHERE id=1'''
        self.cur.execute(updateSQL, (str(throttleLow),str(throttleHigh),))
        self.conn.commit()