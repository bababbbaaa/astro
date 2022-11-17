from sqlalchemy.orm import sessionmaker
from .posts import *

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

LINK = 'sqlite:///' + abspath(join('..', 'horoscope.db'))

def create_session():
    engine = create_engine(LINK)
    return sessionmaker(engine)()

connection = ConnectDb()
cursor = connection.cursor()

cursor.execute("select * from Posts")
posts = cursor.fetchall()


print(posts)

_session = create_session()
for post in posts:
    id, category, time, date, telegram_id, post_id = post

    post = add_post(
        _session,
        category,
        telegram_id,
        post_id,
        date,
        'something',
        time
    )

    print(post.FirstRow, post.Time)