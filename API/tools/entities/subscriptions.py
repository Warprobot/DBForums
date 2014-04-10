__author__ = 'warprobot'

from API.tools import DBconnect


"""
Helper class to manipulate with subscriptions.
"""


def save_subscription(email, thread_id):
    DBconnect.exist(entity="Threads", identifier="id", value=thread_id)
    DBconnect.exist(entity="Users", identifier="email", value=email)
    subscription = DBconnect.select_query(
        'select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscription) == 0:
        DBconnect.update_query('INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread_id, email, ))
        subscription = DBconnect.select_query(
            'select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
        )

    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def remove_subscription(email, thread_id):
    DBconnect.exist(entity="Threads", identifier="id", value=thread_id)
    DBconnect.exist(entity="Users", identifier="email", value=email)
    subscription = DBconnect.select_query(
        'select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscription) == 0:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    DBconnect.update_query('DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, ))

    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response