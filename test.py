import sqlite3


conn = sqlite3.connect("lib_book.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM books ORDER BY RANDOM() LIMIT 1")

data = cursor.fetchone()
book = data[0]

conn.close()

print(book)
