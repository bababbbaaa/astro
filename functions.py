import encodings
from getpass import getuser
from tokenize import Token
import requests
import json
import config
import bs4
from bs4 import BeautifulSoup
from horoscopeusr import CreateUsrMess
from sqlalchemy import null
import config
import horoscopeproc
import horoscopeusr as horoscopeusr
import sqlite3
import random
import pathlib
from datetime import *
import horoscopedb as horoscopedb
from config import TOKEN
from horoscopedb import ConnectDb 
from horoscoperr import HandleMess
# from config import TOKEN
DATE_FORMAT = '%d.%m.%Y'

def Get_Data():
    return datetime.datetime.strftime(datetime.datetime.now(), DATE_FORMAT)

    
def send_mes(text, id):
    tok = TOKEN
    Url = "https://api.telegram.org/bot"+tok+"/sendMessage"
    params = {
        "parse_mode": "html",
        "chat_id": id, "text": text,
        "parse_mode": "html"
    }
    request = requests.post(Url, params=params)
    txt=request.text
    txt=json.loads(txt)["ok"]
    if txt==False:
        pass
        #something to understand that user blocked bot
    return(txt)

def managment_check(pict=[], audio=[], video=[], text="", id="", is_manager=True):
    media = []
    
    tok = TOKEN
    files = {}
    is_caption_exists = False
    # media.append({"type":"text","media":text})
    for i in range(len(pict)):
        if not pict[i].filename == "":
            if is_caption_exists == False:
                media.append({"type": "photo", "media": "attach://pict" +
                             str(i), "caption": text, "parse_mode": "html"})
                is_caption_exists = True
                files["pict"+str(i)] = open("data/"+pict[i].filename, "rb")

            else:
                media.append(
                    {"type": "photo", "media": "attach://pict"+str(i)})
                files["pict"+str(i)] = open("data/"+pict[i].filename, "rb")
    for i in range(len(video)):
        if not video[i].filename == "":
            if is_caption_exists == False:
                media.append({"type": "video", "media": "attach://video" +
                             str(i), "caption": text, "parse_mode": "html"})
                is_caption_exists = True
                files["video"+str(i)] = open("data/"+video[i].filename, "rb")

            else:
                media.append(
                    {"type": "video", "media": "attach://video"+str(i)})
                files["video"+str(i)] = open("data/"+video[i].filename, "rb")
    for i in range(len(audio)):
        if not audio[i].filename == "":

            media.append({"type": "audio", "media": audio[i].read(
            ), "caption": text, "parse_mode": "html"})
    Url = "https://api.telegram.org/bot"+tok+"/sendMediaGroup"
    # new_par={
    #     "chat_id":CHAT_ID,
    #     "media":media
    # }
    # media=json.dumps(media)
    params = {
        "parse_mode": "html",
        "chat_id": id, "media":
        json.dumps(media)
    }
    # print(new_par)
    requests1 = requests.post(url=Url, params=params, files=files)
    return(requests1.text)

def teleg_get():
    Url = "https://api.telegram.org/bot"+TOKEN+"/getMe"
    requests1 = requests.post(url=Url)
    return(requests1.text)

def validation(message):
    if len(message)<150 and message.find("/")==-1:
        # for i in range(len(message)):
        #     index=ord(message[i])
        #     # print(index)
        #     if not ((index>=1040 and index<=1103) or (index>=23 and index<=47) or (index>=65 and index<=90) or (index>=97 and index<=122)):
        #         return(0)
    
        return(1)
    else:
        return 0
# print(validation("fkjdjfdkf"))
def validation_post_data(message):
    message=list(map(int,message.split(".")))
    today_data=list(map(int,Get_Data().split(".")))
    # print(today_data)
    month=today_data[1]
    year=today_data[2]
    day=today_data[0]
    if int(message[2])<year:
        return(False)
    if message[1]>12 or message[1]<month:
        
        return(False)
    if message[0]>31 or message[0]<0 :
        
        
        return(False)
    if month==message[1] and message[0]<day:
        return(False)
    return(True)
