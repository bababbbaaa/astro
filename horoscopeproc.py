import horoscopedb
from horoscoperr import HandleMess
import random
from datetime import date, datetime, timedelta



# дней, дня 
def strRusDays(inpDays):
   strD = str(abs(inpDays))
   S = strD[-1]
   if (S == "1")  and (inpDays!= 11):
      return "день"
   elif (S in {"2","3","4"})and (inpDays not in{12,13,15}) :
      return "дня"
   else:
      return "дней" 
   
    

 
#  количество строк в таблице

def GetTbLen(conn,inpTbName):
 try:
   cur = conn.cursor()
   cur.execute("SELECT COUNT(1) FROM "+inpTbName);                       
   records = cur.fetchall()
   if len(records) == 0:
     return(0)
   else:
     return(records[0][0]) 
 except Exception as error:
    HandleMess("Ошибка подсчета кол-ва строк в таблице: "+str(inpTbName)+"\n"+ str(error),4,True)
    return(0)
 finally:    
    if cur:
       cur.close()



## получить заголовок из таблицы по текущей дате

def GetCommonDayHeaderOnDate(conn,inpDate,TomorrTable=0):    
 try:

     listMonth =("января","февраля","марта",
                "апреля","мая","июня",
                "июля","августа","сентября",
                "октября","ноября","декабря")
    

     CurrDate = inpDate   # date.today()
     inpDateStr = CurrDate.strftime("%Y-%m-%d")
     cur = conn.cursor()
     if TomorrTable==0:
       cur.execute("SELECT Header FROM MessHeaders WHERE MessDate = %s",(inpDateStr,))
     else:
       cur.execute("SELECT Header FROM MessHeaders_1 WHERE MessDate = %s",(inpDateStr,))
       
     records = cur.fetchall()
       
     if len(records) == 0:  
         HandleMess("Не найдено ни одного заголовка для даты "+inpDateStr,3,True)
         CurrHeaderTXT = "ЗАГОЛОВОК"
     else:
         CurrHeaderTXT = records[0][0]
     
     CurrDateTXT = CurrDate.strftime("%d")+" "+listMonth[CurrDate.month-1] 

     return CurrDateTXT+".\n\nОбщий гороскоп дня.</b>\n\n"+CurrHeaderTXT
 except Exception as error:
     HandleMess("Ошибка процедуры формирования общего заголовка: \n"+ str(error),4,True)
     return(None)
 finally:  
    if cur:
       cur.close()

