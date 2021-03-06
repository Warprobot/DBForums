from API.tools.entities import users

__author__ = 'warprobot'

from API.tools import DBconnect

"""
Helper class to manipulate with users.
"""


def add_follow(email1, email2):
    DBconnect.exist(entity="Users", identifier="email", value=email1)
    DBconnect.exist(entity="Users", identifier="email", value=email2)

    if email1 == email2:
        raise Exception("User with email=" + email1 + " can't follow himself")

    follows = DBconnect.select_query(
        'SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
    )

    if len(follows) == 0:
        DBconnect.update_query('INSERT INTO Followers (follower, followee) VALUES (%s, %s)', (email1, email2, ))

    user = users.details(email1)
    return user


def remove_follow(email1, email2):
    follows = DBconnect.select_query(
        'SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
    )

    if len(follows) != 0:
        DBconnect.update_query('DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))
    else:
        raise Exception("No such following")

    return users.details(email1)


def followers_list(email, type, params):
    DBconnect.exist(entity="Users", identifier="email", value=email)
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"

    query = "SELECT " + type + " FROM Followers JOIN Users ON Users.email = Followers." + type + \
            " WHERE " + where + " = %s "

    if "since_id" in params:
        query += " AND Users.id >= " + str(params["since_id"])
    if "order" in params:
        query += " ORDER BY Users.name " + params["order"]
    else:
        query += " ORDER BY Users.name DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    followers_ids_tuple = DBconnect.select_query(query=query, params=(email, ))

    f_list = []
    for id in followers_ids_tuple:
        id = id[0]
        f_list.append(users.details(email=id))

    return f_list