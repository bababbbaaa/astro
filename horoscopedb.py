import sqlite3
import pathlib
import datetime 
from horoscoperr import HandleMess
from mysql.connector import connect, Error
#  подключиться к базе данных

def ConnectDb(): 
   try:
      conn =  connect(host = "195.2.79.3",
                   user = "admin2",
                    password="Sergey123()",
                    database = "horoscope")
      return(conn)
   except Exception as error:
      HandleMess("Ошибка подключения к базе: "+str(error),4)	
      return(None)


#  создать структуру таблиц, некоторые заполнить
def CreateTables():
 
 conn = ConnectDb()
 if conn is None:      
    return(False)
 try:
    
    cur = conn.cursor()

     
    cur.execute("""CREATE TABLE IF NOT EXISTS  Genders (
                                    ID  TINYINT  NOT NULL ,
                                    Name  VARCHAR(1) NOT NULL,
                                    PRIMARY KEY (ID)
                                    ) 
                              """)
     

    cur.execute("""CREATE TABLE IF NOT EXISTS Directions(
                                    ID TINYINT   NOT NULL ,
                                    Name VARCHAR(3) NOT NULL,
                                    PRIMARY KEY (ID)
                                    );
                              """)
          
     
    cur.execute("""CREATE TABLE IF NOT EXISTS DesTimes(
                                    ID TINYINT  NOT NULL,   /* нумерация с нуля */
                                    DesTimeBegin TIME,
                                    Name   VARCHAR(5),
                                    PRIMARY KEY (ID)
                                    );
                              """)
     
     # таблица сегодняшних сообщений
    cur.execute("""CREATE TABLE IF NOT EXISTS MessHeaders(
                                    ID INTEGER,         /*нумерация с нуля*/
                                    MessDate   DATE,    /*Дата к которой относится  заголовок, каждый заголовок строго на свою дату*/
                                    Header     TEXT,
                                    PRIMARY KEY (ID)
                                    );
                              """)

     # таблица завтрашних сообщений - сегодня заменено на завтра
    cur.execute("""CREATE TABLE IF NOT EXISTS MessHeaders_1(
                                    ID INTEGER,          /* нумерация с нуля*/
                                    MessDate   DATE,     /*Дата к которой относится  заголовок, каждый заголовок строго на свою дату*/
                                    Header     TEXT,
                                    PRIMARY KEY (ID)
                                    );
                              """) 
     # таблица сегодняшних сообщений
    cur.execute("""CREATE TABLE IF NOT EXISTS MessBodies(
                                    ID INTEGER,     /*  -- нумерация с нуля */
                                    Col_1  TEXT,   /*отношения*/
                                    Col_2  TEXT,   /*возможности*/
                                    Col_3  TEXT,   /*здоровье*/
                                    Col_4  TEXT,    /*деньги*/
                                    PRIMARY KEY (ID)
                                    );
                              """)
     # таблица завтрашних сообщений - сегодня заменено на завтра
    cur.execute("""CREATE TABLE IF NOT EXISTS MessBodies_1(
                                    ID INTEGER,     /*  -- нумерация с нуля */
                                    Col_1  TEXT,   /*отношения*/
                                    Col_2  TEXT,   /*возможности*/
                                    Col_3  TEXT,   /*здоровье*/
                                    Col_4  TEXT,    /*деньги*/
                                    PRIMARY KEY (ID)
                                    );
                              """)


      #  Таблица одноразовых временных пользователей
    cur.execute("""CREATE TABLE IF NOT EXISTS UsersTmp(                            
                                    ID INTEGER    NOT NULL AUTO_INCREMENT,
                                    TelegramID    BIGINT NOT NULL,
                                    Name          VARCHAR(255),                                    
                                    Gender_ID     TINYINT,                                    
                                    Birthday      VARCHAR(20),
                                    Birthplace    VARCHAR(255),
                                    Col_1   INTEGER,
                                    Col_2   INTEGER,
                                    Col_3   INTEGER,
                                    Col_4   INTEGER,
                                    PRIMARY KEY (ID),
                                    FOREIGN KEY (Gender_ID) REFERENCES Genders(ID)
                                    );
                             """) 

    cur.execute("""CREATE TABLE IF NOT EXISTS Sources(
                                    ID    INTEGER  NOT NULL AUTO_INCREMENT,                                   
                                    Name  VARCHAR(255),
                                    Token VARCHAR(255),
                                    PRIMARY KEY (ID)
                                    );
                             """)                                  

