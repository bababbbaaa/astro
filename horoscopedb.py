import sqlite3
import pathlib
import datetime 
from horoscoperr import HandleMess
#  подключиться к базе данных

def ConnectDb(subscribe=False): 
 try:
    if subscribe==True:
      conn = sqlite3.connect('payments.db')
    else:
      conn = sqlite3.connect('horoscope.db')
##    conn.row_factory = sqlite3.Row
    return(conn)
 except Exception as error:
    HandleMess("Ошибка подключения к базе: "+DbWay+"\n"+str(error),4)	
    return(None)


#  создать структуру таблиц, некоторые заполнить
def CreateTables(new_table=False):
 
 conn = ConnectDb(new_table)
 if conn is None:      
    exit()
 try:
    
     cur = conn.cursor()


##     cur.execute("""CREATE TABLE IF NOT EXISTS Const(
##                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
##                                    Name TEXT,
##                                    ConstVal TEXT
##                                    );
##                              """)
     
##     cur.execute("""CREATE UNIQUE INDEX IF NOT EXISTS "Const_Name_UIND" ON "Const" ("Name"); """)
     
     cur.execute("""CREATE TABLE IF NOT EXISTS Genders(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Name TEXT               
                                    );
                              """)
     

     cur.execute("""CREATE TABLE IF NOT EXISTS Directions(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Name TEXT              
                                    );
                              """)
          
     
     cur.execute("""CREATE TABLE IF NOT EXISTS DesTimes(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,    -- нумерация с нуля 
                                    DesTimeBegin TEXT,
                                    Name   TEXT
                                    );
                              """)
     
     # таблица сегодняшних сообщений
     cur.execute("""CREATE TABLE IF NOT EXISTS MessHeaders(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT, -- нумерация с нуля
                                    MessDate   DATE, /*Дата к которой относится  заголовок, каждый заголовок строго на свою дату*/
                                    Header     TEXT
                                    );
                              """)

     # таблица завтрашних сообщений - сегодня заменено на завтра
     cur.execute("""CREATE TABLE IF NOT EXISTS MessHeaders_1(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT, -- нумерация с нуля
                                    MessDate   DATE, /*Дата к которой относится  заголовок, каждый заголовок строго на свою дату*/
                                    Header     TEXT
                                    );
                              """) 
     # таблица сегодняшних сообщений
     cur.execute("""CREATE TABLE IF NOT EXISTS MessBodies(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- нумерация с нуля 
                                    Col_1  TEXT,   /*отношения*/
                                    Col_2  TEXT,   /*возможности*/
                                    Col_3  TEXT,   /*здоровье*/
                                    Col_4  TEXT    /*деньги*/
                                    );
                              """)
     # таблица завтрашних сообщений - сегодня заменено на завтра
     cur.execute("""CREATE TABLE IF NOT EXISTS MessBodies_1(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- нумерация с нуля 
                                    Col_1  TEXT,   /*отношения*/
                                    Col_2  TEXT,   /*возможности*/
                                    Col_3  TEXT,   /*здоровье*/
                                    Col_4  TEXT    /*деньги*/
                                    );
                              """)
      

 

     cur.execute("""CREATE TABLE IF NOT EXISTS AstroSchool(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- нумерация с нуля 
                                    Category   TEXT,    --  рубрика
                                    DateSend   DATE,
                                    TimeSend   DATETIME,
                                    ManagerID  INTEGER,
                                    MessageID    INTEGER
                                    );
                              """)


      #  Таблица одноразовых временных пользователей
     cur.execute("""CREATE TABLE IF NOT EXISTS UsersTmp(                            
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                                    TelegramID    TEXT NOT NULL,
                                    Name          TEXT,                                    
                                    Gender_ID     INTEGER,                                    
                                    Birthday      DATE,
                                    Birthplace    TEXT,
                                    Col_1   INTEGER,
                                    Col_2   INTEGER,
                                    Col_3   INTEGER,
                                    Col_4   INTEGER,
                                    FOREIGN KEY (Gender_ID) REFERENCES Genders(ID));
                             """) 

     cur.execute("""CREATE TABLE IF NOT EXISTS Sources(
                                    ID    INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,                                   
                                    Name  TEXT,
                                    Token TEXT);
                             """)                                  
                                     
     
     cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                                    Name          TEXT,
                                    IS_Main       INTEGER,        /*это главный пользователь, все родственники*/
                                    Gender_ID     INTEGER,
                                    BirthTime     DATETIME,
                                    Birthday      DATE,
                                    Birthplace    TEXT,                                    
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
                                    StdShutoff    INTEGER  DEFAULT (1),   /* стандартное отключение  - 1, 0 - бесконечная подписка, по умолчанию  1  */                                    
                                    TryPayRem     INTEGER DEFAULT(2),  /*Осталось попыток списания средств*/   
                                    Source_ID     INTEGER,  /*откуда пришел клиент*/      
                                    RegDate_seconds INTEGER,
                                    DateSend_seconds INTEGER, 
                                    ActiveUntil_seconds INTEGER,
                                    RegDateFin_seconds INTEGER,                         
                                    FOREIGN KEY (DesTime_ID) REFERENCES DesTimes(ID),
                                    FOREIGN KEY (Gender_ID) REFERENCES Genders(ID),
                                    FOREIGN KEY (SubscrType_ID) REFERENCES SubscrTypes(ID),
                                    FOREIGN KEY (Source_ID) REFERENCES Sources(ID)
                                    );               
                              """)


     cur.execute(""" CREATE TRIGGER IF NOT EXISTS  ADEL_Users  AFTER DELETE ON Users
                    WHEN OLD.IS_Main = 1
                    BEGIN
                        DELETE FROM Users WHERE TelegramID = OLD.TelegramID;
                    END;
                """) 

     cur.execute("""CREATE TRIGGER IF NOT EXISTS AUPD_Users  AFTER UPDATE OF IsActiveSub, IsActiveBot  ON Users
                     WHEN OLD.IS_MAIN = 1
                     BEGIN
                        UPDATE Users
                        SET IsActiveSub = NEW.IsActiveSub,
                            IsActiveBot = NEW.IsActiveBot
                        WHERE TelegramID = OLD.TelegramID AND 
                              ID <> OLD.ID;
                     END;
    
                """)


     cur.execute("""CREATE TRIGGER IF NOT EXISTS AUPD_Users_DesTime  AFTER UPDATE OF DesTime_ID ON Users
                    WHEN OlD.DesTime_ID IS NULL AND 
                          NEW.DesTime_ID IS NOT NULL
                    BEGIN
                       UPDATE Users
                       SET RegDateFin = datetime('now', 'localtime') 
                        WHERE ID = OLD.ID;
                    END;
                """)



     cur.execute("""CREATE TRIGGER  IF NOT EXISTS AUPD_Users_Birth AFTER UPDATE OF BirthTime,
                                                                                   Birthday,
                                                                                   Birthplace
                   ON Users
                   BEGIN
                     UPDATE Users   SET DateSend = 0 WHERE ID = OLD.ID;
                   END;
       
                 """)
       
     cur.execute("""CREATE TRIGGER IF NOT EXISTS AINS_Users AFTER INSERT  ON Users
                    BEGIN
                      UPDATE Users
                      SET RegDate = datetime('now', 'localtime') 
                      WHERE ID = NEW.ID;
                    END;
                 """)
     
     cur.execute("""CREATE TABLE IF NOT EXISTS UserMess(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                                    User_ID INTEGER,
                                    Col_1   INTEGER,
                                    Col_2   INTEGER,
                                    Col_3   INTEGER,
                                    Col_4   INTEGER,
                                    
                                    FOREIGN KEY (User_ID) REFERENCES Users(ID),
                                    FOREIGN KEY (Col_1) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_2) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_3) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_4) REFERENCES MessBodies(ID)
                                   
                                    );               
                              """)

     cur.execute("""CREATE TABLE IF NOT EXISTS UserSentMess(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                                    User_ID INTEGER,
                                    DateSend DATE,      /*дата отправки данного сообщения*/
                                    Col_1   INTEGER,
                                    Col_2   INTEGER,
                                    Col_3   INTEGER,
                                    Col_4   INTEGER,
                                    
                                    FOREIGN KEY (User_ID) REFERENCES Users(ID),
                                    FOREIGN KEY (Col_1) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_2) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_3) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_4) REFERENCES MessBodies(ID)
                                   
                                    );               
                              """)


     cur.execute("""CREATE INDEX IF NOT EXISTS "Users_TelegramID_IND" ON "Users" ("TelegramID");
                              """)

     cur.execute("""CREATE UNIQUE INDEX IF NOT EXISTS "Users_TelegramID_Name_UIND" ON "Users" ("Name", "TelegramID");
                 """)
     
     cur.execute("""CREATE TABLE IF NOT EXISTS Cashflow(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                                    User_ID     INTEGER  NOT NULL,
                                    Direction_ID  INTEGER  NOT NULL,
                                    DateMov     TEXT  NOT NULL,
                                    Sum         DECIMAL(15,2)  NOT NULL,
                                    FOREIGN KEY (User_ID) REFERENCES Users(ID),
                                    FOREIGN KEY (Direction_ID) REFERENCES Directions(ID)
                                    );
                              """)
     
     cur.execute(""" CREATE TRIGGER IF NOT EXISTS "ADEL_CashFlow" AFTER DELETE ON "Cashflow"
                     BEGIN   
                       UPDATE Users 
                       SET Вalance = (SELECT SUM(CashFlow.Sum*CashFlow.Direction_ID) as
                                    Balance FROM Cashflow WHERE CashFlow.User_ID = OLD.User_ID )                
                       WHERE ID = OLD.User_ID ;  
                     END;
                 """)
 
     cur.execute("""CREATE TRIGGER IF NOT EXISTS "AINS_CashFlow" AFTER INSERT ON "Cashflow"
                    BEGIN
                      UPDATE Users
                      SET Вalance = (SELECT SUM(CashFlow.Sum*CashFlow.Direction_ID) as
                                     Balance FROM Cashflow WHERE CashFlow.User_ID = NEW.User_ID )
                      WHERE ID = NEW.User_ID; 
                    END;
                 """)
     
     cur.execute("""CREATE TRIGGER IF NOT EXISTS "AUPD_CashFlow" AFTER UPDATE OF "User_ID", "Direction_ID", "Sum" ON "Cashflow"
                    BEGIN
                      UPDATE Users 
                      SET Вalance = (SELECT SUM(CashFlow.Sum*CashFlow.Direction_ID) as
                                     Balance FROM Cashflow WHERE CashFlow.User_ID = NEW.User_ID )
                      WHERE ID = NEW.User_ID ;

                      UPDATE Users
                      SET Вalance = (SELECT SUM(CashFlow.Sum*CashFlow.Direction_ID) as
                                     Balance FROM Cashflow WHERE CashFlow.User_ID = OLD.User_ID )
                      WHERE ID = OLD.User_ID ;
                    END;
                 """)                   

     
     
     cur.execute("""CREATE TABLE IF NOT EXISTS SubscrTypes(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,                                  
                                    Days INTEGER,
                                    Cost DECIMAL(15,2)
                                    );
                              """)


     # заполнить служебные таблицы


     cur.execute("""SELECT * from Genders""")
     records = cur.fetchall()
     if len(records) == 0:
            cur.execute("""INSERT INTO Genders (ID, Name) VALUES (1, 'M');""")              
            cur.execute("""INSERT INTO Genders (ID, Name) VALUES (2, 'F');""")
            
     cur.execute("""SELECT * from Directions""")
     records = cur.fetchall()
     if len(records) == 0:
            cur.execute("""INSERT INTO Directions (ID, Name) VALUES (1, 'IN');""") 
            cur.execute("""INSERT INTO Directions (ID, Name) VALUES (-1, 'OUT');""") 

     cur.execute("""SELECT * from SubscrTypes""")
     records = cur.fetchall()
     if len(records) == 0:
            cur.execute("""INSERT INTO SubscrTypes (ID,Days,Cost) VALUES (1,30,0);""")
            cur.execute("""INSERT INTO SubscrTypes (ID,Days,Cost) VALUES (2,30,100);""")
            cur.execute("""INSERT INTO SubscrTypes (ID,Days,Cost) VALUES (3,180,300);""")
            cur.execute("""INSERT INTO SubscrTypes (ID,Days,Cost) VALUES (4,365,500);""")
            
     cur.execute("""SELECT * from DesTimes""")
     records = cur.fetchall()
     if len(records) == 0:
        recordTimes = list()
        DesTimeBegin = datetime.datetime(1980,1, 1, 8, 30, 0 ).strftime("%H:%M:%S")
        recordTimes.append((0,DesTimeBegin,"Утро",))
        DesTimeBegin = datetime.datetime(1980,1, 1, 18, 30, 0 ).strftime("%H:%M:%S")
        recordTimes.append((1,DesTimeBegin,"Вечер",))
        

##        for i in range(0,24,1):
##           DesTimeBegin = datetime.datetime(1980,1, 1, i, 0, 0 ).strftime("%H:%M:%S")
##           DesTimeEnd = datetime.datetime(1980,1, 1, i, 23, 59 ).strftime("%H:%M:%S")
##           recordTimes.append((i,DesTimeBegin,DesTimeEnd,))
           
        cur.executemany("""INSERT INTO DesTimes (ID,DesTimeBegin,Name) VALUES (?,?,?);""", recordTimes)

     # заполнить пользовательские таблицы тестовой информацией


     cur.execute("""SELECT * FROM MessHeaders""")
     records = cur.fetchall()
     if len(records) == 0:              
        recordsHeader = list()
        for i in range(0,100,1):
           recordsHeader.append((i,str(i)+"_Заголовок",))
        cur.executemany("""INSERT INTO MessHeaders (ID,Header) VALUES (?,?);""", recordsHeader)   

     cur.execute("""SELECT * FROM MessBodies""")
     records = cur.fetchall()
     if len(records) == 0:              
        recordsHeader = list()
        for i in range(0,100,1):
           recordsHeader.append((i,str(i)+"_Сообщение_1",str(i)+"_Сообщение_2",str(i)+"_Сообщение_3",str(i)+"_Сообщение_4",))
        cur.executemany("""INSERT INTO MessBodies (ID,Col_1,Col_2,Col_3,Col_4) VALUES (?,?,?,?,?);""", recordsHeader)



##     cur.execute("""SELECT * FROM AstroSchool""")
##     records = cur.fetchall()
##     if len(records) == 0:              
##        recordsHeader = list()
##        for i in range(0,100,1):
##           recordsHeader.append((i,str(i)+"_Занятие астрошколы",))
##        cur.executemany("""INSERT INTO AstroSchool (ID,Lesson) VALUES (?,?);""", recordsHeader)   
     
     conn.commit()
     HandleMess("База создана/обновлена")
     
 except sqlite3.Error as error:
     HandleMess("Ошибка при начальном заполнении БД : "+ "\n"+ str(error),2)
 finally:
     if cur:
        cur.close()
     if conn:
        conn.close()
        
     return(None)
       

CreateTables()

