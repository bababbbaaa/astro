import openpyxl
import horoscopedb as horoscopedb
from horoscoperr import HandleMess
from datetime import date, datetime, timedelta
from horoscopeproc import GetTbLen



# возвращает список: сколько пользователей пришло с каких ресурсов
# возвращает список кортежей: (количество,ID из таблицы Source,Наименование, Токен)
def CountUserSource():
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return(None)
   cur = conn.cursor()
   cur.execute(""" SELECT COUNT(1) ,    /*0*/       /*колько пользователей с каждого ID */
                   Users.Source_ID,
                   Sources.Name,
                   Sources.Token
                   
                   FROM Users

                   LEFT JOIN Sources         
                   ON Sources.ID = Users.Source_ID
                   
                   GROUP BY  Users.Source_ID,Sources.Name, Sources.Token
                   
                   """)
   records = cur.fetchall()
   return(records)
   
 except Exception as error:
    HandleMess("Ошибка CountUserSource  \n"+ str(error),4,True)
    return(None) 
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()


# возвращает кортеж : (количество записей в таблице Users, количество окончательно зарегитрированных пользователей)
def CountUserData():
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return(None)

   UsrLen = GetTbLen(conn,"Users")
       
   cur = conn.cursor()
   cur.execute(""" SELECT COUNT(1)  
                   FROM Users
                   WHERE (RegDate IS NOT NULL) AND (RegDateFin IS NULL)               
                   
                   """)
   records = cur.fetchall()
   
   if len(records) == 0:
     return(UsrLen,0)
   else:
     return(UsrLen,records[0][0]) 
   
 except Exception as error:
    HandleMess("Ошибка CountUserData  \n"+ str(error),4,True)
    return(None) 
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()
    
    

##  выбрать данные  статистики с фильтроа 
##   фильтр - это кортеж с кортежами , каждый вложенный состоит из 3- х элементов
##  имя фильтруемого поля, условие (как оно пишетсы в бд), значение условия
##  пример GetUserStatistics((("Name","=","Вася"), ("TelegramID","=","123"),) )  

### список допустимых полей фильтра а также описание значений полей выбрки
##                     Source_ID          - ID Источника прихода пользователя 
##                     Source_Name        - Наименование Источника прихода пользователя
##                     TelegramID         - Телеграм  ID    
##                     IsActiveBot        - Активен ли бот 1/0 
##                     RegDate            - Дата регистрации, когда польователь впервые был добавлен в БД    
##                     User_Name         - имя пользователя,         
##                     Gender             - пол  M/F
##                     Birthplace         - месторождения  
##                     Birthday           - день рождения      
##                     BirthTime          - дата , содержащая в т.ч. и время рождения    
##                     DesTime            - желаемое время получения рассылки утро/вечер
##                     RegDateFin         - дата окончательной регистрации (когда пользователь указал DesTime)она же дата получения первого г.                
##                     DaysFromRegDate    - разница между тек датой и датой (RegDate)  начальной регистрации
##                     DaysFromRegDateFin - разница между тек датой и окончательной датой(RegDateFin) регистрации она же дата получения первого г.
##                     SubscrType_ID      - ID типа подписки, ID  в таблице SubscrTypes,
##                     SubscrType_Days    - на сколько дней оформлена тек. подписка
##                     TryPayRem          - осталось попыток оплатить подписку
##                     RecurrActive       - активен  ли рекуррентный платеж , поле будет сформировано позднее
##                     RemDaysSubscr      - осталось дней подписки
## 


