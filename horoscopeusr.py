import horoscopedb
import horoscopeproc
from horoscoperr import HandleMess
import random
from datetime import date, datetime, timedelta



# добавить пользователя в базу данных,  подписка начальная
#в случае успеха  возвращает кортеж (True,)
#в случае ошибки возвращает кортеж (False,Описание ошибки)

def RegUser(inpTelegramID):
 try:

   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,"Ошибка подключения к БД",4,))
   cur = conn.cursor()
   # проверить существует ли главный пользователь с  таким же ТЛГ ID

   
   
   cur.execute("SELECT Name FROM Users WHERE  TelegramID = %s" ,(inpTelegramID,))                       
   
   
   records = cur.fetchall()

   if len(records)>=1:        # пользователь уже зарегистрирован
      
      HandleMess("Пользователь уже зарегистрирован, ТЛГ ID :"+str(inpTelegramID)+", имя: "+records[0][0],1,True)
      return((False,"Пользователь уже зарегистрирован, ТЛГ ID :"+str(inpTelegramID)+", имя: "+records[0][0],1,))

   
   
   # такого пользователя ранее не было - просто добавить гл.
   lenMess = horoscopeproc.GetTbLen(conn,"MessBodies")
   
   strQuery = """INSERT INTO Users (Name,TimeZone, TelegramID,IS_Main,
                                     IsActiveBot,Balance,IsActiveSub,SubscrType_ID,
                                     ActiveUntil,DateSend,IntrvMessBeg,IntrvMessEnd)                                     
                 VALUES ('',0,%s,1,
                         1,0,1,1,                         
                         NOW(),DATE_SUB(NOW(), INTERVAL 100 YEAR),%s,%s)
                """

##   NOW(),DATE_SUB(NOW(), INTERVAL 300 YEAR),%s,%s)*/
   cur.execute(strQuery,(inpTelegramID,0,-1,)) # IntrvMessBeg,IntrvMessEnd - интервал ID таблицы MessBodies из кот были сформ сообщения пользователю
   ##cur.execute(strQuery,(inpTelegramID,0,lenMess-1,)) # IntrvMessBeg,IntrvMessEnd - интервал ID таблицы MessBodies из кот были сформ сообщения пользователю          
   conn.commit()
   
##   newID = cur.lastrowid      #  добавить пользователю список его собщений - из таблицы MessBodies
##   if not CreateUsrMess(conn,newID,0,lenMess):  # регистрация будет вызываться отдельно
##      return((False,"",2,))
##   else:
   return((True,"",3,))

 except Exception as error:
   HandleMess("Ошибка процедуры регистрации пользователя, ТГ ID: "+str(inpTelegramID)+"\n"+str(error),3,True)
   return((False,"Ошибка процедуры регистрации, поробуйте позднее",4,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 




## inpValues- словарь содержащий Name,Gender_ID,Birthday,DesTime_ID,BirthTime,Birthplace
def RegUserFull(inpTelegramID,inpValues):
 try:

   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,"Ошибка подключения к БД",4,))
   cur = conn.cursor()
   # проверить существует ли главный пользователь с  таким же ТЛГ ID

   
   
   cur.execute("SELECT Name FROM Users WHERE  TelegramID = %s" ,(inpTelegramID,))                       
   
   
   records = cur.fetchall()

   if len(records)==0:        # пользователь уже зарегистрирован
      
      HandleMess("Пользователь не зарегистрирован, ТЛГ ID :"+str(inpTelegramID),True)
      return((False,"Пользователь не  зарегистрирован, ТЛГ ID :"+str(inpTelegramID)))

   
   
   # такого пользователя ранее не было - просто добавить гл.
   lenMess = horoscopeproc.GetTbLen(conn,"MessBodies")
   
