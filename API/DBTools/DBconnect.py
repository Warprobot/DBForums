__author__ = 'warprobot'

import MySQLdb as db


class DBConnection:
    """
    MySQL connector - helper class.
    Class fields wth your personal information.

    http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
    Default settings are below. Rough hard coding.
    """
    def __init__(self):
        pass

    # Main connector method
    def connect(self):
        return db.connect(self.host, self.user, self.password, self.dataBase, init_command='set names UTF8')
    host = "localhost"
    user = "root"
    password = ""
    dataBase = "DBForums"


# Execute update query
def exec_update(query, params):
    try:
        con = DBConnection()
        con = con.connect()
        con.autocommit(False)
        with con:
            cursor = con.cursor()
            con.begin()
            cursor.execute(query, params)
            con.commit()
            cursor.close()
            id = cursor.lastrowid
        con.close()
    except db.Error:
        raise db.Error("Database error in update query.")
    return id


# Execute query
def exec_query(query, params):
    try:
        con = DBConnection()
        con = con.connect()
        with con:
            cursor = con.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
        con.close()
    except db.Error:
        raise db.Error("Database error in usual query")
    return result


# Check if something exists
def exist(entity, identificator, value):
    if not len(exec_query('SELECT id FROM ' + entity + ' WHERE ' + identificator + ' = %s', (value, ))):
        raise Exception("No such element in " + entity + " with " + identificator + " = " + str(value))
    return