# сформировать все сообщения для активных  в этот час,
# либо для пользователя по ТЛГ ID 
def GenHourMessAll(inpDesTimeID,inpTelegramID=None):

 # подключиться к базе

 try:
    cur = False
    conn = horoscopedb.ConnectDb()
    
    if conn is None:      
       return(None)
    
    cur = conn.cursor()
    # размер таблиц с текстами

    
    bodyLen = GetTbLen(conn,"MessBodies")
    
    if bodyLen == 0: 
       HandleMess("Пустая таблица  текстов ",4,True)
       return(None)
    
    midday = datetime.strptime('12:00:00', '%H:%M:%S').time()
    
    # найти заголовок на сегодня, и на завтра
    TodayHeaderTXT = GetCommonDayHeaderOnDate(conn,date.today())
    TomorHeaderTXT = GetCommonDayHeaderOnDate(conn,date.today()+timedelta(days=1),1) # текст на завтра взять из завтрашней таблицы
    
    if (TodayHeaderTXT == None or TomorHeaderTXT == None):
       return(None) 

    
     
    currNow = date.today()
    
    txtQuery = """SELECT Users.ID as UsrID,
                         Name,
                         TelegramID,
                         Gender_ID,
                         UM.MessID as MessID,    /*идентификатор в таблице UserMess потом удалить эти сообщения*/
                         UserMess.Col_1,
                         coalesce(Mb1.Col_1,'') as txtCol_1,
                         UserMess.Col_2,
                         coalesce(Mb2.Col_2,'') as txtCol_2,
                         UserMess.Col_3,
                         coalesce(Mb3.Col_3,'') as txtCol_3,
                         UserMess.Col_4,
                         coalesce(Mb4.Col_4,'') as txtCol_4,
                         ActiveUntil as ActiveUntil,
                         Users.StdShutoff  as StdShutoff,
                         
                         UserSentMess.ID as SentMessID,      /*отправленные сегодня сообщения*/
                         UserSentMess.Col_1,
                         coalesce(SMb1.Col_1,'') as StxtCol_1,  
                         UserSentMess.Col_2,
                         coalesce(SMb2.Col_2,'') as StxtCol_2,
                         UserSentMess.Col_3,
                         coalesce(SMb3.Col_3,'') as StxtCol_3,
                         UserSentMess.Col_4,
                         coalesce(SMb4.Col_4,'') as StxtCol_4,
                         Users.RegDateFin        as RegDateFin,   /* дата регистрации */
                         Users.DesTime_ID        as DesTime_ID,    /*когда высылать гороскоп утро(0)/вечер(1)*/

                         coalesce(Mb1T.Col_1,'') as txtCol_1T,  /*26*/  /*завтрашние сообщения*/                     
                         coalesce(Mb2T.Col_2,'') as txtCol_2T,  /*27*/                        
                         coalesce(Mb3T.Col_3,'') as txtCol_3T,  /*28*/                       
                         coalesce(Mb4T.Col_4,'') as txtCol_4T,  /*29*/ 

                         coalesce(SMb1T.Col_1,'') as StxtCol_1T, /*30*/  /*завтрашние из отправленных*/                         
                         coalesce(SMb2T.Col_2,'') as StxtCol_2T, /*31*/                        
                         coalesce(SMb3T.Col_3,'') as StxtCol_3T, /*32*/                        
                         coalesce(SMb4T.Col_4,'') as StxtCol_4T,  /*33*/
                         Users.SubscrType_ID as SubscrType_ID,     /*34*/   /*тип подписки 1-пробная,3 - оплачена, 5 - не активна*/
                         CASE WHEN Users.SubscrType_ID = 3 THEN 0 
	                 ELSE      Users.SubscrType_ID     END As SubscrTypeForORDER  /* необходимо для сортировки сначла опл(3), потом проб(1),не акт (5)*/
                         
                                                                    
                        
                 FROM Users
                 """
    
    txtQueryMiddleAll=""" LEFT JOIN  
                    ( SELECT MIN(ID) as MessID, 
                             User_ID as User_ID           
                      FROM UserMess
                      GROUP BY User_ID 
                     ) As UM ON Users.ID = UM.User_Id

                   LEFT JOIN                               /*сегодняшние сообщения*/
                     ( SELECT MIN(ID) as MessID, 
                             User_ID as User_ID           
                      FROM UserSentMess
                      WHERE DateSend = CURRENT_DATE() 
                      GROUP BY User_ID 
                     ) As USM ON Users.ID = USM.User_Id
                     """

   
    txtQueryMiddleOne=""" LEFT JOIN  
                     ( SELECT MIN(ID) as MessID, 
                             User_ID as User_ID           
                      FROM UserMess WHERE User_ID = %s                      
                     ) As UM ON Users.ID = UM.User_Id 

                    LEFT JOIN                               /*сегодняшние сообщения*/
                     
                     ( SELECT MIN(ID) as MessID, 
                             User_ID as User_ID           
                      FROM UserSentMess
                      WHERE  DateSend = CURRENT_DATE() AND User_ID = %s 
                      
                     ) As USM ON Users.ID = USM.User_Id
                     """ 
                         
               
    txtQueryEnd=     """ LEFT JOIN  UserMess ON  UserMess.ID = UM.MessID
                 LEFT JOIN  UserSentMess ON  UserSentMess.ID = USM.MessID
                 
                 LEFT JOIN MessBodies as Mb1 
                 ON   Mb1.ID = UserMess.Col_1 

                 LEFT JOIN MessBodies as Mb2
                 ON Mb2.ID = UserMess.Col_2 

                 LEFT JOIN MessBodies as Mb3 
                 ON Mb3.ID = UserMess.Col_3 

                 LEFT JOIN MessBodies as Mb4 
                 ON Mb4.ID = UserMess.Col_4

                 LEFT JOIN MessBodies as SMb1 
                 ON   SMb1.ID = UserSentMess.Col_1 

                 LEFT JOIN MessBodies as SMb2
                 ON SMb2.ID = UserSentMess.Col_2 

                 LEFT JOIN MessBodies as SMb3 
                 ON SMb3.ID = UserSentMess.Col_3 

                 LEFT JOIN MessBodies as SMb4 
                 ON SMb4.ID = UserSentMess.Col_4

                 /*второй комплект для завтрашних г*/

                 LEFT JOIN MessBodies_1 as Mb1T 
                 ON   Mb1T.ID = UserMess.Col_1 

                 LEFT JOIN MessBodies_1 as Mb2T
                 ON Mb2T.ID = UserMess.Col_2 

                 LEFT JOIN MessBodies_1 as Mb3T 
                 ON Mb3T.ID = UserMess.Col_3 

                 LEFT JOIN MessBodies_1 as Mb4T 
                 ON Mb4T.ID = UserMess.Col_4

                 LEFT JOIN MessBodies_1 as SMb1T 
                 ON   SMb1T.ID = UserSentMess.Col_1 

                 LEFT JOIN MessBodies_1 as SMb2T
                 ON SMb2T.ID = UserSentMess.Col_2 

                 LEFT JOIN MessBodies_1 as SMb3T 
                 ON SMb3T.ID = UserSentMess.Col_3 

                 LEFT JOIN MessBodies_1 as SMb4T 
                 ON SMb4T.ID = UserSentMess.Col_4  """

    
    if (inpTelegramID != None):

       
       cur.execute("SELECT ID FROM  Users WHERE TelegramID =%s ",(inpTelegramID,))
       records = cur.fetchall()
       if len(records) == 0:  
         HandleMess("Не найдено ни одной записи ключевыми полями, ТЛГ ID: "+str(inpTelegramID)+" и не сегодняшней датой отправки ",3,True)
         return(None)       
       CurrUsrID = records[0][0]       
       cur.execute(txtQuery + txtQueryMiddleOne+txtQueryEnd+" WHERE RegDateFin IS NOT NULL AND TelegramID =%s  ",(CurrUsrID,CurrUsrID,inpTelegramID,))         
       records = cur.fetchall()
       
       if len(records) == 0:  
         HandleMess("Не найдено ни одной записи ключевыми полями, ТЛГ ID: "+str(inpTelegramID)+" и не сегодняшней датой отправки ",3,True)
         return(None)       

    else:
       
       if inpDesTimeID == None:
         HandleMess("Не указано время утро(0)/вечер(1)",3,True)
         return(None)
        
       # выбрать всех активных для этого часа
       cur.execute(txtQuery + txtQueryMiddleAll+txtQueryEnd+ """ WHERE (IsActiveBot = 1 AND
                                       /*  IsActiveSub = 1 AND*/
                                       /*   ActiveUntil > ? AND*/
                                       RegDateFin IS NOT NULL AND 
                                          DesTime_ID = %s  AND
                                     /* TelegramID = 5560719600  AND*/
                                         
                                        (Users.DateSend<>CURRENT_DATE()) )
                               ORDER BY SubscrTypeForORDER """,(inpDesTimeID,))#(datetime.strftime(datetime.now(), "%Y-%m-%d"),inpDesTimeID,))

       records = cur.fetchall() 

    resList = list()  # список всех сообщений пользователю
    usrList = list()  # писок пользователей кому проставить дату отправки в Users
    usrMessList = list()  # список сообщений для удаления из UserMess
    usrStopList = list()  # список пользователей , которым отключить подписку
    newTodayList = list() # список сообщений, которые добавить в сегодня отправленные
    for row in records:
      
      UserID = row[0]
      CurrName = row[1]
      CurrTelegramID = row[2] 
      GenderID = row[3]
      MessID = row[4] # id сообщения кооторое сработало, его удалить
      col_1  = row[5]
      Txt_1  = row[6]
      col_2 = row[7]
      Txt_2 = row[8]
      col_3 = row[9]
      Txt_3 = row[10]
      col_4 = row[11]
      Txt_4 = row[12]
      ActiveUntil = row[13]
      StdShutoff  = row[14]
      
      SentMessID  = row[15] #  сначала проверяем в отправленных сегодня , потом уже берем из списка
      Scol_1      = row[16]
      Stxt_1      = row[17]
      Scol_2      = row[18]
      Stxt_2      = row[19] 
      Scol_3      = row[20]
      Stxt_3      = row[21]
      Scol_4      = row[22]
      Stxt_4      = row[23]
      DesTimeID   = row[25]   # время получения горо
      SubscrTypeID = row[34]  # если SubscrTypeID = 5  подписка не активна, отправлять только заголовок дня
      
      
      # взять из завтрашней таблицы
      if DesTimeID == 1:
         Txt_1  = row[26]
         Txt_2  = row[27]
         Txt_3  = row[28]
         Txt_4  = row[29]
         
         Stxt_1 = row[30]
         Stxt_2 = row[31]
         Stxt_3 = row[32]
         Stxt_4 = row[33] 
      
      RegDateFin  = str(row[24])   # дата и время регистрации пользователя
      
      RegDateFin_obj = datetime.strptime(RegDateFin, '%Y-%m-%d %H:%M:%S')
      
      RegDate     = RegDateFin_obj.date()
      RegTime     = RegDateFin_obj.time()

      DesTimeID   = row[25]   # время получения горо

      if DesTimeID==0:    # утром сегодняшний
         DayHeaderTXT = TodayHeaderTXT
         whatDay  = "сегодня"
      else:                 # вечером завтрашний
         DayHeaderTXT = TomorHeaderTXT
         whatDay  = "завтра"

      if ActiveUntil  == None:
         HandleMess("У пользователя не указана дата окончания подписки, ТЛГ ID: "+str(inpTelegramID),4,True)    
         continue
      
      if SentMessID != None:   # сегодня уже пользователю отправляли, взять из отправленных
         Txt_1 =  Stxt_1
         Txt_2 =  Stxt_2
         Txt_3 =  Stxt_3  
         Txt_4 =  Stxt_4
         todaySentMess = True
      else:                    # сегодня еще не отправляли
         todaySentMess = False
         if MessID == None: 
            HandleMess("У пользователя ТЛГ ID: "+str(CurrTelegramID)+", Имя: "+str(CurrName)+" закончились сообщения!",4,True)
            continue

         usrMessList.append((MessID,))#  добавляем в удаляемые сообщения
         newTodayList.append((UserID,currNow,col_1,col_2,col_3,col_4)) #  добавляем в сегодняшние сообщения
        
      
      

      ServMess =""
      Stat     = 0
      leftDays  = durDays(currNow,str(ActiveUntil)) # проверить оставшуюся подписку
      if leftDays == None:
         HandleMess("Ошибка поиска разницы дат, ТЛГ ID: "+str(inpTelegramID),4,True)    
         continue
      if StdShutoff == 1: # собщения выдаем только по флажку
        Stat = 2 
        if leftDays <=0:
           
          usrStopList.append((UserID,)) # отключить от рассылки
          
          ServMess ="Ваша подписка окончена !"
          Stat = 3
        elif leftDays <=3:         
          ServMess =" До окончания подписки "+("остался" if leftDays == 1  else "осталось")+" "+str(leftDays)+" "+strRusDays(leftDays)     
          Stat = 2 

      if (RegDate == currNow) and (DesTimeID == 1) and (RegTime < midday  ): # зарегился сегодня  до обеда и время отправки вечер, то сегодня в рассылку  включать
         pass
      else:   
        if Stat != 3:
           usrList.append((currNow,UserID,))  # проставить дату отправки пользователю (т.е.  блокировать сегодняшнюю  рассылку)


      
      CurrDo = "Дорогой " if GenderID == 1 else "Дорогая "
      
           
      CurrResHeaderTXT = "<b>"+CurrDo+CurrName+", "+whatDay+" "+DayHeaderTXT 
      
      if SubscrTypeID == 5: #по статусом 5 не формировать перс гор - только шапку
         CurrMessTXT = ""
         CurrResHeaderTXT = CurrResHeaderTXT+"\n\n\n <b>Прекрасного дня!</b> 🌸🌸🌸"     
         
      else:   
         CurrMessTXT = formMess(Txt_1,Txt_2,Txt_3,Txt_4)
      
      resList.append((CurrTelegramID,CurrName,CurrResHeaderTXT,CurrMessTXT,ServMess,Stat,todaySentMess,DesTimeID,)) 
      
    if cur:  
        cur.close()
    delAndUpdUsrInfo(conn,currNow,usrList,usrMessList,usrStopList,newTodayList)  # сохранить дату отправки в Users и удалить отправленные из UserMess, отключить от раасылки
    
    return(resList)
    
 except Exception as error:
    HandleMess("Ошибка процедуры формирования текста г. для часа: "+str(inpDesTimeID)+"\n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()   



#  возвращает разницу в днях между тек датой и вх датой
#  сколько осталось до вхдаты 
def durDays(now,inpDateStr):
  try: 
  #  now  = date.today()
    inpDate = datetime.strptime(inpDateStr, "%Y-%m-%d").date()
    deltadays = (inpDate- now).days
    return(deltadays)
  except  Exception as error:
     HandleMess("Ошибка поиска разницы дат, дата: "+str(inpDateStr)+"\n"+ str(error),4,True)
     return(None)   
    
# сформировать тело сообщения из отдельных текстов БД
def formMess(Txt_1,Txt_2,Txt_3,Txt_4):
    
    resStr =  "<b>Твой персональный гороскоп.</b>\n\n🎯 🎯 🎯\n\n"+Txt_2      #"Возможности\n\n"+Txt_2
 
    resStr = resStr + "\n\n❤ ❤ ❤\n\n"+Txt_1 #"\n\nОтношения\n\n"+Txt_1
    
    resStr = resStr + "\n\n🍔 🥑 😊\n\n"+Txt_3      #"\n\nЗдоровье\n\n"+Txt_3
    
    resStr = resStr +"\n\n💰 💰 💰\n\n"+Txt_4   #\n\nДеньги\n\n"+Txt_4
    
   
    
    resStr = resStr +  "\n\n\n <b>Прекрасного дня!</b> 🌸🌸🌸"
    
    return(resStr)


## пользователям в спике проставить дату отправки для предохранения от повторной
## удалить сработавшие сообщения по usrMessList из userMess

def delAndUpdUsrInfo(conn,currDate,usrList,usrMessList,usrStopList,newTodayList):
 try:

   
   cur = conn.cursor()
   cur.executemany("UPDATE Users SET DateSend = %s WHERE ID = %s ",usrList)
   
   cur.executemany("DELETE FROM UserMess WHERE ID = %s ",usrMessList)
    
##   cur.executemany("UPDATE Users SET IsActiveSub = 0  WHERE ID = ? ",usrStopList)   пока не отменяем подписку
      
   cur.executemany("INSERT INTO UserSentMess (User_ID,DateSend,Col_1,Col_2,Col_3,Col_4)  VALUES (%s,%s,%s,%s,%s,%s) ",newTodayList) # добавить все новые отправленные сообщения     

   
   cur.execute("DELETE FROM UserSentMess WHERE DateSend <> %s ",(currDate,)) #  удалить все несегодняшние сообщения
   
   
   conn.commit()
   
 except Exception as error:
    HandleMess("Ошибка обновления даты отправки или списка сообщений пользователя \n"+ str(error),4,True)    
 finally:    
    if cur:
       cur.close()




# получить статус подписки пользователей
def GetSubscrState(inpTelegramID=None):
 try:
    cur = False
    conn = horoscopedb.ConnectDb()
    if conn is None:      
       return(None)

    currNow = date.today()  
    cur = conn.cursor()

    txtQuery = """SELECT SubscrType_ID,
                          ActiveUntil,
                          SubscrTypes.Days,
                          IsActiveSub,
                          IsActiveBot,
                          TryPayRem,
                          TelegramID
                   FROM  Users
                   LEFT JOIN SubscrTypes
                   ON   SubscrTypes.ID = SubscrType_ID
                   WHERE  IsActiveBot =1 """


    if inpTelegramID  == None:
      cur.execute(txtQuery) 
    else:
      cur.execute(txtQuery+ " AND TelegramID = %s ",(inpTelegramID,))  
      
      
    records = cur.fetchall()   
    resList = list()  # список статусов
    for row in records:
   
      SubscrType  = row[0]
      ActiveUntil = row[1] 
      DaysSubscr  = row[2]
      IsActiveSub = row[3]
      IsActiveBot = row[4]
      TryPayRem   = row[5] # осталось  попыток списать средства
      TelegramID  = row[6]
      if DaysSubscr == None:
        HandleMess("У пользователя вообще нет подписки, ТЛГ ID: "+str(inpTelegramID),4,True)    
        return(None)
    
      if ActiveUntil  == None:
        HandleMess("У пользователя не указана дата окончания подписки, ТЛГ ID: "+str(inpTelegramID),4,True)    
        return(None)

      leftDays  = durDays(currNow,str(ActiveUntil))
      if leftDays == None:
        HandleMess("Ошибка поиска разницы дат, ТЛГ ID: "+str(inpTelegramID),4,True)    
        return(None)

      Stat = 0  
      if IsActiveSub != 0:
        
        if SubscrType == 1:         
          Mess = "Активирован пробный период на "
          Stat = 1
        else:
          Mess = "Активирована подписка на "
          Stat = 2
          
        if  leftDays<=3:
          Stat = 6   
          if SubscrType == 1:         
             Mess = "Заканчивается пробный период на "          
          else:
            Mess = "Заканчивается подписка на "
        
        Mess = Mess + str(DaysSubscr)+" дней. Дней до окончания: "+str(leftDays)+"."
      else:

        if TryPayRem<=0:
          Stat = 5
          Mess = "Не удалось продлить подписку"
        else:   
          if SubscrType == 1:
            Mess = "Закончился пробный период"
            Stat = 3
          else:   
            Mess = "Подписка неактивна"
            Stat = 4
            
      if inpTelegramID  == None and Stat<=2:
         continue
      else:   
        resList.append((TelegramID,SubscrType,ActiveUntil,DaysSubscr,leftDays,Mess,Stat,))
	 
    return(resList) 

 except Exception as error:
    HandleMess("Ошибка процедуры получения статуса подписки "+str(inpTelegramID)+"\n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()


# возвращает  гороскоп для временного пользователя, только на сегодня
def GenTmpUsrMess(inpTelegramID):
  # подключиться к базе

 try:
    cur = False
    conn = horoscopedb.ConnectDb()
    if conn is None:      
       return(None)
    cur = conn.cursor()
    DayHeaderTXT = GetCommonDayHeaderOnDate(conn,date.today())
    
    whatDay  = "сегодня"

    txtQuery = """SELECT MainTb.TelegramID,
                       MainTb.Name,
                       MainTb.Gender_ID,
                       MainTb.Birthday,
                       coalesce(MainTb.Col_1,SecTb.Col_1,''),
                       coalesce(MainTb.Col_2,SecTb.Col_2,''),
                       coalesce(MainTb.Col_3,SecTb.Col_3,''),
                       coalesce(MainTb.Col_4,SecTb.Col_4,''),
                       coalesce(Mb1.Col_1,'') as txtCol_1,
                       coalesce(Mb2.Col_2,'') as txtCol_2,
                       coalesce(Mb3.Col_3,'') as txtCol_3,
                       coalesce(Mb4.Col_4,'') as txtCol_4,
                       MainTb.ID
                       
               FROM UsersTmp as MainTb
               LEFT JOIN
               ( SELECT ID, 
                        Birthday,
                        Gender_ID,
                        Col_1,
                        Col_2,
                        Col_3,
                        Col_4                 
                 FROM UsersTmp
                 WHERE (Birthday IS NOT NULL)  and
                       (Gender_ID IS NOT NULL) and
                       (Col_1  IS NOT NULL) and
                       (Col_2  IS NOT NULL) and
                       (Col_3  IS NOT NULL) and
                       (Col_4  IS NOT NULL)                                   
                  ) as SecTb ON
               
               (SecTb.Birthday  = MainTb.Birthday) and
               (SecTb.Gender_ID = MainTb.Gender_ID) and
               (SecTb.ID <> MainTb.ID)

                 LEFT JOIN MessBodies as Mb1 
                 ON Mb1.ID = coalesce(MainTb.Col_1,SecTb.Col_1,'')

                 LEFT JOIN MessBodies as Mb2
                 ON Mb2.ID = coalesce(MainTb.Col_2,SecTb.Col_2,'')

                 LEFT JOIN MessBodies as Mb3 
                 ON Mb3.ID = coalesce(MainTb.Col_3,SecTb.Col_3,'')

                 LEFT JOIN MessBodies as Mb4 
                 ON Mb4.ID = coalesce(MainTb.Col_4,SecTb.Col_4,'')
               
               WHERE (MainTb.ID = (SELECT MAX(ID) FROM UsersTmp WHERE TelegramID = %s)) LIMIT 1 """


    
    cur.execute(txtQuery,(inpTelegramID,))  
    resList = list()  # список всех сообщений пользователю
    
    records = cur.fetchall()
    if len(records) != 1:
       return(resList)
   
    
    ServMess = None
    Stat  = None
    todaySentMess = None
    row = records[0]
    CurrTelegramID  = row[0]
    CurrName        = row[1] 
    GenderID        = row[2]
    Birthday        = row[3]
    UsersTmpID      = row[12]
    
    Txt_1           = row[8]
    Txt_2           = row[9]
    Txt_3           = row[10]
    Txt_4           = row[11]

    if(Txt_1 == "") or (Txt_2 == "") or (Txt_3 == "") or (Txt_4 == ""):    # еще не присвоены колонки
       
       lenMess = GetTbLen(conn,"MessBodies")
       
       Col_1 = random.randint(0, lenMess-1)  # получить новые значения 
       Col_2 = random.randint(0, lenMess-1)
       Col_3 = random.randint(0, lenMess-1)
       Col_4 = random.randint(0, lenMess-1) 
       cur.execute(""" SELECT Col_1 as Txt FROM MessBodies WHERE ID = %s
                        UNION ALL
                        SELECT Col_2 as Txt FROM MessBodies WHERE ID = %s
                        UNION ALL
                        SELECT Col_3 as Txt FROM MessBodies WHERE ID = %s
                        UNION ALL
                        SELECT Col_4 as Txt FROM MessBodies WHERE ID = %s """,(Col_1,Col_2,Col_3,Col_4,))       
       records = cur.fetchall()
       
       Txt_1           = records[0][0]
       Txt_2           = records[1][0]
       Txt_3           = records[2][0]
       Txt_4           = records[3][0]
       # сохранить новые значения в последнюю запись с указанным ТЛГ ID
       cur.execute(""" UPDATE  UsersTmp
                       SET Col_1 = %s, Col_2 = %s, Col_3 = %s,Col_4 = %s
                       WHERE ID = %s """,(Col_1,Col_2,Col_3,Col_4,UsersTmpID,))       

       conn.commit() 
        
          
    CurrDo = "Дорогой " if GenderID == 1 else "Дорогая " 
    CurrResHeaderTXT = "<b>"+CurrDo+CurrName+", "+whatDay+" "+DayHeaderTXT      
    CurrMessTXT = formMess(Txt_1,Txt_2,Txt_3,Txt_4)
    resList.append((CurrTelegramID,CurrName,CurrResHeaderTXT,CurrMessTXT,GenderID,Birthday,)) 

    return(resList)
   
 except Exception as error:
    HandleMess("Ошибка процедуры формирования для врем польз ТЛГ ID: "+str(inpTelegramID)+"\n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()   


# записать данные в таблицу
def AddToAstroSchool(inpCategory,inpDateSend,inpTimeSend,inpManagerID,inpMessageID):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,))
   cur = conn.cursor()

   cur.execute("""SELECT 1 FROM AstroSchool              
                  WHERE (DateSend = ? AND TimeSend = ? AND ManagerID  = ? AND MessageID = ? )                     
               """,(inpDateSend,inpTimeSend,inpManagerID,inpMessageID,))
   records = cur.fetchall()
   if len(records) != 0:
      return((False,"Запись с подобными ключевыми полями уже существует",))
    

   cur.execute("INSERT INTO AstroSchool (Category,DateSend, TimeSend,ManagerID,MessageID)  VALUES (?,?,?,?,?) ",
               (inpCategory,inpDateSend,inpTimeSend,inpManagerID,inpMessageID,))

   conn.commit()
   return((True,))
 except Exception as error:
    HandleMess("Ошибка процедуры ""AddToAstroSchoo"" \n"+ str(error),4,True)
    return((False,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()

       
# удалить данные из таблицы

def DelFromAstroSchool(inpDateSend, inpCategory = None):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,))
   cur = conn.cursor()

   if inpCategory == None:
     cur.execute("DELETE FROM AstroSchool WHERE  = ? ",(inpDateSend,)) 
   else:      
     cur.execute("DELETE FROM AstroSchool WHERE (DateSend = ? AND Category = ?)",(inpDateSend,inpCategory,))

   conn.commit()
   return((True,))
 except Exception as error:
    HandleMess("Ошибка процедуры ""DelFromAstroSchool"" \n"+ str(error),4,True)
    return((False,)) 
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()


# удалить данные из таблицы по MessageID

def DelFromAstroSchoolOnMessID(inpMessageID):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,))
   cur = conn.cursor()
  
   cur.execute("DELETE FROM AstroSchool WHERE MessageID = ? ",(inpMessageID,))   

   conn.commit()
   return((True,))
 except Exception as error:
    HandleMess("Ошибка процедуры ""DelFromAstroSchoolOnMessID"" \n"+ str(error),4,True)
    return((False,)) 
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()

       
       
