import MySQLdb

def setup_conn(cursor):
    cursor.execute('SET NAMES utf8')
    cursor.execute('SET CHARACTER SET utf8')
    cursor.execute('SET character_set_connection=utf8')


def query_db(cursor, query, args=(), one=False):
    cursor.execute(query, args)
    rv = [dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row)) for row in cursor.fetchall()]
    return (rv[0] if rv else None) if one else rv

def connect(host, user, db):
    conn = MySQLdb.connect(host=host, user=user, db=db)
    setup_conn(conn.cursor())

    return conn

