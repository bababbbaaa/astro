import sqlite3
import pathlib
import datetime 
#  подключиться к базе данных

def ConnectDb(): 
 try:
    
    conn = sqlite3.connect('horoscope.db') 
    return(conn)
 except Exception as error:
    return(None)


#  создать структуру таблиц, некоторые заполнить
def CreateTables():
 
 conn = ConnectDb()
 if conn is None:      
    exit()
 try:
    
     cur = conn.cursor()
     cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                                    Name          TEXT,
                                    IS_Main       INTEGER,        /*это главный пользователь, все родственники*/
                                    Gender_ID     INTEGER,
                                    BirthTime     DATETIME,
                                    Birthday      DATE,
                                    Birthplace    TEXT,
                                    CurrLocation  TEXT,
                                    DesTime_ID    INTEGER,        /*желаемое время получения сообщения*/    
                                    TimeZone      INTEGER,
                                    TelegramID    TEXT NOT NULL,
                                    RegDate       DATE,
                                    RegDateFin    DATE,           /*дата, когда было окончено первоначальное заполнение анкеты*/  
                                    IsActiveBot   INTEGER,        /*бот активен*/
                                    Balance       DECIMAL(15,2),
                                    IsActiveSub   INTEGER,        /*подписка активна, при активной подписке может быть отключен бот*/
                                    SubscrType_ID INTEGER,
                                    ActiveUntil   DATE,      /*дата окончания подписки*/
                                    DateSend      DATE,     /* дата последней отправки сообщения*/
                                    IntrvMessBeg  INTEGER, /* интервал (начало) MessBodies из которого были снегенированы сообщения */
                                    IntrvMessEnd  INTEGER, /* интервал (окончание) */ 
                                    StdShutoff    INTEGER  DEFAULT (0),   /* стандартное отключение  - 1, 0 - бесконечная подписка, по умолчанию  0  */
                                    
                                    
                                    FOREIGN KEY (DesTime_ID) REFERENCES DesTimes(ID),
                                    FOREIGN KEY (Gender_ID) REFERENCES Genders(ID),
                                    FOREIGN KEY (SubscrType_ID) REFERENCES SubscrTypes(ID)                
                                    );               
                              """)


     

     # заполнить служебные таблицы


     cur.execute("""SELECT * from Genders""")
     records = cur.fetchall()
     if len(records) == 0:
            cur.execute("""INSERT INTO Genders (ID, Name) VALUES (1, 'M');""")              
            cur.execute("""INSERT INTO Genders (ID, Name) VALUES (2, 'F');""")
 except sqlite3.Error as error:
     HandleMess("Ошибка при начальном заполнении БД : "+ "\n"+ str(error),2)
 finally:
     if cur:
        cur.close()
     if conn:
        conn.close()
        
     return(None)
       

# CreateTables()