# поменять данные в таблице AstroSchool

def ChAstroSchool(inpMessageID,inpFieldName, inpValue):

 try:
  cur = False
  conn = horoscopedb.ConnectDb()
  if conn is None:      
        return((False,))
  cur = conn.cursor()

             
  
  UsrFields = ['Category',
               'DateSend',
               'TimeSend',
               'ManagerID']

  for i in range(len(UsrFields)):
     UsrFields[i] = UsrFields[i].capitalize() # привести имена полей к единообразному виду 

  inpFieldName = inpFieldName.capitalize()

  
  if not inpFieldName in UsrFields:
     HandleMess("Ошибка имени поля для изменения AstroSchool : "+inpFieldName,3,True)
     return(False,"Ошибка имени поля для изменения AstroSchool: "+inpFieldName)

  cur.execute("SELECT 1 FROM AstroSchool WHERE MessageID = ? " ,(inpMessageID,))
  records = cur.fetchall()
  
  if len(records) == 0:  
    HandleMess("В AstroSchool  не найден MessageID: "+ str(inpMessageID) ,3,True)
    return(False,"В AstroSchool  не найден MessageID: "+str(inpMessageID),)

  cur.execute("UPDATE AstroSchool SET "+inpFieldName+" = ? WHERE MessageID = ?  " ,(inpValue,inpMessageID,))

  conn.commit()
  return(True,)
 except Exception as error:
    HandleMess("Ошибка прцедуры изменения AstroSchool, MessageID: "+str(inpMessageID)+"\n"+str(error),3,True)
    return(False,"Ошибка прцедуры изменения AstroSchool, MessageID: "+str(inpMessageID)+", поле :"+inpFieldName,)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close() 

       