def create_natal_map(name,birth_day,birth_time,id):
    birth_day=birth_day.split(".")
    day=birth_day[0]
    month=birth_day[1]
    tok=TOKEN
    year=birth_day[2]
    # id=952863788
    birth_time=birth_time.split(":")
    hour=birth_time[0]
    minutes=birth_time[1]
    URL="https://geocult.ru/natalnaya-karta-onlayn-raschet?fn=+"+name+"&fd="+day+"&fm="+month+"&fy="+year+"&fh="+hour+"&fmn="+minutes+"&c1=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F&ttz=20&tz=Europe%2FMoscow&tm=3&lt=55.7522&ln=37.6155&hs=P&sb=1"
    resp=requests.get(URL).text
    soup = BeautifulSoup (resp, 'html.parser')
    soup=soup.find("center")
    soup=soup.findChild().get("href")
    media=[]
    media.append({"type": "photo", "media": "attach://pict1", "caption": "text", "parse_mode": "html"})
    Url = "https://api.telegram.org/bot"+tok+"/sendMediaGroup"
    params = {
    "parse_mode": "html",
    "chat_id": id, "media":
    json.dumps(media)
    }
    files={}
    # print(new_par)
    file=requests.get(soup)
    file=file.content
    # print(file)
    f=open("data/"+str(id)+".png","wb")
    f.write(file)
    f.close()
def validation_date(message):
    try: 
        message=list(map(int,message.split(".")))
        if int(message[2])<1905 or int(message[2]>2022):
            return("not_real_data")
        if message[1]>12 or message[1]<0:
            return("not_real_data")
        if message[0]>31 or message[0]<0:
            return("not_real_data")
        return(1)
    except:
        return("not_real_data")
# print(validation_date("04:01:2005"))

def validation_time(message):
    try: 
        message=list(map(int,message.split(":")))
        if message[1]>60 or message[1]<0:
            return("not_real_data")
        if message[0]>24 or message[0]<0:
            return("not_real_data")
        return(1)
    except:
        return("not_real_data")


def register_user(user,id):
    users=open("users.txt","a")

    for i in user[id]:
        pass

    users.close()

def check_if_exists(id):

    return(0)



def full_delete_user(id):
    UsrFields = ['Name',
               'Gender_ID',
               'BirthTime',
               'Birthday',
               'Birthplace',              
               'DesTime_ID',          
               'TimeZone',
               'IsActiveBot',
               'Source_ID',
               ]
    for i in UsrFields:
        horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName=i,inpValue="")
def RegUser(conn,inpTelegramID):
    try:
     
        cur = conn.cursor()
        # проверить существует ли главный пользователь с  таким же ТЛГ ID

        cur.execute("SELECT IS_Main,IsActiveSub,SubscrType_ID,coalesce(Name,'') FROM Users WHERE  TelegramID = ?" ,(inpTelegramID,));                       

        records = cur.fetchall()
        
        if len(records)>=4:        # не более 4 пользователей с одного ТЛГ ID
            
            HandleMess("Под данным ТЛГ ID уже зарегистрированно 4 польователя, ТЛГ ID :"+inpTelegramID,1,True)
            return((False,"Под данным ТЛГ ID уже зарегистрированно 4 польователя !"))
        elif len(records)>=1:      # найти главного , проверить его подписку и заполненность имени у всех остальных
            mainRow = None
            for row in records:
                IS_Main = row[0]
                IsActiveSub = row[1]
                SubscrType_ID = row[2]
                Name = row[3].strip()          
                if Name == '':
                    HandleMess("У одного из пользователей не указано имя, регистрация доп. пользователей невозможна,ТЛГ ID :"+inpTelegramID,1,True)
                    return((False,"У одного из пользователей не указано имя, регистрация доп. пользователей невозможна"))    
                    
                if IS_Main==1:       # нашли главного                
                    mainRow = row
                    if IsActiveSub != 1:                
                        HandleMess("У гл. пользователя неактивна подписка, регистрация доп. пользователей невозможна,ТЛГ ID :"+inpTelegramID,1,True)
                        return((False,"У гл. пользователя неактивна подписка, регистрация доп. пользователей невозможна"))

                    if SubscrType_ID == 1:
                        HandleMess("У гл. пользователя бесплатная подписка, регистрация доп. пользователей невозможна,ТЛГ ID :"+inpTelegramID,1,True)
                        return((False,"У гл. пользователя бесплатная подписка, регистрация доп. пользователей невозможна"))
                    
            if mainRow == None:
                HandleMess("Не найден, гл пользователь,ТЛГ ID :"+inpTelegramID,1,True)
                return((False,"Ошибка регистрации, попробуйте позднее"))

            # гл пользователь проверки прошел, можно добавлять родственника, данные о подписке будут браться из гл. 

            strQuery = """INSERT INTO Users (Name,TelegramID,IS_Main,RegDate,IsActiveBot,IsActiveSub)                                     
                        VALUES ('',?,0,datetime('now','localtime'),1,1) """
            cur.execute(strQuery,(inpTelegramID,));
            conn.commit()
            return((True,))
            

        # такого пользователя ранее не было - просто добавить гл.
        
        strQuery = """INSERT INTO Users (Name,TimeZone, TelegramID,IS_Main,
                                            RegDate,IsActiveBot,Вalance,IsActiveSub,
                                            SubscrType_ID,ActiveUntil)                                     
                    VALUES ('',0,?,1,
                            datetime('now','localtime'),1,0,1,
                            1,
                            (
                                SELECT date(strftime('%s','now', 'localtime')+Days*86400,'unixepoch') as ActiveUntil 
                                FROM SubscrTypes
                                WHERE SubscrTypes.ID = 1
                            ) )
                        """
        cur.execute(strQuery,(inpTelegramID,));
        conn.commit()
        return((True,))

    except Exception as error:
        pass
        # HandleMess("Ошибка процедуры регистрации пользователя, ТГ ID: "+str(inpTelegramID+"\n"+str(error),3,True))
        return((False,"Ошибка процедуры регистрации, поробуйте позднее"))
    finally:    
        if cur:
            cur.close()



