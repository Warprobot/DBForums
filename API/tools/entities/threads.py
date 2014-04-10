from API.tools.entities import users, forums

__author__ = 'warprobot'

from API.tools import DBconnect

"""
Helper class to manipulate with threads.
"""


def save_thread(forum, title, isClosed, user, date, message, slug, optional):
    DBconnect.exist(entity="Users", identifier="email", value=user)
    DBconnect.exist(entity="Forums", identifier="short_name", value=forum)

    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    thread = DBconnect.select_query(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE slug = %s', (slug, )
    )
    if len(thread) == 0:
        DBconnect.update_query('INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) '
                               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (forum, title, isClosed, user, date, message, slug, isDeleted, ))
        thread = DBconnect.select_query(
            'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
            'FROM Threads WHERE slug = %s', (slug, )
        )
    thread = thread[0]
    response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }

    # Delete few extra elements
    del response["dislikes"]
    del response["likes"]
    del response["points"]
    del response["posts"]

    return response


def details(id, related):
    thread = DBconnect.select_query(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (id, )
    )
    if len(thread) == 0:
        raise Exception('No thread exists with id=' + str(id))
    thread = thread[0]
    thread = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }

    if "user" in related:
        thread["user"] = users.details(thread["user"])
    if "forum" in related:
        thread["forum"] = forums.details(short_name=thread["forum"], related=[])

    return thread


def vote(id, vote):
    DBconnect.exist(entity="Threads", identifier="id", value=id)

    if vote == -1:
        DBconnect.update_query("UPDATE Threads SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        DBconnect.update_query("UPDATE Threads SET likes=likes+1, points=points+1  where id = %s", (id, ))

    return details(id=id, related=[])


def open_close_thread(id, isClosed):
    DBconnect.exist(entity="Threads", identifier="id", value=id)
    DBconnect.update_query("UPDATE Threads SET isClosed = %s WHERE id = %s", (isClosed, id, ))

    response = {
        "thread": id
    }

    return response


def update_thread(id, slug, message):
    DBconnect.exist(entity="Threads", identifier="id", value=id)
    DBconnect.update_query('UPDATE Threads SET slug = %s, message = %s WHERE id = %s', (slug, message, id, ))

    return details(id=id, related=[])


def threads_list(entity, identifier, related, params):
    if entity == "forum":
        DBconnect.exist(entity="Forums", identifier="short_name", value=identifier)
    if entity == "user":
        DBconnect.exist(entity="Users", identifier="email", value=identifier)
    query = "SELECT id FROM Threads WHERE " + entity + " = %s "
    parameters = [identifier]

    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    thread_ids_tuple = DBconnect.select_query(query=query, params=parameters)
    thread_list = []

    for id in thread_ids_tuple:
        id = id[0]
        thread_list.append(details(id=id, related=related))

    return thread_list


def remove_restore(thread_id, status):
    DBconnect.exist(entity="Threads", identifier="id", value=thread_id)
    DBconnect.update_query("UPDATE Threads SET isDeleted = %s WHERE id = %s", (status, thread_id, ))

    response = {
        "thread": thread_id
    }
    return response