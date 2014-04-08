__author__ = 'warprobot'

import DBconnect
from API.DBTools import users

"""
Helper class to manipulate with forums.
"""


def save_forum(name, short_name, user):
    DBconnect.exist(entity="Users", identificator="email", value=user)
    forum = DBconnect.exec_query(
        'select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        DBconnect.exec_update('INSERT INTO Forums (name, short_name, user) VALUES (%s, %s, %s)',
                              (name, short_name, user, ))
        forum = DBconnect.exec_query(
            'select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
        )
    return forum_description(forum)


def forum_description(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


def details(short_name, related):
    forum = DBconnect.exec_query(
        'select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        raise ("No forum with exists short_name=" + short_name)
    forum = forum_description(forum)

    if "user" in related:
        forum["user"] = users.details(forum["user"])
    return forum


def list_users(short_name, optional):
    DBconnect.exist(entity="Forums", identificator="short_name", value=short_name)

    query = "SELECT distinct email FROM Users JOIN Posts ON Posts.user = Users.email " \
            " JOIN Forums on Forums.short_name = Posts.forum WHERE Posts.forum = %s "
    if "since_id" in optional:
        query += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY Users.id " + optional["order"]
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])

    users_tuple = DBconnect.exec_query(query, (short_name, ))
    list_u = []
    for user in users_tuple:
        user = user[0]
        list_u.append(users.details(user))
    return list_u
