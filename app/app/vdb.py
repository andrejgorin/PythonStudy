import MySQLdb
def frdb(query):
    db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="unl",
                     charset='utf8',
                     use_unicode=True,
                     db="dslamz")
    cur = db.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return results