def ConnectDb(): 
 try:
    conn = sqlite3.connect('horoscope.db', check_same_thread=False) 
    return(conn)
 except Exception as error:
    HandleMess("Ошибка подключения к базе: "+DbWay+"\n"+str(error),4)	
    return(None)


#  создать структуру таблиц, некоторые заполнить


def RegMainUser(inpTelegramID):
    try:
        cur = False
        conn = horoscopedb.ConnectDb()
        if conn is None:
            return(None)     
        cur = conn.cursor()
        # проверить существует ли главный пользователь с  таким же ТЛГ ID

        lenMess = horoscopeproc.GetTbLen(conn,"MessBodies")

        cur.execute("SELECT IS_Main,IsActiveSub,SubscrType_ID,coalesce(Name,'') FROM Users WHERE  TelegramID = ?" ,(inpTelegramID,));                       


        records = cur.fetchall()
        conn.commit()
        # conn.close()
        cur.close()
        if len(records)==0:
            horoscopeusr.RegUser(inpTelegramID=inpTelegramID)
            return(True,)
        else:
            return(False,)
    except Exception as err:
        pass
   # такого пользователя ранее не было - просто добавить гл.
   
    # strQuery = """INSERT INTO Users (Name,TimeZone, TelegramID,IS_Main,
    #                                  RegDate,IsActiveBot,Balance,IsActiveSub,
    #                                  SubscrType_ID,ActiveUntil,DateSend,IntrvMessBeg,IntrvMessEnd)                                     
    #            VALUES ('',0,?,1,
    #                    datetime('now','localtime'),1,0,1,
    #                    1,
    #                    (
    #                      SELECT date(strftime('%s','now', 'localtime')+Days*86400,'unixepoch') as ActiveUntil 
    #                      FROM SubscrTypes
    #                      WHERE SubscrTypes.ID = 1
    #                    ),0,?,? )
    #             """
    # cur.execute(strQuery,(inpTelegramID,0,lenMess-1,)); # IntrvMessBeg,IntrvMessEnd - интервал ID таблицы MessBodies из кот были сформ сообщения пользователю
             
    # conn.commit()
   
    # newID = cur.lastrowid      #  добавить пользователю список его собщений - из таблицы MessBodies
    # if not CreateUsrMess(conn,newID,0,lenMess):
    #   return((False,))
    # else:  
    #   return((True,))

