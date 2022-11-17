import sqlite3

def ConnectDb(new_table=False): 
 try:
    if new_table==True:
      conn = sqlite3.connect('horoscope_bufer.db')
    else:
      conn = sqlite3.connect('horoscope.db')
##    conn.row_factory = sqlite3.Row
    return(conn)
 except Exception as error:
    print(error)
    return(None)

connection = ConnectDb()
cursor = connection.cursor()

cursor.execute("select * from PostsBuffer")
posts = cursor.fetchall()


print(posts)