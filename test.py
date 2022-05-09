import sqlite3

conn = sqlite3.connect('user.db', isolation_level=None)
cur = conn.cursor()

user_id = 277367977915973635
cur.execute('SELECT * FROM student_info WHERE id=%d' %user_id)
print(cur.fetchone())