##    cur.execute("""CREATE TABLE IF NOT EXISTS SubscrTypes(
##                                    ID TINYINT NOT NULL AUTO_INCREMENT,
##                                    Days INTEGER,
##                                    Cost DECIMAL(15,2),
##                                    PRIMARY KEY (ID)
##                                    );
##                              """)

    cur.execute("""CREATE TABLE IF NOT EXISTS Subscriptions (
	                         ID  INTEGER  NOT NULL  AUTO_INCREMENT,
	                         TelegramID	BIGINT NOT NULL,
	                         Type	VARCHAR(15) NOT NULL,
	                         Start	VARCHAR(10) NOT NULL,
	                         End	VARCHAR(10) NOT NULL,
	                         PayID	VARCHAR(255) NOT NULL,
	                         PRIMARY KEY (ID)
	                         );
	                      """)



   
##    cur.execute("""DROP TABLE IF EXISTS UserMess """)
##    cur.execute("""DROP TABLE IF EXISTS UserSentMess""")
##    cur.execute("""DROP TABLE IF EXISTS Users """)
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                                    ID INTEGER  NOT NULL AUTO_INCREMENT ,
                                    Name          VARCHAR(255),
                                    IS_Main       TINYINT,        /*это главный пользователь, все родственники*/
                                    Gender_ID     TINYINT,
                                    BirthTime     VARCHAR(10),
                                    Birthday      VARCHAR(20),
                                    Birthplace    VARCHAR(255),                                    
                                    DesTime_ID    TINYINT,        /*желаемое время получения сообщения*/    
                                    TimeZone      TINYINT,
                                    TelegramID    BIGINT NOT NULL,
                                    RegDate       DATETIME,
                                    RegDateFin    DATETIME,           /*дата, когда было окончено первоначальное заполнение анкеты*/  
                                    IsActiveBot   TINYINT,        /*бот активен*/
                                    Balance       DECIMAL(15,2),
                                    IsActiveSub   TINYINT,        /*подписка активна, при активной подписке может быть отключен бот*/
                                    SubscrType_ID TINYINT,
                                    ActiveUntil   DATE,      /*дата окончания подписки*/
                                    DateSend      DATE,     /* дата последней отправки сообщения*/
                                    IntrvMessBeg  INTEGER, /* интервал (начало) MessBodies из которого были снегенированы сообщения */
                                    IntrvMessEnd  INTEGER, /* интервал (окончание) */ 
                                    StdShutoff    TINYINT  DEFAULT 1,   /* стандартное отключение  - 1, 0 - бесконечная подписка, по умолчанию  1  */                                    
                                    TryPayRem     TINYINT DEFAULT 2,  /*Осталось попыток списания средств*/   
                                    Source_ID     VARCHAR(255),  /* токен откуда пришел клиент*/      
                                    PRIMARY KEY (ID),
                                    FOREIGN KEY (DesTime_ID) REFERENCES DesTimes(ID),
                                    FOREIGN KEY (Gender_ID) REFERENCES Genders(ID)                                                                  
                                    );               
                              """) 

##    conn.commit()


##/*Внимание, при переносе отключить триггеры, потом включить !!!*/
##/* ключ для SubscrType_ID  не нужен вообще, это поле переопределено*/
    

##    cur.execute("""DROP INDEX  Users_TelegramID_IND ON Users; """)
##    cur.execute("""CREATE INDEX  Users_TelegramID_IND ON Users (TelegramID);  """)
##
##    cur.execute("""DROP INDEX Users_IsActiveBot_IND ON Users; """)
##    cur.execute("""CREATE INDEX  Users_IsActiveBot_IND ON Users (IsActiveBot);""")
##
##    cur.execute("""DROP INDEX Users_DesTime_ID_IND ON Users; """)
##    cur.execute("""CREATE INDEX Users_DesTime_ID_IND ON Users (DesTime_ID); """)
##
##    cur.execute("""DROP INDEX Users_RegDateFin_IND ON Users; """)
##    cur.execute("""CREATE INDEX Users_RegDateFin_IND ON Users (RegDateFin); """)

    
     

    cur.execute("""CREATE TABLE IF NOT EXISTS UserMess(
                                    ID INTEGER   NOT NULL AUTO_INCREMENT,
                                    User_ID INTEGER,
                                    Col_1   INTEGER,
                                    Col_2   INTEGER,
                                    Col_3   INTEGER,
                                    Col_4   INTEGER,
                                    PRIMARY KEY (ID),
                                    FOREIGN KEY (User_ID) REFERENCES Users(ID), 
                                    FOREIGN KEY (Col_1) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_2) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_3) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_4) REFERENCES MessBodies(ID)                                   
                                    );               
                              """)

    cur.execute("""CREATE TABLE IF NOT EXISTS UserSentMess(
                                    ID INTEGER   NOT NULL AUTO_INCREMENT,
                                    User_ID INTEGER,
                                    DateSend DATE,      /*дата отправки данного сообщения*/
                                    Col_1   INTEGER,
                                    Col_2   INTEGER,
                                    Col_3   INTEGER,
                                    Col_4   INTEGER,
                                    PRIMARY KEY(ID),
                                    FOREIGN KEY (User_ID) REFERENCES Users(ID),
                                    FOREIGN KEY (Col_1) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_2) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_3) REFERENCES MessBodies(ID),
                                    FOREIGN KEY (Col_4) REFERENCES MessBodies(ID)                                   
                                    );               
                              """)

    cur.execute("""CREATE TABLE IF NOT EXISTS Buttons(
	                           ID INTEGER   NOT NULL AUTO_INCREMENT,
	                           PostID	VARCHAR(255) NOT NULL,
	                           Source	VARCHAR(255)NOT NULL,
	                           Url	        VARCHAR(255)NOT NULL,
	                           PRIMARY KEY(ID)	
                                   );
                             """)

    cur.execute("""CREATE TABLE IF NOT EXISTS Posts(
	                         ID INTEGER   NOT NULL AUTO_INCREMENT,
	                         Category	VARCHAR(255) NOT NULL,
	                         Time	VARCHAR(5) NOT NULL,
	                         Date	VARCHAR(10) NOT NULL,
	                         ManagerID	VARCHAR(255) NOT NULL,
	                         PostID	VARCHAR(255) NOT NULL,
	                         FirstRow	VARCHAR(255) NOT NULL,
	                         FilePath	VARCHAR(255),
	                         PRIMARY KEY(ID)	
                                 );
                             """)


    cur.execute("""CREATE TABLE IF NOT EXISTS Payments(
	            ID INTEGER NOT NULL AUTO_INCREMENT,
	            sub_type INTEGER NOT NULL, 
	            telegram_id    BIGINT NOT NULL,
	            payment_id VARCHAR(255) NOT NULL, 
	            active_until VARCHAR(10) NOT NULL, 
	            days INTEGER NOT NULL, 
	            payed BOOLEAN NOT NULL, 
	            amount INTEGER NOT NULL, 
	            link VARCHAR(255) NOT NULL, 
	            PRIMARY KEY(ID)		
                    );
                 """) 


    cur.execute("""DROP TRIGGER IF EXISTS AUPD_Users_Birth """)     
    cur.execute("""CREATE TRIGGER  AUPD_Users_Birth AFTER UPDATE ON Users
                  FOR EACH ROW BEGIN
                     IF NEW.BirthTime <> OLD.BirthTime OR
                        NEW.Birthday <> OLD.Birthday OR
                        NEW.Birthplace <> OLD.Birthplace     THEN 
                        UPDATE Users SET DateSend = 0 WHERE ID = OLD.ID;
                     END IF;
                  END;
                  """)
##    
##    cur.execute("""DROP TRIGGER IF EXISTS AUPD_Users_DesTime """)
##    cur.execute("""CREATE TRIGGER AUPD_Users_DesTime  AFTER UPDATE ON  Users
##                    FOR EACH ROW BEGIN
##                    IF OlD.DesTime_ID IS NULL AND NEW.DesTime_ID IS NOT NULL THEN                    
##                       UPDATE Users
##                       SET RegDateFin = NOW()
##                       WHERE ID = OLD.ID;
##                    END IF;    
##                    END;
##                """)
##
##
##    cur.execute("""DROP TRIGGER IF EXISTS AINS_Users """) 
##    cur.execute("""CREATE TRIGGER  AINS_Users AFTER INSERT ON Users
##                   FOR EACH ROW BEGIN
##                      UPDATE Users
##                      SET RegDate = NOW()
##                      WHERE ID = NEW.ID;
##                   END;
##                 """) 

    
    conn.commit()
    HandleMess("База MySql создана/обновлена")
    return(True) 
 except Exception as error:
    HandleMess("Ошибка при начальном заполнении БД : "+ "\n"+ str(error),2)
    return(False) 
 finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
    

##CreateTables()

