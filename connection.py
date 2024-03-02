import psycopg2
from psycopg2.extras import DictCursor

# константы
DATABASE_NAME = "pyMessager"
USER = "postgres"
PASSWORD = "pass"
HOST = "localhost"

class DatabaseQueries:

    def isLoginExist(login):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT login FROM users WHERE login = %s", (login, ))
                    if cursor.rowcount > 0:
                        return True
                    return False
        except Exception as e:
            print("Error connecting to database ", e)

    def setLoginAndPassword(login, password):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
                    connection.commit()
        except Exception as e:
            print("Error connecting to database ", e)

    def isLoginAndPasswordTrue(userLogin, userPassword):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT login, password FROM users WHERE login = %s AND password = %s", (userLogin, userPassword))
                    if cursor.rowcount > 0:
                        return True
                    return False
        except Exception as e:
            print("Error connecting to database ", e)
    
    def getId(login):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM users WHERE login = %s", (login, ))
                    return cursor.fetchone()[0]
        except Exception as e:
            print("Error connecting to database ", e)

    def getIdFromCorrespondences(id):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor(cursor_factory = DictCursor) as cursor:
                    cursor.execute("SELECT user_id, user_id_with FROM correspondences WHERE user_id = %s OR user_id_with = %s", (id, id))
                    rows = cursor.fetchall()

                    resultData = []
                    for row in rows:
                        if row['user_id'] == id:
                            resultData.append(row['user_id_with'])
                        elif row['user_id_with'] == id:
                            resultData.append(row['user_id'])
                    
                    return resultData
        except Exception as e:
            print("Error connecting to database ", e)

    def idsToLogins(idUsers):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor(cursor_factory = DictCursor) as cursor:
                    cursor.execute("SELECT login, id FROM users WHERE id IN %s", (tuple(idUsers), ))
                    rows = cursor.fetchall()
                    
                    resultData = dict()
                    for row in rows:
                        resultData[row['id']] = row['login']

                    return resultData
        except Exception as e:
            print("Error connecting to database", e)

    def isCorrespondenceExsist(userId, userIdWith):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT user_id, user_id_with FROM correspondences WHERE (user_id = %s OR user_id = %s) AND (user_id_with = %s OR user_id_with = %s)"
                    cursor.execute(sql, (userId, userIdWith, userId, userIdWith))
                    if cursor.rowcount != 0:
                        return True
                    return False
        except Exception as e:
            print("Error connecting to database ", e)

    def addCorrespondence_getId(userId, userIdWith):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO correspondences (user_id, user_id_with, user_is_read, user_with_is_read) VALUES (%s, %s, %s, %s) RETURNING id"
                    cursor.execute(sql, (userId, userIdWith, True, False))
                    
                    return cursor.fetchone()[0]
        except Exception as e:
            print("Error connecting to database ", e)

    def setMessage(userId, userIdWith, idCorrespondence, message):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO messages (id_sender, id_recipient, message, id_correspondences, is_read) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (userId, userIdWith, message, idCorrespondence, False))
                    connection.commit()
        except Exception as e:
            print("Error connecting to database ", e)

    def getMessages(idCorrespondence, userId):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM messages WHERE id_correspondences = %s", (idCorrespondence, ))
                    rows = cursor.fetchall()

                    resultData = []
                    for row in rows:
                        sender = row[1]
                        if sender == userId:
                            sender = "you"
                        resultData.append({"sender" : sender, 
                                          "message" : row[3],
                                          "send_time" : str(row[5])[:16],
                                          "status" : row[6]})

                    return resultData
        except Exception as e:
            print("Error connecting to database ", e)

    def getIdCorrespondence(userId, userIdWith):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT id FROM correspondences WHERE (user_id = %s OR user_id = %s) AND (user_id_with = %s OR user_id_with = %s)"
                    cursor.execute(sql, (userId, userIdWith, userId, userIdWith))
                    
                    return cursor.fetchone()[0]
        except Exception as e:
            print("Error connecting to database ", e)

    def messageReadByUser(idCorrespondence, userId):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE messages SET is_read = %s WHERE id_correspondences = %s AND id_sender != %s", (True, idCorrespondence, userId))
                    connection.commit()
        except Exception as e:
            print("Error conecting to database ", e)

    def getStatus(userId, userIdWith):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT user_id, user_is_read FROM correspondences WHERE user_id = %s AND user_id_with = %s", (userId, userIdWith))
                    if cursor.rowcount > 0:
                        return cursor.fetchone()[1]
                    
                    cursor.execute("SELECT user_id_with, user_with_is_read FROM correspondences WHERE user_id_with = %s AND user_id = %s", (userId, userIdWith))
                    return cursor.fetchone()[1]
        except Exception as e:
            print("Error connecting to database ", e)

    def correspondenceIsRead(idCorrespondence, userId):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM correspondences WHERE user_id = %s AND id = %s", (userId, idCorrespondence))
                    
                    is_read = "user_is_read"
                    if cursor.rowcount == 0:
                        is_read = "user_with_is_read"
                    
                    sql = f"UPDATE correspondences SET {is_read} = %s WHERE id = %s"
                    cursor.execute(sql, (True, idCorrespondence))
                    connection.commit()
        except Exception as e:
            print("Error connecting to database ", e)

    def correspondencesIsNotRead(idCorrespondence, userIdWith):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT user_id_with FROM correspondences WHERE user_id_with = %s AND id = %s", (userIdWith, idCorrespondence))

                    is_read = "user_is_read"
                    if cursor.rowcount > 0:
                        is_read = "user_with_is_read"

                    sql = f"UPDATE correspondences SET {is_read} = %s WHERE id = %s"
                    cursor.execute(sql, (False, idCorrespondence))
                    connection.commit()
        except Exception as e:
            print("Error connecting to database ", e)

    def deleteAccount(userId):
        try:
            with psycopg2.connect(dbname = DATABASE_NAME, user = USER, password = PASSWORD, host = HOST) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM messages WHERE id_sender = %s OR id_recipient = %s", (userId, userId))
                    connection.commit()

                    cursor.execute("DELETE FROM correspondences WHERE user_id = %s OR user_id_with = %s", (userId, userId))
                    connection.commit()

                    cursor.execute("DELETE FROM users WHERE id = %s", (userId, ))
                    connection.commit()
        except Exception as e:
            print("Error connection to database ", e)