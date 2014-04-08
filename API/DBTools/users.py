__author__ = 'warprobot'

from API.DBTools import DBconnect
"""
Helper class to manipulate with users.
"""


def save_user(email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    try:
        user = select_user('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
        if len(user) == 0:
            DBconnect.exec_update(
                'INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
        user = select_user('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s',
                           (email, ))
    except Exception as e:
        raise Exception(e.message)

    return user_describe(user)


def update_user(email, about, name):
    DBconnect.exist(entity="Users", identificator="email", value=email)
    DBconnect.exec_update('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s',
                          (email, about, name, email, ))
    return details(email)


def followers(email, type):
    where = "followee"
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    f_list = DBconnect.exec_query(
        "SELECT " + type + " FROM Followers JOIN Users ON Users.email = Followers." + type +
        " WHERE " + where + " = %s ", (email, )
    )
    return tuple2list(f_list)


def details(email):
    user = user_query(email)
    if user is None:
        raise Exception("No user with email " + email)
    user["followers"] = followers(email, "follower")
    user["following"] = followers(email, "followee")
    user["subscriptions"] = user_subscriptions(email)
    return user


def user_subscriptions(email):

    s_list = []
    subscriptions = DBconnect.exec_query('select thread FROM Subscriptions WHERE user = %s', (email, ))
    for el in subscriptions:
        s_list.append(el[0])
    return s_list


#-----------------------------------------------------------------------------------------------------------------------


def user_query(email):
    user = select_user('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
    if len(user) == 0:
        return None
    return user_describe(user)


def user_describe(user):
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response


def select_user(query, params):
    return DBconnect.exec_query(query, params)


def tuple2list(list):
    new_list = []
    for el in list:
        new_list.append(el[0])
    return new_list