##   strQuery = """INSERT INTO Users (Name,Gender_ID,Birthday,DesTime_ID,BirthTime,Birthplace,
##                                    TimeZone, TelegramID,IS_Main,
##                                     IsActiveBot,Balance,IsActiveSub,SubscrType_ID,
##                                     RegDate,RegDateFin,
##                                     ActiveUntil,DateSend,IntrvMessBeg,IntrvMessEnd)                                     
##                 VALUES (%s,%s,%s,%s,%s,%s,
##                         0,%s,1,
##                         1,0,1,1,
##                         NOW(), NOW(),
##                         DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY) ,0,0,-1)
##                """

   strQuery = """UPDATE  Users SET Name = %s,
                                     Gender_ID = %s,
                                     Birthday = %s,
                                     DesTime_ID = %s,
                                     BirthTime = %s,
                                     Birthplace = %s,                                                                    
                                     RegDate = NOW(),
                                     RegDateFin = NOW(),
                                     ActiveUntil = DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY)                 
                 WHERE TelegramID = %s        
                """


   
   cur.execute(strQuery,(inpValues['Name'],inpValues['Gender_ID'],inpValues['Birthday'],inpValues['DesTime_ID'],inpValues['BirthTime'],inpValues['Birthplace'],
                         inpTelegramID,)) # IntrvMessBeg,IntrvMessEnd - интервал ID таблицы MessBodies из кот были сформ сообщения пользователю
   
   ##cur.execute(strQuery,(inpTelegramID,0,lenMess-1,)) # IntrvMessBeg,IntrvMessEnd - интервал ID таблицы MessBodies из кот были сформ сообщения пользователю          
   conn.commit()
   
##   newID = cur.lastrowid      #  добавить пользователю список его собщений - из таблицы MessBodies
##   if not CreateUsrMess(conn,newID,0,lenMess):  # регистрация будет вызываться отдельно
##      return((False,"",2,))
##   else:
   return((True,"",3,))

 except Exception as error:
   HandleMess("Ошибка процедуры регистрации пользователя, ТГ ID: "+str(inpTelegramID)+"\n"+str(error),3,True)
   return((False,"Ошибка процедуры регистрации, поробуйте позднее",4,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 






## пользователю с UserID  добавить список сообщений, просто перемешанных номеров от begMess до endMess по 4 колонкам
def CreateUsrMess(conn,UserID,begMess,endMess):
 try:  
   cur = conn.cursor()
   lst_1 = list(range(begMess, endMess))
   lst_2 = list(range(begMess, endMess))
   lst_3 = list(range(begMess, endMess))
   lst_4 = list(range(begMess, endMess))
   random.shuffle(lst_1)
   random.shuffle(lst_2)
   random.shuffle(lst_3)
   random.shuffle(lst_4)
   reslist = list()
   for i in range (0,len(lst_1)):
      reslist.append((UserID,lst_1[i],lst_2[i],lst_3[i],lst_4[i],)) 
   
  
   cur.executemany("INSERT INTO UserMess (User_ID,Col_1,Col_2,Col_3,Col_4) VALUES(%s, %s, %s, %s, %s)", reslist)
   conn.commit()
   return True
 except Exception as error:
   HandleMess("Ошибка процедуры формирования сообщений для User ID: "+str(UserID)+"\n"+str(error),3,True)
   return False
 finally:    
   if cur:
      cur.close()
      
# сформировать сообщения отдельному пользователю по ТЛГ ID      
def GenNewUserMess(inpTelegramID):
 try:

   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,"Ошибка подключения к БД",4,))
   cur = conn.cursor()
   

   cur.execute("SELECT ID FROM Users WHERE  TelegramID = %s" ,(inpTelegramID,))                       
   records = cur.fetchall()
   
   if len(records)==0:        # пользователь не зарегистрирован      
      HandleMess("Пользователь не зарегистрирован, ТЛГ ID :"+str(inpTelegramID),True)
      return((False,"Пользователь не зарегистрирован, ТЛГ ID :"+str(inpTelegramID)))
   CurrID = records[0][0]

   
   # если у пользователя есть сообщения - ему не генерировать
   cur.execute("SELECT ID FROM UserMess WHERE  User_ID = %s" ,(CurrID,))
   records = cur.fetchall()
   
   
   if len(records)!=0:
      return((True,"У пользователя уже есть сообщения , ТЛГ ID :"+str(inpTelegramID),3,))       
             
   lenMess = horoscopeproc.GetTbLen(conn,"MessBodies") 
   if not CreateUsrMess(conn,CurrID,0,lenMess):  # регистрация будет вызываться отдельно
      return((False,"",2,))
  
   cur.execute("UPDATE Users SET IntrvMessEnd = %s WHERE ID = %s ",(lenMess-1,CurrID,))   
   conn.commit() 
   return((True,"",3,))
  

 except Exception as error:
   HandleMess("Ошибка процедуры регистрации пользователя, ТГ ID: "+str(inpTelegramID)+"\n"+str(error),3,True)
   return((False,"Ошибка процедуры регистрации, поробуйте позднее",4,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 

      
# проверить и догенерировать сообщения всем пользователям
#
#
def GenAllUsrMess():
 try:

   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,"Ошибка подключения к БД",4,))

   lenMess = horoscopeproc.GetTbLen(conn,"MessBodies") # размер таблицы сообщений
   lastID  = lenMess-1
   
   cur = conn.cursor()
   cur.execute("SELECT ID,IntrvMessEnd FROM Users WHERE IntrvMessEnd < %s ",(lastID,) )

   usrList = list()   
   records = cur.fetchall()
