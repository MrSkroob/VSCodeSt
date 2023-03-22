import sqlite3


connection = sqlite3.connect('chinook.db')


name = input("Input album name\n> ")
query = """
SELECT Title FROM albums
WHERE albums.Title LIKE (?)
"""
print(query)
print('\nResults found:\n--------------')
cursor = connection.execute(query, (name,))
for row in cursor:
    print(row[0])


connection.close()
