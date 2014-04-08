__author__ = 'warprobot'

from API.DBTools import DBconnect
from API.DBTools.DBconnect import DBConnection
from API.DBTools import users, forums, threads


"""
Helper class to manipulate with posts.
"""


def create(date, thread, message, user, forum, optional):
    DBconnect.exist(entity="Threads", identificator="id", value=thread)
    DBconnect.exist(entity="Forums", identificator="short_name", value=forum)
    DBconnect.exist(entity="Users", identificator="email", value=user)
    if len(DBconnect.exec_query("SELECT Threads.id FROM Threads JOIN Forums ON Threads.forum = Forums.short_name "
                                "WHERE Threads.forum = %s AND Threads.id = %s", (forum, thread, ))) == 0:
        raise Exception("no thread with id = " + thread + " in forum " + forum)
    if "parent" in optional:
        if len(DBconnect.exec_query("SELECT Posts.id FROM Posts JOIN Threads ON Threads.id = Posts.thread "
                             "WHERE Posts.id = %s AND Threads.id = %s", (optional["parent"], thread, ))) == 0:
            raise Exception("No post with id = " + optional["parent"])
    query = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    parameters = [message, user, forum, thread, date]

    #optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
    for param in optional:
        query += ", "+param
        values += ", %s"
        parameters.append(optional[param])

    query += ") VALUES " + values + ")"

    update_thread_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"

    con = DBConnection()
    con = con.connect()
    con.autocommit(False)
    with con:
        cursor = con.cursor()
        try:
            con.begin()
            cursor.execute(update_thread_posts, (thread, ))
            cursor.execute(query, parameters)
            con.commit()
        except Exception as e:
            con.rollback()
            raise Exception("Database error: " + e.message)
        #DatabaseConnection.connection.commit()
        post_id = cursor.lastrowid
        cursor.close()

    con.close()
    post = post_query(post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post


def details(id, related):
    post = post_query(id)
    if post is None:
        raise Exception("no post with id = "+id)

    if "user" in related:
        post["user"] = users.details(post["user"])
    if "forum" in related:
        post["forum"] = forums.details(short_name=post["forum"], related=[])
    if "thread" in related:
        post["thread"] = threads.details(id=post["thread"], related=[])

    return post


def posts_list(entity, identificator, related, params):
    if entity == "forum":
        DBconnect.exist(entity="Forums", identificator="short_name", value=identificator)

    #-------------------------------------------------------------------------------------------------------------------
    if entity == "thread":
        DBconnect.exist(entity="Threads", identificator="id", value=identificator)
    #-------------------------------------------------------------------------------------------------------------------

    if entity == "user":
        DBconnect.exist(entity="Users", identificator="email", value=identificator)
    query = "SELECT id FROM Posts WHERE " + entity + " = %s "
    parameters = [identificator]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])
    post_ids = DBconnect.exec_query(query=query, params=parameters)
    post_list = []
    for id in post_ids:
        id = id[0]
        post_list.append(details(id=id, related=related))
    return post_list


def remove_restore(post_id, status):
    DBconnect.exist(entity="Posts", identificator="id", value=post_id)
    DBconnect.exec_update("UPDATE Posts SET isDeleted = %s WHERE Posts.id = %s", (status, post_id, ))
    return {
        "post": post_id
    }


def update(id, message):
    DBconnect.exist(entity="Posts", identificator="id", value=id)
    DBconnect.exec_update('UPDATE Posts SET message = %s WHERE id = %s', (message, id, ))
    return details(id=id, related=[])


def vote(id, vote):
    DBconnect.exist(entity="Posts", identificator="id", value=id)
    if vote == -1:
        DBconnect.exec_update("UPDATE Posts SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        DBconnect.exec_update("UPDATE Posts SET likes=likes+1, points=points+1  where id = %s", (id, ))
    return details(id=id, related=[])

#-----------------------------------------------------------------------------------------------------------------------

def select_post(query, params):
    return DBconnect.exec_query(query, params)


def post_query(id):
    post = select_post('select date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, likes, message, parent, points, thread, user '
                       'FROM Posts WHERE id = %s', (id, ))
    if len(post) == 0:
        return None
    return post_describe(post)


def post_describe(post):
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],

    }
    return post_response
