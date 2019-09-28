def retrieve_fulcrum_values(conn, row=None):
    cur = conn.cursor()
    if row == None:
        retrieve_sql = ''' SELECT * FROM fulcrum_values'''
        cur.execute(retrieve_sql)
    else:
        retrieve_sql = ''' SELECT * FROM fulcrum_values WHERE id=? '''
        cur.execute(retrieve_sql, row)
    
    return cur.fetchall()

def insert_fulcrum_values_row(conn, values):
    insert_sql = ''' INSERT INTO fulcrum_values(calibration, throttleLow, throttleHigh) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(insert_sql, values)
    conn.commit()
    pass

def delete_fulcrum_values_extra(conn):
    cur = conn.cursor()
    cur.execute()
    pass

def cleanup_fulcrum_values_table(conn):
    fulcrum_value_rows = retrieve_fulcrum_values(conn)
    if len(fulcrum_value_rows) > 1:
        pass
    elif len(fulcrum_value_rows) < 1:
        insert_fulcrum_values_row(conn, (0, 0, 0))
        print('added fulcrum_values row to table')
    else:
        pass