import datetime
import horoscopedbMySQL




# процедура создает бд в MYSQL затем копирует  данные из SQLite предварительно их обрабатывая

def CleanMySql():
 connMySql = horoscopedbMySQL.ConnectMySql()
 if connMySql is None:      
   return(False)
 curMySql = False
 try:
   curMySql = connMySql.cursor()
   curMySql.execute("DELETE FROM Directions")
   connMySql.commit()

   print("Удаление UserMess")
   curMySql.execute("DELETE FROM UserMess")
   print("Закончено удаление   UserMess")
   connMySql.commit()
   curMySql.execute("DELETE FROM UserSentMess")
   
   curMySql.execute("DELETE FROM Users")
   connMySql.commit()
   curMySql.execute("DELETE FROM UsersTmp")
   curMySql.execute("DELETE FROM MessHeaders")
   curMySql.execute("DELETE FROM MessHeaders_1")
   curMySql.execute("DELETE FROM MessBodies")
   curMySql.execute("DELETE FROM MessBodies_1")
   curMySql.execute("DELETE FROM Buttons")
   curMySql.execute("DELETE FROM Posts")
   curMySql.execute("DELETE FROM Sources")
   curMySql.execute("DELETE FROM Subscriptions")
   curMySql.execute("DELETE FROM Payments")
   
   curMySql.execute("DELETE FROM Genders")
   curMySql.execute("DELETE FROM DesTimes")
   connMySql.commit()
   return(True)  
 except Exception as error:
   connMySql.rollback() 
   print("Ошибка при очистке БД : "+ "\n"+ str(error),2)
   return(False)  
 finally:
    if curMySql:
        curMySql.close()
    if connMySql:
        connMySql.close()    


# почистить гендер
def ClearGender(inpG):
   if inpG == None:  return(None)
   if inpG != 1:     return(2)
   return(1)

# почистить таблицу  пользвателей
def CleanTbUsersTmp(inpRec):
   
   resList = list()   
   for row in inpRec:
      curL = list(row)   
      curL[3] = ClearGender(row[3])   # почистить гендер
      resList.append(tuple(curL)) 
       
   return(resList)

# почистить таблицу врем польз
def CleanTbUsers(inpRec):
   
   resList = list()   
   for row in inpRec:
      curL = list(row)   
      curL[3] = ClearGender(row[3]) # почистить гендер
      curL[8] = 0                   # поле TimeZone
      if curL[12]=="":     curL[12] = 0         # IsActiveBot
      if curL[22]=="":     curL[22] = None      # Source_ID
      if curL[7]=="":      curL[7]= None        # DesTime_ID      
      if curL[4] != None:  curL[4] = str(curL[4])[:10]    # BirthTime обрезать до 10 симв
      if curL[19] == -1:   curL[19] = 199     #IntrvMessEnd
      resList.append(tuple(curL)) 
       
   return(resList)

# почистить таблицу врем польз
def CleanTbPayments(inpRec):
   
   resList = list()   
   for row in inpRec:
      curL = list(row)
      if curL[2]!="" and  curL[3]!="":
          resList.append(tuple(curL)) 
       
   return(resList)

         
#  скопировать табл из Sqlite в mySql
def CopySimplTable(curDb,curMySql,inpFields,inpTbName,corrProc=""):

    resS = ""
    for i in range(inpFields.count(",")):
        resS = resS +"%s,"
    resS = resS +"%s"
   
    curDb.execute("SELECT "+ inpFields+ " FROM "+inpTbName)    
    recDb =curDb.fetchall()
    
    if corrProc!= "":   # вызвать процедуру корр данных
       recDb = corrProc(recDb)
 
    curMySql.executemany("INSERT INTO "+inpTbName+"("+inpFields+")  VALUES ("+ resS+")",recDb)
    