# получить данные из таблицы
def GetFromAstroSchool(inpDateSend, inpCategory = None):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return(None)
   cur = conn.cursor()

   if inpCategory == None:
     cur.execute("SELECT Category,DateSend, TimeSend,ManagerID,MessageID FROM AstroSchool WHERE DateSend = ? ",(inpDateSend,)) 
   else:      
     cur.execute("SELECT Category,DateSend, TimeSend,ManagerID,MessageID FROM AstroSchool WHERE (DateSend = ? AND Category = ?)",(inpDateSend,inpCategory,))

   records = cur.fetchall()
   return(records)
 except Exception as error:
    HandleMess("Ошибка процедуры ""GetFromAstroSchool"" \n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()   

       
# получить список всех тлг ID получающих сообщения в указанное время
def GetListUsersOnDesTime(inpDesTimeID):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return(None)
   cur = conn.cursor()
   cur.execute("SELECT TelegramID FROM Users  WHERE DesTime_ID = %s AND ActiveUntil > %s",(inpDesTimeID,datetime.strftime(datetime.now(), "%Y-%m-%d")))
   records = cur.fetchall() 
   return(records)
   
 except Exception as error:
    HandleMess("Ошибка получения списка ТЛГ ID получающих г. во время "+str(inpDesTimeID)+" \n"+ str(error),4,True)    
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()   

##  выбрать данные из любой  таблицы по фильтрам
##   фильтр - это кортеж с кортежами , каждый вложенные состоит из 3- х элементов
##  имя фильтруемого поля, условие (как оно пишетсы в бд), значение условия
##  пример SelectDeleteFromTable("AstroSchool",(("Name","=","Вася"), ("ID",">",3),)  )       - добавить
##  пример SelectDeleteFromTable("AstroSchool",(("Name","=","Вася"), ("ID",">",3),),True  ) - Удалить
##         SelectDeleteFromTable("AstroSchool",(('ID','>=',10),),True )
       
## все условия объединяются оператором AND
##  допускается предача пустого кортежа условия
##  IsDel = True - Удаляет данные по указанному признаку
       
def SelectDeleteFromTable(inpTbName,inpFilter, IsDel=False):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return(None)
   cur = conn.cursor()
   if IsDel:
     Qtext = "DELETE FROM "+inpTbName 
   else:   
     Qtext = "SELECT * FROM "+inpTbName
   
   QVal = list()   
   WhereText =" "  
   for onecond in inpFilter:
      WhereText = WhereText +onecond[0]+ onecond[1]+ "%s AND "
      QVal.append(onecond[2]) 

   WhereText = WhereText.rstrip(' AND ')  # удалить последнюю запятую
   
   if len(inpFilter)!= 0:
      Qtext = Qtext+" WHERE "
      
   Qtext = Qtext+WhereText

   cur.execute(Qtext,tuple(QVal))
   if IsDel:
      conn.commit()
      return(True)
   else:
      records = cur.fetchall() 
      return(records)
   
 except Exception as error:
    HandleMess("Ошибка унив. запроса к таблице "+inpTbName+ "\n"+ str(error),4,True)    
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()   



# записать данные в таблицу,
#  передаем имя таблицы и словарь  с именами полей и значениями
#  добавляется одна запись
#  например
#  InsertIntoTable(inpTbName="Sources",inpValues={"Name":"publdasdasic_name","Token":"tokdffdsfsden"})
#  Возвращает кортеж (True, ID  новой записи) или (False,)  при неудаче
def InsertIntoTable(inpTbName,inpValues):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return((False,))
   cur = conn.cursor()

   Qtext = "INSERT INTO "+inpTbName
   
   QVal = list()   
   NamesFields =" "
   QMark      = " "
   
   for key in inpValues:
      NamesFields = NamesFields +key+","
      QVal.append(inpValues[key]) 
      QMark = QMark+" %s,"
      
   NamesFields = NamesFields.rstrip(',')  # удалить последнюю запятую
   QMark = QMark.rstrip(',')
   if len(NamesFields)== 0:
      return((False,))
      
   Qtext = Qtext+"("+NamesFields+") VALUES ("+QMark+")" 

   
   cur.execute(Qtext,tuple(QVal))
   
   conn.commit()
   newID = cur.lastrowid
   return((True,newID,))
 except Exception as error:
    HandleMess("Ошибка добавления данных в таблицу "+inpTbName+" \n"+ str(error),4,True)
    return((False,))
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()

# сохранить id пользователей в файл по заданным параметрам
def SaveSegmentDb(inPar):
 try:
   if inPar == '1': # платная
      Qfilter = " WHERE IsActiveBot = 1 AND  SubscrType_ID = 3"      
   elif inPar == '2': # триал
      Qfilter = " WHERE IsActiveBot = 1 AND  SubscrType_ID = 1"      
   elif inPar == '3': # отписан
      Qfilter = " WHERE IsActiveBot = 0 AND  RegDateFin IS NOT NULL"      
   elif inPar == '4': # не завершена рег
      Qfilter = " WHERE RegDateFin IS NULL"      
   elif inPar == '5': # завершена платная подписка
      Qfilter = " WHERE IsActiveBot = 1 AND  SubscrType_ID = 5"       
   else:   
       inPar = '6'
       Qfilter = "" 

   path="static/Segment_"+inPar+".txt"
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return(False)
      
   f_out = open(path, 'w')   
   cur = conn.cursor()

   cur.execute("SELECT TelegramID FROM Users "+Qfilter)
   records = cur.fetchall()
   for row in records:
        f_out.write(str(row[0])+'\n')
        
   return(path)
 except Exception as error:
    return(error)
    
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()
    if f_out:
       f_out.close()


def CopyUsrMess():
 try:
   curNew = False
   curOld = False
   connNew = horoscopedb.ConnectDb()
   connOld = horoscopedb.ConnectOldDb()
   curNew = connNew.cursor()
   curOld = connOld.cursor()
   curNew.execute("""SELECT  Users.ID 
                 /*  Users.TelegramID,*/
		 /*  coalesce(UsrMess.CountMess,0) as UsrCountMess  */
                FROM Users 
                LEFT JOIN ( SELECT Count(1) CountMess,
                           User_ID
                           FROM UserMess
                           GROUP BY User_ID ) as UsrMess 
               ON UsrMess.User_ID = Users.ID
               WHERE (Users.IsActiveBot =0 and (Users.SubscrType_ID = 3 OR Users.SubscrType_ID = 1))and (coalesce(UsrMess.CountMess,0)=0) """)

   recordsNew = curNew.fetchall()
   resListIDNew = list()
   strList = ""
   for row in recordsNew:
     resListIDNew.append(row[0])
     strList = strList+str(row[0])+","

   strList = strList[:-1]  
   resTupIDNew = tuple(resListIDNew)
   print(strList)
   
   
##   print(type(resListIDNew))
##   print(resListIDNew)
   
   curOld.execute("SELECT User_ID,Col_1,Col_2,Col_3,Col_4 FROM UserMess WHERE User_ID IN ( "+strList+")")
   recordsOld = curOld.fetchall()

   curNew.executemany("INSERT INTO UserMess (User_ID,Col_1,Col_2,Col_3,Col_4)  VALUES (%s,%s,%s,%s,%s) ",recordsOld) 
   connNew.commit()
   
   
   print("Hello")
##   
   print(str(len(recordsOld)))
    
 except Exception as error:
    print(error)
    return(error)
    
 finally:    
    if curNew:
       curNew.close()
    if connNew:  
       connNew.close()
    if curOld:
       curOld.close()
    if connOld:  
       connOld.close()   
 
       

##
## Активна платная подписка: \n\
##                       отбираются записи таблицы Users у которых \n\
##                       ActiveBot = 1 и  SubscrType_ID=3\n\
##                       файл: ..static/Segment_1.txt  \n\n\
##                    2. Триал активен  \n \
##                       ActiveBot = 1 и  SubscrType_ID=1\n\
##                       файл: ..static/Segment_2.txt  \n\n\
##                    3. Пользователь отписан  \n \
##                       ActiveBot = 0 и RegDateFin<> NULL \n\
##                       файл: ..static/Segment_3.txt  \n\n\
##                    4. Не завершена регистрация \n \
##                       RegDateFin= NULL\n\
##                       файл: ..static/Segment_4.txt  \n\n\
##                    5. Завершена платная подписка \n \
##                       ActiveBot = 1 и  SubscrType_ID=5\n\
##                       файл: ..static/Segment_5.txt  \n\n\
##                    6. Все пользователи \n\
##                       Все записи таблицы Users\n\
##                       файл: ..static/Segment_6.txt"

   




##print(InsertIntoTable(inpTbName="Sources",inpValues={"Name":"publdasdasic_name","Token":"tokdffdsfsden"}))
##res = SelectDeleteFromTable("Users",(('ID','>',1000),("Gender_ID"," = ","2")))
##for row in res:
##   print(row)
##res =
       #933017341,193427287
##       314801740,245188029
##        5392589497


##old = datetime.now()

##print(GenHourMessAll(0,121212121237))
##print(GenHourMessAll(1,))#5560719600
#5392589497
##print("tot="+str(datetime.now()-old))
##for row in res:
##   print(row[2])
##print(GenHourMessAll(1))
##print(SaveSegmentDb('3'))

##CopyUsrMess()


##print(InsertIntoTable(inpTbName="Sources",inpValues={"Name":"publdasdasic_name","Token":"tokdffdsfsden"}))
