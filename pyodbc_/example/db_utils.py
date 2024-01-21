import pyodbc

def get_cursor_express():
        cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                        "Server=localhost\sqlexpress;"
                        "Database=Stonks;"
                        "Trusted_Connection=yes;")
        cursor = cnxn.cursor()    
        return cursor

def get_cursor():
        cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                        "Server=DESKTOP-BKHK1H3;"
                        "Database=Stonks;"
                        "Trusted_Connection=yes;")
        cursor = cnxn.cursor()    
        return cursor

def run_sql(sql, values=[]):
    cursor = get_cursor()
    if values:
        cursor.execute(sql, values)
    else:
        cursor.execute(sql)
    cursor.commit()
    cursor.close()

def run_sql_many(sql, values):
    cursor = get_cursor()
    cursor.executemany(sql, values)
    cursor.commit()
    cursor.close()