def CopyMainDbToMySql():


 if not horoscopedbMySQL.CreateTablesMySqlNoTrigg():
    print("Ошибка создания БД в MySQL")
    return(False)
 print("очистка таблиц")
 if not CleanMySql():
    return(False)


 curDb = False
 curMySql = False
 connDb = horoscopedbMySQL.ConnectDb()
 if connDb is None:      
   return(False)

 connMySql = horoscopedbMySQL.ConnectMySql()
 if connMySql is None:      
   return(False)

 
 try:
       
    curDb = connDb.cursor()
    curMySql = connMySql.cursor()

    print("Перенос таблиц") 
    CopySimplTable(curDb,curMySql,"ID,Name","Genders")
    CopySimplTable(curDb,curMySql,"ID,Name","Directions") 
    CopySimplTable(curDb,curMySql,"ID,DesTimeBegin,Name","DesTimes")
    CopySimplTable(curDb,curMySql,"ID,MessDate,Header","MessHeaders")
    CopySimplTable(curDb,curMySql,"ID,MessDate,Header","MessHeaders_1")    
    CopySimplTable(curDb,curMySql,"ID,Col_1,Col_2,Col_3, Col_4","MessBodies")
    CopySimplTable(curDb,curMySql,"ID,Col_1,Col_2,Col_3, Col_4","MessBodies_1")    
    CopySimplTable(curDb,curMySql,"ID,PostID,Source,Url","Buttons")
    CopySimplTable(curDb,curMySql,"ID,Category,Time,Date,ManagerID,PostID,FirstRow,FilePath","Posts")    
    CopySimplTable(curDb,curMySql,"ID,Name,Token","Sources") 
    CopySimplTable(curDb,curMySql,"ID,TelegramID,Type,Start,End,PayID","Subscriptions")    
    CopySimplTable(curDb,curMySql,"ID,TelegramID,Name,Gender_ID,Birthday,Birthplace,Col_1,Col_2,Col_3,Col_4","UsersTmp",CleanTbUsersTmp) 

    print("Перенесены мелкие справочники")

    print("Начало переноса Users")
    CopySimplTable(curDb,curMySql,"""ID,Name,IS_Main,Gender_ID,BirthTime,Birthday,Birthplace,DesTime_ID,TimeZone,TelegramID,
                                    RegDate,RegDateFin,IsActiveBot,Balance,IsActiveSub,SubscrType_ID,ActiveUntil,DateSend,IntrvMessBeg,IntrvMessEnd,
                                    StdShutoff,TryPayRem, Source_ID ""","Users",CleanTbUsers)
    
    print("Перенос Users окончен")
    CopySimplTable(curDb,curMySql,"ID,User_ID,DateSend,Col_1,Col_2,Col_3,Col_4","UserSentMess")
    print("Начало переноса UserMess "+str(datetime.datetime.now()))
    CopySimplTable(curDb,curMySql,"ID,User_ID,Col_1,Col_2,Col_3,Col_4","UserMess")    
    print("Конец переноса UserMess "+str(datetime.datetime.now()))


    connMySql.commit()
##    horoscopedbMySQL.CreateTablesMySqlOnlyTrigg()
    print("Перенос данных окончен")
    return(True)    
 except Exception as error:
   connMySql.rollback() 
   print("Ошибка при начальном заполнении БД : "+ "\n"+ str(error),2)
   return(False)  
 finally:
    if curDb:
        curDb.close()
    if connDb:
        connDb.close()
        
    if curMySql:
        curMySql.close()
    if connMySql:
        connMySql.close()
        
#
#
def CopyPayDbToMySql():
 curDb = False
 curMySql = False
 connDb = horoscopedbMySQL.ConnectDb(True)
 if connDb is None:      
   return(False)

 connMySql = horoscopedbMySQL.ConnectMySql()
 if connMySql is None:      
   return(False)
 try:
       
    curDb = connDb.cursor()
    curMySql = connMySql.cursor()
    CopySimplTable(curDb,curMySql,"ID,sub_type,telegram_id,payment_id,active_until,days,payed,amount,link","Payments",CleanTbPayments)

    print("Перенесена таблица Payments")
    return(True)    
    
 except Exception as error:
   connMySql.rollback() 
   print("Ошибка при начальном заполнении БД : "+ "\n"+ str(error),2)
   return(False)  
 finally:
    if curDb:
        curDb.close()
    if connDb:
        connDb.close()
        
    if curMySql:
        curMySql.close()
    if connMySql:
        connMySql.close()    


print(CopyMainDbToMySql())
print(horoscopedbMySQL.CreateTablesMySqlOnlyTrigg())
print(CopyPayDbToMySql())


   