##   print(str(len(records)))
   
   if len(records) == 0:
      return True
    
   for row in records:
      currID  = row[0]
      currEND = row[1]  # -1 тоже самое что 199 (была ошибка один день, не было соммита)
      if currEND==-1:
         currEND = 199 
      #print(str(currID)+" "+str(currEND))
##      if currEND >= lastID:
##        continue
      if not CreateUsrMess(conn,currID,currEND+1,lenMess):
        print("Ошибка генерации сообщений для User ID "+str(currID))  
        return False
      usrList.append((lastID,currID,))
##   print(usrList)   
   cur.executemany("UPDATE Users SET IntrvMessEnd = %s WHERE ID = %s ",usrList)  
##    cur.execute("UPDATE Users SET IntrvMessEnd = ? WHERE ID = ?  " ,(lastID,currID,))
   conn.commit()





   return True
 except Exception as error:
   HandleMess("Ошибка процедуры добавления сообщений пользователям \n"+str(error),3,True)
   print("Ошибка "+str(error))
   return False
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 


   
 
# изменить параметры регистрации пользователя по ТЛГ ID
# менять можно не все параметры, а только из списка ниже

def ChUserInfo(inpTelegramID,inpFieldName, inpValue):


 try:
  cur = False
  conn = horoscopedb.ConnectDb()
  if conn is None:      
        return((False,))
  cur = conn.cursor()
  
  UsrFields = ['Name',
               'Gender_ID',
               'BirthTime',
               'Birthday',
               'Birthplace',              
               'DesTime_ID',          
               'TimeZone',
               'IsActiveBot',
               'Source_ID',
               'ActiveUntil',
               'SubscrType_ID',
               "IsActiveSub"
               ]

  for i in range(len(UsrFields)):
     UsrFields[i] = UsrFields[i].capitalize() # привести имена полей к единообразному виду 

  inpFieldName = inpFieldName.capitalize()

  
  if not inpFieldName in UsrFields:
     HandleMess("Ошибка имени поля для изменения Users : "+inpFieldName,3,True)
     return(False,)

  cur.execute("SELECT 1 FROM Users WHERE TelegramID = %s " ,(inpTelegramID,))
  records = cur.fetchall()
  
  if len(records) != 1:  
    HandleMess("Не зарегистрирован  ТЛГ ID: "+inpTelegramID ,3,True)
    return(False,"Не зарегистрирован  ТЛГ ID: "+inpTelegramID,)

  cur.execute("UPDATE Users SET "+inpFieldName+" = %s WHERE TelegramID = %s  " ,(inpValue,inpTelegramID,))

  conn.commit()
  return(True,)
 except Exception as error:
    HandleMess("Ошибка процедуре изменения Users, ТЛГ ID: "+inpTelegramID+"\n"+str(error),3,True)
    return(False,"Ошибка процедуры изменения Users, ТЛГ ID: "+inpTelegramID+", поле :"+inpFieldName,)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 

     

# список имен пользователей по тлг ID, глав польз  идет первым в списке

def ListUserName(conn,inpTelegramID):
 try:
  cur = conn.cursor()   
  cur.execute("SELECT Name FROM Users WHERE (TelegramID = %s) ORDER BY IS_Main DESC" ,(inpTelegramID,))
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

