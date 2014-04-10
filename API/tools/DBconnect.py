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
    @staticmethod
    def connect():
        return db.connect(host="localhost", user="root", passwd="", db="DBForums", port=3306, init_command="SET NAMES utf8")


# Execute update query
def update_query(query, params):
    try:
        con = DBConnection()
        con = con.connect()
        cursor = con.cursor()
        cursor.execute(query, params)
        con.commit()
        inserted_id = cursor.lastrowid

        cursor.close()
        con.close()
    except db.Error:
        raise db.Error("Database error in update query.")
    return inserted_id


# Execute query
# Returns tuple!
def select_query(query, params):
    try:
        con = DBConnection()
        con = con.connect()
        cursor = con.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        con.close()
    except db.Error:
        raise db.Error("Database error in usual query")
    return result


# Check if something exists
def exist(entity, identifier, value):
    if not len(select_query('SELECT id FROM ' + entity + ' WHERE ' + identifier + '=%s', (value, ))):
        raise Exception("No such element in " + entity + " with " + identifier + "=" + str(value))
    return