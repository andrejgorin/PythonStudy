import sqlite3
def frdb(query):
    db = sqlite3.connect('vdb.db')
    cur = db.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return results