######################## процедуры временных пользователей
# зарегистрировать временного пользователя 
def RegTmpUser(inpTelegramID):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,"Ошибка подключения к БД",4,))
   cur = conn.cursor()
   
   cur.execute( """INSERT INTO UsersTmp (TelegramID)
                 VALUES (%s)""",(inpTelegramID,));
   
   conn.commit()
   return((True,"",3,))
 except Exception as error:
   HandleMess("Ошибка процедуры регистрации временного пользователя, ТГ ID: "+inpTelegramID+"\n"+str(error),3,True)
   return((False,"Ошибка процедуры регистрации временного пользователя, поробуйте позднее",4,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 

  
               
### удалить временного пользователя 
def DelTmpUser(inpTelegramID=None):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,"Ошибка подключения к БД",4,))
   cur = conn.cursor()
   if inpTelegramID == None:
      cur.execute("DELETE FROM UsersTmp");                        
   else:    
      cur.execute("DELETE FROM UsersTmp WHERE  TelegramID = %s" ,(inpTelegramID,));                       
   conn.commit()
   return((True,"",3,))
 except Exception as error:
   HandleMess("Ошибка процедуры удаления временного пользователя, ТГ ID: "+inpTelegramID+"\n"+str(error),3,True)
   return((False,"Ошибка процедуры удаления временного пользователя, поробуйте позднее",4,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()

       
# получить информацию о временном пользователе
def GetTmpUserInfo(inpTelegramID):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,"Ошибка подключения к БД",4,))
   cur = conn.cursor()
   
   cur.execute("SELECT  TelegramID,Name,Gender_ID,Birthday FROM UsersTmp WHERE  TelegramID = %s ORDER BY ID DESC LIMIT 1" ,(inpTelegramID,));                       
   records = cur.fetchall()
   if len(records)>0:
      row = records[0]
      return((True,"",3,{"TelegramID":row[0],"Name":row[1],"Gender_ID":row[2],"Birthday":row[3]},)) 
   else:   
      return((False,"",3,))  
              
 except Exception as error:
   HandleMess("Ошибка процедуры ""GetTmpUserInfo"", ТГ ID: "+inpTelegramID+"\n"+str(error),3,True)
   return((False,"Ошибка процедуры ""GetTmpUserInfo"", поробуйте позднее",4,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()

       
def ChTmpUserInfo(inpTelegramID,inpFieldName, inpValue):

 try:
  cur = False
  conn = horoscopedb.ConnectDb()
  if conn is None:      
        return((False,))
  cur = conn.cursor()
  
  UsrFields = ['Name',
               'Gender_ID',               
               'Birthday',
               'Birthplace']

  for i in range(len(UsrFields)):
     UsrFields[i] = UsrFields[i].capitalize() # привести имена полей к единообразному виду 

  inpFieldName = inpFieldName.capitalize()

  
  if not inpFieldName in UsrFields:
     HandleMess("Ошибка имени поля для изменения UsersTmp : "+inpFieldName,3,True)
     return((False,))

  cur.execute("SELECT 1 FROM UsersTmp WHERE TelegramID = %s " ,(inpTelegramID,))
  records = cur.fetchall()
  
  if len(records) == 0:  
    HandleMess("Не зарегистрирован временный ТЛГ ID: "+inpTelegramID ,3,True)
    return((False,"Не зарегистрирован временный ТЛГ ID: "+inpTelegramID,))


  cur.execute("UPDATE UsersTmp SET "+inpFieldName+" = %s WHERE ID = (SELECT MAX(ID) FROM UsersTmp WHERE TelegramID = %s)", (inpValue,inpTelegramID,))
   

  conn.commit()
  return((True,))
 except Exception as error:
    HandleMess("Ошибка процедуре изменения Users, ТЛГ ID: "+inpTelegramID+"\n"+str(error),3,True)
    return(False,"Ошибка процедуры изменения Users, ТЛГ ID: "+inpTelegramID+", поле :"+inpFieldName,)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 




##inpValues = {"Name":"Sasa","Gender_ID":1,"Birthday":'23.12.2022',"DesTime_ID":1,"BirthTime":'23:59',"Birthplace":'fff'}
##RegUserFull(121212121299,inpValues)
##print(GenNewUserMess(121212121212))
##conn = horoscopedb.ConnectDb()
##print(RegUser(123456789))
##CreateUsrMess(conn,1,0,10)
##print(ChUserInfo("123","Source_ID", 3) )
##print(ChUserInfo(conn,"1234","sasa","DesTime_id", "10") )

##old = datetime.now()
##print(GenNewUserMess(123456789))
##print("tot="+str(datetime.now()-old))
       

##print(DelTmpUser())       
##print(GetTmpUserInfo("12345")[3]["Birthday"])
##print(RegTmpUser("12345"))
##print(ChTmpUserInfo("12345","Name","ыыыыы"))
##print(datetime.datetime.now())
##print(GenAllUsrMess())
##print(datetime.datetime.now())

##print(RegUser(121212121237))
##print(RegTmpUser(121212121212))
##print(ChUserInfo(121212121212,"Source_ID", 5) )
