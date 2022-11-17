import horoscopedb as horoscopedb

conn=horoscopedb.ConnectDb()
cur=conn.cursor()
cur.execute("SELECT * FROM Sources")
records=cur.fetchall()
cur.execute("DROP TABLE Sources")
cur.execute("""CREATE TABLE IF NOT EXISTS Sources(
                                    ID    INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,                                   
                                    Name  TEXT,
                                    Token TEXT,
                                    Price int);
                             """)  
for i in records:
    cur.executemany("INSERT INTO Sources (Name,Token,Price)  VALUES (?,?,?)",(i[1],i[2],1))