def GetUserStatistics(inpFilter,AddHeader = False):
 try:
   cur = False
   conn = horoscopedb.ConnectDb()
   if conn is None:      
       return(None)
   cur = conn.cursor()
   

   Qtext = """ SELECT Users.Source_ID       as Source_ID  ,   
                     Sources.Name           as Source_Name ,  
                     Users.TelegramID       as TelegramID ,  
                     Users.IsActiveBot      as IsActiveBot,
                     Users.RegDate          as RegDate ,      
                     Users.Name             as User_Name,         
                     Genders.Name           as Gender,       
                     Users.Birthplace       as Birthplace,  
                     Users.Birthday         as Birthday,     
                     Users.BirthTime        as BirthTime,    
                     DesTimes.Name          as DesTime,       
                     Users.RegDateFin       as RegDateFin,                
                     CAST((JulianDay('now') - JulianDay(Users.RegDate))as Integer)       as DaysFromRegDate,
                     CAST((JulianDay('now') - JulianDay(Users.RegDateFin))as Integer)     as DaysFromRegDateFin,
                     Users.SubscrType_ID   as SubscrType_ID,
                     SubscrTypes.Days      as SubscrType_Days,
                     Users.TryPayRem       as TryPayRem,
                     0                     as RecurrActive,
                     CAST((JulianDay(Users.ActiveUntil) - JulianDay('now') ) as Integer) as RemDaysSubscr
                                                     
                  FROM Users
                  
                  LEFT JOIN Genders
                  ON Genders.ID = Users.Gender_ID
                  
                  LEFT JOIN Sources         
                  ON Sources.ID = Users.Source_ID

                  LEFT JOIN DesTimes
                  ON DesTimes.ID = Users.DesTime_ID
                  
                  LEFT JOIN SubscrTypes
                  ON SubscrTypes.ID =  Users.SubscrType_ID
                  """
   QVal = list()   
 
   WhereText =" "  
   for onecond in inpFilter:      
      WhereText = WhereText +onecond[0]+ onecond[1]+ "? AND "
      QVal.append(onecond[2]) 


   WhereText = WhereText.rstrip(" AND ")  # удалить последнюю запятую
   
   
   if len(inpFilter)!= 0:
      Qtext = Qtext+" WHERE "
      
   Qtext = Qtext+WhereText
   

   cur.execute(Qtext,tuple(QVal))
   
   records = cur.fetchall()
   

   currNowStr = datetime.now().strftime(("%d-%m-%Y %H:%M")) 
   if AddHeader:
      records.insert(0,('','',"Статистика на "+currNowStr))
      records.insert(1,('',))
      i = 2
      if len(inpFilter)== 0:
        records.insert(i,("Описание отбора: Все записи",))
        i = i +1
      else:
         records.insert(i,("Описание отбора:",))
         i = i +1 
         for currFilt in inpFilter:        
           records.insert(i,("","",currFilt[0],currFilt[1],currFilt[2]))
           i = i +1
      records.insert(i,("",))
      i = i +1
      records.insert(i,('Source_ID',
                   'Source_Name',
                   'TelegramID',
                   'IsActiveBot',
                   'RegDate',
                   'User_Name',
                   'Gender',
                   'Birthplace',
                   'Birthday',
                   'BirthTime',
                   'DesTime',
                   'RegDateFin',
                   'DaysFromRegDate',
                   'DaysFromRegDateFin',
                   'SubscrType_ID',
                   'SubscrType_Days',
                   'TryPayRem',
                   'RecurrActive',
                   'RemDaysSubscr'))
      
      records.insert(i+1,('ID Источника',
                   'Наим. Источника',
                   'ТЛГ  ID',
                   'Активен бот',
                   'Дата нач. рег.',
                   'Имя',
                   'Пол',
                   'Место рождения',
                   'День рождения',
                   'Время рождения',
                   'Время рассылки',
                   'Дата кон. рег.',
                   'Дней с даты нач. рег.',
                   'Дней с даты кон. рег.',
                   'ID типа подписки',
                   'Дней подписки',
                   'Осталось попыток оплаты',
                   'Активен рекурр. плат.',
                   'Осталось дней подписки'))
   
   return(records)
   
 except Exception as error:
    HandleMess("Ошибка получения статистики \n"+ str(error),4,True)
    return(None)
 finally:    
    if cur:
       cur.close()
    if conn:  
       conn.close()   

#  выгружает данные о статистике пользователю в Эксель файл
#  имя файла:UsrStat_03_07_2022_13_20.xlsx
#  WayToFile каталог куда сохраняется Excel файл
def GetUserStatisticsExcel(inpFilter,WayToFile = ""):
 try:

   currNowStr = datetime.now().strftime(("%d_%m_%Y_%H_%M"))
   fileName = WayToFile+"UsrStat_"+currNowStr+".xlsx"  
   wb = openpyxl.Workbook()
   exList = wb.active

   records =  GetUserStatistics(inpFilter,True)
   
   if records == None:
      return(False)     
   for row in records:   
     exList.append(row)

     
   wb.save(fileName)
   return(True)  
 except Exception as error:
   HandleMess("Ошибка получения статистики или записи в файл:"+fileName+" \n"+ str(error),4,True)
   return(False)    



##print(GetUserStatisticsExcel( (("Gender"," = ","M"),("Birthplace"," LIKE ","Москва")),'C:\PYTHON3104\\' ) )
