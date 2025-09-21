import sqlite3

conn = sqlite3.connect('ctf.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (key TEXT PRIMARY KEY, value TEXT)')
cursor.execute('INSERT OR REPLACE INTO users (key, value) VALUES (?, ?)', ('user:admin', 'Hi Admin lol'))
cursor.execute('INSERT OR REPLACE INTO users (key, value) VALUES (?, ?)', ('secret_flag', 'NHNC{lETs_cOoK_THe_GoOSE_:speaking_head::speaking_head::speaking_head:}'))
conn.commit()
conn.close()
