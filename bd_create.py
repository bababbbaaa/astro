import encodings
from tokenize import Token
import requests
import json
import config
import sqlite3
import pathlib
import datetime
from functions import ConnectDb 
from horoscoperr import HandleMess
def CreateTables():   
 conn = ConnectDb()
 if conn is None:      
    exit()
 try:
    
     cur = conn.cursor()


     cur.execute("""CREATE TABLE IF NOT EXISTS Const(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Name TEXT,
                                    ConstVal TEXT
                                    );
                              """)
     cur.execute("""CREATE UNIQUE INDEX IF NOT EXISTS "Const_Name_UIND" ON "Const" ("Name"); """)
     
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
                                    DesTimeEnd   TEXT
                                    );
                              """)
     
     
     cur.execute("""CREATE TABLE IF NOT EXISTS MessHeaders(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT, -- нумерация с нуля 
                                    MessDate TEXT,
                                    Header      TEXT
                                    );
                              """)

     
     cur.execute("""CREATE TABLE IF NOT EXISTS MessBodies(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- нумерация с нуля 
                                    Col_1  TEXT,
                                    Col_2  TEXT,
                                    Col_3  TEXT,
                                    Col_4  TEXT
                                    );
                              """)
 
 
     cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                                    Name          TEXT,
                                    IS_Main       INTEGER,
                                    Gender_ID     INTEGER,
                                    BirthTime     TEXT,
                                    Birthday      TEXT,
                                    Birthplace    TEXT,
                                    CurrLocation  TEXT,
                                    DesTime_ID    INTEGER,
                                    TimeZone      INTEGER,
                                    TelegramID    TEXT,
                                    RegDate       TEXT,
                                    IsActiveBot   INTEGER,
                                    Вalance       DECIMAL(15,2),
                                    IsActiveSub   INTEGER, 
                                    SubscrType_ID INTEGER,
                                    ActiveUntil   TEXT,
                                    FOREIGN KEY (DesTime_ID) REFERENCES DesTimes(ID),
                                    FOREIGN KEY (Gender_ID) REFERENCES Genders(ID),
                                    FOREIGN KEY (SubscrType_ID) REFERENCES SubscrTypes(ID)                
                                    );               
                              """)

     cur.execute("""CREATE INDEX IF NOT EXISTS "Users_TelegramID_IND" ON "Users" ("TelegramID");
                              """)

##     cur.execute("""CREATE UNIQUE INDEX IF NOT EXISTS "Users_IS_MAIN_UIND" ON "Users" ("IS_Main", "TelegramID");     
##                 """)
##   у родственников одинаковый TelegramID и  IS_Main = 0, индекс не работает
     
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
        for i in range(0,24,1):
           DesTimeBegin = datetime.datetime(1980,1, 1, i, 0, 0 ).strftime("%H:%M:%S")
           DesTimeEnd = datetime.datetime(1980,1, 1, i, 23, 59 ).strftime("%H:%M:%S")
           recordTimes.append((i,DesTimeBegin,DesTimeEnd,))
           
        cur.executemany("""INSERT INTO DesTimes (ID,DesTimeBegin,DesTimeEnd) VALUES (?,?,?);""", recordTimes)

     # заполнить пользовательские таблицы тестовой информацией


     cur.execute("""SELECT * FROM MessHeaders""")
     records = cur.fetchall()
     if len(records) == 0:              
        recordsHeader = list()
        for i in range(0,100,1):
           recordsHeader.append((i,str(i)+"_Заголовок",))
        cur.executemany("""INSERT INTO MessHeaders (ID,MessDate,Header) VALUES (?,0,?);""", recordsHeader)   

     cur.execute("""SELECT * FROM MessBodies""")
     records = cur.fetchall()
     if len(records) == 0:              
        recordsHeader = list()
        for i in range(0,100,1):
           recordsHeader.append((i,str(i)+"_Сообщение_1",str(i)+"_Сообщение_2",str(i)+"_Сообщение_3",str(i)+"_Сообщение_4",))
        cur.executemany("""INSERT INTO MessBodies (ID,Col_1,Col_2,Col_3,Col_4) VALUES (?,?,?,?,?);""", recordsHeader)
     
     conn.commit()
     HandleMess("База создана")
     
 except sqlite3.Error as error:
     HandleMess("Ошибка при начальном заполнении БД : "+ "\n"+ str(error),2)
 finally:
     if cur:
        cur.close()
     if conn:
        conn.close()
        
     return(None)
       
CreateTables()