# изменить параметры регистрации пользователя по внутр ID
# менять можно не все параметры, а только из списка ниже

def ChUserInfo(conn,inpTelegramID,inpUsrName,inpFieldName, inpValue):
    
 try:
  cur = conn.cursor()
  
  UsrFields = ['Name',
               'Gender_ID',
               'Birthday',
               'BirthTime',
               'Birthplace',
               'CurrLocation',
               'DesTime_ID',          
               'TimeZone',
               'IsActiveBot']

  inpUsrName = inpUsrName.capitalize()   # поле Name, является частью ключа - его вегда приводить к единому виду
  
  for i in range(len(UsrFields)):
     UsrFields[i] = UsrFields[i].capitalize() # привести имена полей к единообразному виду 

  if inpFieldName== "Name".capitalize():     #  имя пользователя привести к единому виду.
     inpValue = inpValue.capitalize()
  
  if not inpFieldName.capitalize() in UsrFields:
     HandleMess("Ошибка имени поля для изменения Users : "+inpFieldName,3,True)
     return(False)

  cur.execute("SELECT 1 FROM Users WHERE (TelegramID = ? AND Name = ?) " ,(inpTelegramID,inpUsrName,))
  records = cur.fetchall()
  
  if len(records) != 1:  
    HandleMess("Колво записей с ключевыми полями, ТЛГ ID: "+str(inpTelegramID)+", Name:"+inpUsrName+"<> 1 \n",3,True)
    return((False,"Ошибка изменения данных для ТЛГ ID: "+str(inpTelegramID)+", Name:"+inpUsrName))

  cur.execute("UPDATE Users SET "+inpFieldName+" = ? WHERE (TelegramID = ? AND Name = ?) " ,(inpValue,inpTelegramID,inpUsrName,))

  conn.commit()
  conn.close() 
  cur.close()
  return((True,)) 
 except Exception as error:
    try:
        HandleMess("Ошибка процедуре изменения Users, ТЛГ ID: "+str(inpTelegramID)+", Name:"+inpUsrName+"\n"+str(error),3,True)
        conn.commit()
        conn.close() 
        cur.close()
        return((False,"Ошибка процедуре изменения Users, ТЛГ ID: "+str(inpTelegramID)+", Name:"+inpUsrName))

    except:
        HandleMess("Ошибка процедуре изменения ",3,True)
        # conn.commit()
        # conn.close() 
        # cur.close()
 finally:    
   if cur:
     cur.close()


def s_ChUserInfo(conn,inpTelegramID,inpFieldName, inpValue):
    
 try:
  cur = conn.cursor()
  
  UsrFields = ['Name',
               'Gender_ID',
               'Birthday',
               'Вirthplace',
               'CurrLocation',
               'DesTime_ID',          
               'TimeZone',
               'IsActiveBot']
  
  for i in range(len(UsrFields)):
     UsrFields[i] = UsrFields[i].capitalize() # привести имена полей к единообразному виду 

  if inpFieldName== "Name".capitalize():     #  имя пользователя привести к единому виду.
     inpValue = inpValue.capitalize()
  
  if not inpFieldName.capitalize() in UsrFields:
     HandleMess("Ошибка имени поля для изменения Users : "+inpFieldName,3,True)
     return(False)

  cur.execute("SELECT 1 FROM Users WHERE (TelegramID = ?) " ,(inpTelegramID,))
  records = cur.fetchall()
  
  if len(records) != 1:  
    HandleMess("Колво записей с ключевыми полями, ТЛГ ID: "+str(inpTelegramID)+", Name:"+"<> 1 \n",3,True)
    return((False,"Ошибка изменения данных для ТЛГ ID: "+str(inpTelegramID)+", Name:"))

  cur.execute("UPDATE Users SET "+inpFieldName+" = ? WHERE (TelegramID = ?) " ,(inpValue,inpTelegramID,))

  conn.commit()
  return((True,)) 
 except Exception as error:
    HandleMess("Ошибка процедуре изменения Users, ТЛГ ID: "+str(inpTelegramID)+"\n"+str(error),3,True)
    return((False,"Ошибка процедуре изменения Users, ТЛГ ID: "+str(inpTelegramID) ))
 finally:    
   if cur:
     cur.close()
     conn.commit()
     conn.close() 
    #  cur.close()


 

