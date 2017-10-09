import MySQLdb
def frdb(query):
    db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="password",
                     db="example")
    cur = db.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return results
