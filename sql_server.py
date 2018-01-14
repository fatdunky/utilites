'''
Created on 15 Dec. 2017

@author: mcrick
'''

import pyodbc, logging
from _sqlite3 import Cursor

connection = {}

def connect_to_db(db_name, connect_string):
    global connection
    pyodbc.pooling = False
    connection[db_name] = pyodbc.connect(connect_string)

def disconnect_db(db_name):
    global connection
    logging.debug("disconnect_db, %s", db_name)
    if (connection.has_key(db_name)):
        logging.debug("disconnecting, %s", db_name)
        connection[db_name].close()

def run_sql(db_name, sql):
    global connection
    logging.debug("connect=%s, sql=%s", db_name, sql)
    cnxn = None
    if (connection.has_key(db_name)):
        cnxn = connection[db_name]
    else:
        return None
    return_val = []
    try:
        # Using a DSN, but providing a password as well
       
        logging.debug("connected")
        # Create a cursor from the connection
        cursor = cnxn.cursor()
        logging.debug("cursor")
        #cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        #cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        #cnxn.setencoding(encoding='utf-8')
        
        cursor.execute(sql)
        logging.debug("execute")
        for row in cursor:
            return_val.append(row)
        
    finally:
        cursor.close()
        del cursor

    return return_val


    
  