def SetConst(conn,inpConstName,inpConstValue):
    
 try:
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Const WHERE Name = ?",(inpConstName,));                       
    records = cur.fetchone()
    if (records == None) or (len(records) == 0):
       cur.execute("INSERT INTO Const (ConstVal, Name) VALUES (?,?) ",(inpConstValue,inpConstName));    
    else:    
       cur.execute("UPDATE Const SET  ConstVal = ? WHERE Name = ? ",(inpConstValue,inpConstName));     

    conn.commit()
    return(True)    
 except Exception as error:
    HandleMess("Ошибка записи константы: "+str(inpConstName)+"\n"+ str(error),4,True)
    return(False)
 finally:    
    if cur:
       conn.commit()
       conn.close() 
       cur.close()


# получить значение константы 
def GetConst(conn,inpConstName):
 try:
    cur = conn.cursor() 
    cur.execute("SELECT ConstVal FROM Const WHERE Name = ?",(inpConstName,));                       
    records = cur.fetchone()
    
    if (records == None) or (len(records) == 0):
       return(None)
    
    currVal = records[0]
    return(currVal)    
 except Exception as error:
    HandleMess("Ошибка чтения константы: "+str(inpConstName)+"\n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
       conn.commit()
       conn.close() 



# найти случайное число от 1 до messcount 

def FindRndDayHeader(messcount):
    currChoice = random.randint(1,messcount)
    return(currChoice)
 
#  количество строк в таблице

def GetTbLen(conn,inpTbName):
 try:
   cur = conn.cursor()
   cur.execute("SELECT 1 FROM "+inpTbName);                       
   records = cur.fetchall()
   if records == None:
      return(0)
   return(len(records))
 except Exception as error:
    HandleMess("Ошибка подсчета кол-ва строк в таблице: "+str(inpTbName)+"\n"+ str(error),4,True)
    return(0)
 finally:    
    if cur:
       cur.close()


# получить любое поле любой таблицы по ID
def GetAnyFieldOnID(conn,inpTbName,inpFieldName,inpID):
 try:
   cur = conn.cursor()
   cur.execute("SELECT "+inpFieldName+" FROM "+inpTbName+" WHERE ID = ?",(inpID,));                       
   records = cur.fetchone()  
   if (records == None) or (len(records) == 0):
       return(None)
    
   return records[0]

 except Exception as error:
    HandleMess("Ошибка получения знач поля "+inpFieldName+" из таблицы "+inpTbName+"\n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
    

# сформировать все сообщения для активных главных пользователей в этот час
def GenHourMessAll(inpDesTimeID):

 # подключиться к базе

 try:
    cur = False
    conn = ConnectDb()
    if conn is None: 
         
       exit() 
    cur = conn.cursor()
    # размер таблиц с текстами
    
    bodyLen = GetTbLen(conn,"MessBodies")
    headLen = GetTbLen(conn,"MessHeaders")
    if bodyLen == 0 or headLen == 0: 
       HandleMess("Пустая таблица заголовков или текстов ",4,True)
       return(None)
    
    # если начало суток - найти новый заголовок на сегодня, сохранить в константах
    if inpDesTimeID == 0:  
      CurrHeaderID =  FindRndDayHeader(bodyLen)
      resSet = SetConst(conn,"TodayHeadID",CurrHeaderID) #  сохранить заголовок в константах  на весь день
      if not resSet:
         return(None) 
    else:  
      CurrHeaderID = GetConst(conn,"TodayHeadID")
      if CurrHeaderID == None:
         return(None)  
    
    CurrHeaderTXT = GetAnyFieldOnID(conn,"MessHeaders","Header",CurrHeaderID)
    if CurrHeaderTXT == None:
       HandleMess("Ошибка поиска заголовка дня : "+str(CurrHeaderID)+"\n"+ str(error),4,True) 
       return(None)

    # выбрать всех главных активных для этого часа 
    cur.execute("""SELECT ID,Name, TelegramID FROM Users
                   WHERE (IS_Main = 1 AND IsActiveSub = 1 AND DesTime_ID = ? )""",(inpDesTimeID,));

    resList = list()
    records = cur.fetchall()
    for row in records:
      UserID = row[0]
      CurrName   = row[1]
      CurrTelegramID = row[2] 
       
      CurrMessTXT = GenMess(conn,UserID,bodyLen)
      resList.append((CurrTelegramID,CurrName,CurrHeaderTXT,CurrMessTXT,"")) 
          
    return(resList)
    
 except Exception as error:
    HandleMess("Ошибка процедуры формирования текста г. для часа: "+str(inpDesTimeID)+"\n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()   

    

# сформировать случайный список с удалением одинаковых элементов
def GetListInd(messcount,totCh):    
    listInd = list() 
    currChoice = random.randint(0,totCh)
    
    for i in range(4):
       res =  divmod(currChoice,messcount)
       currChoice = res[0]
       listInd.append(str(res[1]))

    reslist = list(set(listInd)) # удаляем одинаковые элементы
    return(reslist) 


def ListUserName(inpTelegramID):
    conn=horoscopedb.ConnectDb()
    try:
        cur = conn.cursor()   
        cur.execute("SELECT Name FROM Users WHERE (TelegramID = ?) ORDER BY IS_Main DESC" ,(inpTelegramID,))
        res = list()
        records = cur.fetchall()
        for row in records:
            res.append(row[0])
        return(res)
            
    except Exception as error:
        HandleMess("Ошибка процедуры ListUsersName, ТЛГ ID: "+inpTelegramID+"\n"+str(error),3,True)
        return(list())
    finally:    
        if cur:
            cur.close()
            conn.commit()

def count_payments():
    conn=sqlite3.connect('payments.db')
    cur=conn.cursor()
    cur.execute("SELECT count(*) FROM Payments")
    length=cur.fetchall()
    cur.close()
    conn.close()
    return int(length[0][0])+10000
print(count_payments())
def GetUsers(inpTelegramID):
    try:
        conn=horoscopedb.ConnectDb()
        cur = conn.cursor()   
        cur.execute("SELECT * FROM Users WHERE (TelegramID = ?)" ,(str(inpTelegramID),))
        res = list()
        records = cur.fetchall()
        cur.close()
        conn.commit()
        for row in records:
            res.append({"ID":row[0],"Name":row[1],"is_main":row[2],"BirthTime":row[4],
        "Birthday":row[5],"Gender_ID":row[3],'Birthplace':row[6],"DesTime_ID":row[7],
        "TimeZone":row[8],"TelegramID":row[9],"RegDate":row[10],"IsActiveBot":row[12],
        "Balance":row[13],"IsActiveSub":row[14],"SubscrType_ID": row[15],
        "ActiveUntil":row[16],"DateSend":row[17],"Source_ID":row[22]
        })
        return(res)
    except Exception as err:
        return([])
    finally:    
        if cur:
            cur.close()



def select_all_active_until_table(id=None):
    try:

        today_data=datetime.now()
        conn=horoscopedb.ConnectDb()
        cur = conn.cursor()
        if id ==None:
            cur.execute("SELECT TelegramID, ActiveUntil FROM Users")
        else:
            cur.execute("SELECT TelegramID, ActiveUntil FROM Users WHERE (TelegramID = ?)",(id,))
        res = list()
        records = cur.fetchall()
        cur.close()
        conn.commit()
        for row in records:
            if row[1]!="":
                end_date=datetime.strptime(row[1],"%Y-%m-%d")
                days_till_end=end_date-today_data
                days_till_end=days_till_end.days
                end_date=datetime.strftime(end_date,"%d.%m.%Y")
                res.append({"id":row[0],"active_until":end_date,"days_till_end":days_till_end})
        res[0]=dict(res[0])
        if id==None:
            return res
        else:
            return(res[0])
    except Exception as error:
        return(list())
    finally:    
        if cur:
            cur.close()
            conn.close()



def validation_everything(text,type):
    if type=="birth_place" or type=='Место проживания' or type=="Name" or type=="BirthTime":
        return(validation(text),text)
    if type=="Birthday":
        if validation_date(text)=="not_real_data":
            return(False,0)
        else:
            return(True,text)
    if type=="Время рождения":
        return(validation_time(text))
    if type=="Gender_ID":
        if text=="м" or text=="М":
            return(True,1,)
        elif text=="ж" or text=="Ж":
            return(True,0,)
        else:
            return(False,0)

def shedule_time_changer(inpTelegramID,shedule_time):
    try:
        conn=horoscopedb.ConnectDb()
        cur = conn.cursor() 
        cur.execute("UPDATE Users SET DesTime_ID = ? WHERE (TelegramID = ?)" ,(int (shedule_time),str(inpTelegramID),))
        conn.commit()




    except:
        pass
    finally:    
        if cur:
            cur.close()
            conn.commit()

# shedule_time_changer(ConnectDb(),952863788,10)




def GenMess(UserID,messcount):

 try:    
    conn=horoscopedb.ConnectDb()
    totCh = messcount**4-1
    cur = conn.cursor()
    
    # бывают одинаковые значения, и запрос их объединяет
    # повторяем пока все элементы не будут разными, т.е. разм списка =4
    
    for i in range(99): 
      listInd = GetListInd(messcount,totCh)  
      if len(listInd)==4: break     
    else:
      HandleMess("Ошибка поиска случайного значения для User ID: "+str(UserID),4,True)
      return(None)
     
    cur = conn.cursor()
    strofIDs = ",".join(listInd)       

    strQuery = """SELECT ID,
                         Col_1,
                         Col_2,
                         Col_3,
                         Col_4
                  FROM MessBodies WHERE ID IN({})
                  """.format(strofIDs)
    cur.execute(strQuery)
    records = cur.fetchall()
    resStr = records[0][1]+"\n"+records[1][2]+"\n"+records[2][3]+"\n"+records[3][4]    

    return(resStr)
 except Exception as error:
   HandleMess("Ошибка процедуры поиска случайного значения для User ID: "+str(UserID)+"\n"+ str(error),4,True)
   return(None)
 finally:    
    if cur:
       cur.close()
       conn.commit()
       cur.close()




# conn=ConnectDb()
# print(ChUserInfo(conn=conn,inpValue="test",inpID=str(952863788),inpFieldName="Вirthplace"))\



def s_GetAnyFieldOnID(conn,inpTbName,inpFieldName,inpTelegramID):
    try:
        cur = conn.cursor()
        cur.execute("SELECT "+inpFieldName+" FROM "+inpTbName+" WHERE TelegramID = ?",(inpTelegramID,));                       
        records = cur.fetchone()  
        if (records == None):
            return(None)
            
        return records[0]

    except Exception as error:
        HandleMess("Ошибка получения знач поля "+inpFieldName+" из таблицы "+inpTbName+"\n"+ str(error),4,True)
        return(None)
    finally:    
        if cur:
            cur.close()

def s1_GetAnyFieldOnID(conn,inpTbName,inpFieldName,inpTelegramID,name):
    try:
        cur = conn.cursor()
        cur.execute("SELECT "+inpFieldName+" FROM "+inpTbName+" WHERE (TelegramID = ? AND Name = ?) ",(inpTelegramID,name));                       
        records = cur.fetchone()  
        if (records == None):
            return(None)
            
        return records[0]

    except Exception as error:
        HandleMess("Ошибка получения знач поля "+inpFieldName+" из таблицы "+inpTbName+"\n"+ str(error),4,True)
        return(None)
    finally:    
        if cur:
            cur.close()
            
# print(s1_GetAnyFieldOnID(conn=ConnectDb(),inpTbName="Users",inpFieldName="Birthday",inpTelegramID="952863788",name="Никита"))
# ChUserInfo(conn="conn",inpValue="Сергей",inpTelegramID=952863788,inpFieldName=None,inpUsrName="name")
# RegMainUser(conn,str(952863788))
# print(GetUsers(conn=conn,inpTelegramID="952863788"))

# print(ChUserInfo(conn=conn,inpValue="Сергей",inpTelegramID=str(952863788),inpFieldName="Name",inpUsrName="as"))
# shedule_time_changer(conn=conn,inpTelegramID=952863788,shedule_time=int(12))


# print(GenHourMessAll(0))
# # print(GenHourMessAll(10))
# send_mes(id=952863788,text='''орогой Сергец, сегодня, 03 июня.