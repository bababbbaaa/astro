
import pandas as pd
import os
from datetime import timedelta
from utils import *
import telebot
from config import *
import config
from telebot import types
from databaseInteraction import *
from rich.console import Console
from flask import Flask, jsonify, request
import flask
from flask_cors import CORS
from horoscopedb import ConnectDb
import json
import functions
from horoscopeusr import ChUserInfo
# from controller import logger
from random import randint
from for_payments import *
# additional tools
import random
from utils.utils import *
DATE_FORMAT = '%d.%m.%Y'
console = Console
bot = telebot.TeleBot(TOKEN, parse_mode=None)

if sys.platform == 'win32':
    HOST = '127.0.0.1'
    PORT = 5000
else:
    HOST = '195.2.79.3'
    PORT = '443'

def wait_until_send(id, text, reply_markup=None, parse_mode=None, url=None):
    while True:

        try:
            result = bot.send_message(
                id, text, reply_markup=reply_markup, parse_mode=parse_mode)
            return result
        except Exception as err:
            console.log(err)
            if 'error_code' not in vars(err).keys():
                return 0
            if err.error_code == 429:
                continue
            elif err.error_code == 400:
                if url != None:
                    new_user_horo = horoscopeproc.GenTmpUsrMess(id)[0]
                    gender = new_user_horo[4]
                    name = new_user_horo[1]
                    horoscopeusr.RegTmpUser(id)
                    horoscopeusr.ChTmpUserInfo(
                        inpTelegramID=id, inpValue=name, inpFieldName="Name")
                    horoscopeusr.ChTmpUserInfo(
                        inpTelegramID=id, inpValue=gender, inpFieldName="Gender_ID")
                    text = new_user_horo[2]+"\n\n"+new_user_horo[3]
                    # wait_until_send(id,"Мы состоявляем гороскоп вашему другу, подождите некоторое время")
                    # send_friend_horo(id, text)
                    return 0
                    # keyboard=types.InlineKeyboardMarkup()
                    # but1=types.InlineKeyboardButton(text="Отправить другу",url=url)
                    # keyboard.add(but1)

                    # wait_until_send(id,text,reply_markup=None,parse_mode="html")
                    # time.sleep(0.1)
                    # return(0)
                else:
                    return err
            else:
                return err
                # return mes


class connect_err(Exception):
    print("Ошибка подключения к бд")


def change_active_until_date(start, date_end, days, base="subs"):
    if date_end.find("-") != -1:
        date_end = datetime.strptime(date_end, "%Y-%m-%d")
        date_end = datetime.strftime(date_end, DATE_FORMAT)
    if datetime.strptime(start, DATE_FORMAT) >= datetime.strptime(date_end, DATE_FORMAT):
        uctive_until = datetime.strptime(
            start, DATE_FORMAT)+timedelta(days=days)
    else:
        uctive_until = datetime.strptime(
            date_end, DATE_FORMAT)+timedelta(days=days)
    if base == "users":
        end = datetime.strftime(uctive_until, "%Y-%m-%d")
    else:
        end = datetime.strftime(uctive_until, DATE_FORMAT)
    return(end)


app = Flask(__name__)
CORS(app)


@app.route("/get_all_subsrcibes", methods=['GET', 'POST'])
def get_all_subs():
    conn = ConnectDb()
    path = "static/Output.xlsx"
    cur = conn.cursor()
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        try:
            cur.execute("SELECT * FROM Payments")
            df = cur.fetchall()
            cur.close()
            conn.close()
            df = pd.DataFrame(df)
            df.to_excel(writer, sheet_name='name')
            return path
        except Exception as err:
            return(err)


@app.route('/convert_tables', methods=['GET', 'POST'])
def converion():
    conn = ConnectDb()
    path = "static/Output.xlsx"
    cur = conn.cursor()
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        try:
            cur.execute("SELECT * FROM Users")
            df = cur.fetchall()
            cur.close()
            conn.close()
            df = pd.DataFrame(df)
            df.to_excel(writer, sheet_name='name')
            return path
        except Exception as err:
            return(err)


# def _get_table(offset,limit,date,gender,tg_id,source):
#     conn=ConnectDb()
#     cur = False
#     if conn is None:
#         raise connect_err("Несоответствующее значение")
#     cur = conn.cursor()
#     start_date=date["since"]
#     end_date=date["to"]
    # cur.execute("SELECT * FROM Users WHERE ID>=%s AND Id<=%s",(offset,offset+limit,));
   # records = cur.fetchall()
@app.route("/delete_file_with_path", methods=["GET", "POST"])
def delete_file():
    data = request.get_json()
    path = data["path"]
    if path.find(".xlsx") != -1:
        try:
            os.remove(path)
            # os.system("rm "+path)
        except:
            os.remove(path)
        return(json.dumps(path))
    else:
        return(json.dumps("NO"))


@app.route('/get_tables', methods=['GET', 'POST'])
def get_tables(data=None):
    # try:
    OBJECT_FOR_TRANSLATION = {

    }
    string_for_request = ""

    tuple_for_request = []
    try:
        if data == None:
            data = request.get_json()
    except Exception as err:
        print(err)
        data = {}
        pass
    if data == None:
        data = {}
    # print(data,"data")
    if "export" in data:
        if data["export"] == True:
            export = True
            del(data["export"])
            dictionary_for_introducing_settings = []
            for i in data:
                if i != "limit" and i != "offset":
                    dictionary_for_introducing_settings.append(
                        tuple([i, str(data[i])]))
        else:
            export = False
            del(data["export"])
    else:
        export = False
    limit = 1
    offset = 0
    if export == False:
        if "limit" in data:
            limit = data["limit"]
            del(data["limit"])
        if "offset" in data:
            offset = data["offset"]
            del(data["offset"])
    else:
        limit = get_amount_of_subs()
        offset = 0
        try:
            del(data["limit"])
        except:
            pass
        try:
            del(data["offset"])
        except:
            pass
    date_exists = False
    if "date" in data:
        date = data["date"]
        start_date = datetime.strptime(date["start"], "%d.%m.%Y")
        start_date = datetime.strftime(start_date, "%d.%m.%Y")

        end_date = datetime.strptime(date["end"], "%d.%m.%Y")
        end_date = datetime.strftime(end_date, "%d.%m.%Y")
        list_of_dates = pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        ).strftime('%d.%m.%Y').tolist()

        string_for_request += "Birthday IN (" + \
            "%s, "*(len(list_of_dates)-1)+"%s) AND "
        tuple_for_request = list_of_dates
        date_exists = True
        del(data["date"])

    if "registration_date" in data:
        start = datetime.strptime(
            data["registration_date"]["start"], "%d.%m.%Y")
        start = datetime.strftime(start, "%Y-%m-%d")+" 00:00:00"

        end = datetime.strptime(data["registration_date"]["end"], "%d.%m.%Y")
        end = datetime.strftime(end, "%Y-%m-%d")+" 00:00:00"
        string_for_request += "RegDate BETWEEN %s AND %s AND "
        tuple_for_request.append(start)
        tuple_for_request.append(end)
        date_exists = True
        del(data["registration_date"])
    if "Name" in data:
        if not data["Name"] == "":

            string_for_request += "Name LIKE %s AND "
            tuple_for_request.append("%"+data["Name"]+"%")
            del data["Name"]
    if "Birthplace" in data:

        if not data["Birthplace"] == "":

            string_for_request += "Birthplace LIKE %s AND "
            tuple_for_request.append("%"+data["Birthplace"]+"%")
            del data["Birthplace"]
    for i in data:
        if not data[i] == None:
            string_for_request += i+" = %s"
            string_for_request += " AND "
            tuple_for_request.append(data[i])
        else:
            string_for_request += i+" IS NULL"
            string_for_request += " AND "
    # print(string_for_request)
    if string_for_request != "":

        string_for_request = string_for_request[:-4]
    conn = ConnectDb()
    cur = conn.cursor()
    # print(tuple(tuple_for_request))
    if not string_for_request == "":
        cur.execute("SELECT * FROM Users WHERE " +
                    string_for_request, tuple(tuple_for_request))
    else:
        cur.execute("SELECT * FROM Users")
    records = cur.fetchall()
    if export == True:
        path = "static/"+str(random.randint(100000, 999999))+".xlsx"
        with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
            dictionary_for_introducing_settings.extend(records)
            records = tuple(dictionary_for_introducing_settings)
            df = pd.DataFrame(records)
            df.to_excel(writer, sheet_name='name')
            return json.dumps(path)

    res = []
    if offset > len(records):
        return(json.dumps([0, []]))
        offset = len(records)-1
    end_range = offset+limit
    length = len(records)
    if end_range > len(records):

        end_range = len(records)
    for row in records[length-offset-limit:length-offset]:#datetime.strftime(row[16],"%Y-%m-%d")
        row=list(row)
        if row[16]==None:
            row[16]=datetime.strptime("01.01.1970","%d.%m.%Y")
        if row[10]==None:
            row[10]=datetime.strptime("01.01.1970","%d.%m.%Y")
        if row[11]==None:
            row[11]=datetime.strptime("01.01.1970","%d.%m.%Y")
        if row[17]==None:
            row[17]=datetime.strptime("01.01.1970","%d.%m.%Y")
        res.append({"ID": row[0], "Name": row[1], "is_main": row[2], "BirthTime": str(row[4]),
                    "Birthday": row[5], "Gender_ID": row[3], 'Birthplace': row[6], "DesTime_ID": row[7],
                    "TimeZone": row[8], "TelegramID": row[9], "RegDate": datetime.strftime(row[10],"%Y-%m-%d %H:%M:%S"), "RegDateFin": datetime.strftime(row[11],"%Y-%m-%d %H:%M:%S"), "IsActiveBot": row[12],
                    "Balance": str(row[13]), "IsActiveSub": row[14], "SubscrType_ID": row[15],
                    "ActiveUntil": datetime.strftime(row[16],"%Y-%m-%d"), "DateSend": datetime.strftime(row[17],"%Y-%m-%d") , "Source_ID": row[22]
                    })
    res=res[::-1]
    conn.commit()
    cur.close()
    conn.close()
    return(json.dumps([length, res]))


@app.route("/get_payment", methods=["GET", "POST"])
def get_payment():
    try:
        # print(json.loads(request.get_data()))
        # print(request.get_json())
        price = request.form.get("OutSum")
        days = request.form.get("Shp_days")
        id = int(request.form.get('Shp_id'))
        InvId = request.form.get('InvId')
        prev_id = 0
        payment_type=request.form.get("IncCurrLabel")
        try:
            prev_id = request.form.get('Shp_prev')
        except:
            pass
        session=sessionmaker(engine)()
        date_end =session.query(User).filter_by(TelegramID=id).first()
        date_end=date_end.ActiveUntil
        date_end = datetime.strftime(date_end, "%Y-%m-%d")
        session.commit()
        end = change_active_until_date(
            start=Get_Data(), date_end=date_end, days=int(days))

        end_for_users = change_active_until_date(
            start=Get_Data(), date_end=date_end, days=int(days), base="users")

        if get_sub(id) != None:
            delete_sub(id)
            if prev_id != None and prev_id != 0:
                x = prev_id
            else:
                x = InvId

            add_sub(id=id, start=Get_Data(), end=end, pay_id=x, type=price)
            add_payment(sub_type=3, telegram_id=id, payment_id=str(
                count_payments()), active_until=end, days=30, payed=True, amount=69, link="REC")
            text = "Ваша подписка успешно продлена"
        else:
            add_sub(id=id, start=Get_Data(), end=end, pay_id=InvId, type=price)
            payment = add_payment(sub_type=3, telegram_id=str(
                id), active_until=end, days=days, payed=True, amount=price, link="None", payment_id=InvId)
            text = config.thanks_for_payment
        try:
            ChUserInfo(inpTelegramID=id, inpFieldName="ActiveUntil",
                       inpValue=end_for_users)
            ChUserInfo(inpTelegramID=id,
                       inpFieldName="IsActiveSub", inpValue=1)
            ChUserInfo(inpTelegramID=id,
                       inpFieldName="SubscrType_ID", inpValue=3)
            
            # signature = request.form.get['SignatureValue']
            pay = payments.get_payment(id)[0]
            #print(pay, "PAYYY")
            try:
                if prev_id!=0 and prev_id!=None:
                    # try:
                    change_unsuccesful_to_succesful(id)
                        
                    # except:
                    #     pass
                    # update_price_list_with_id(id,"new_payment",price)
                else:
                    if len(only_succesfull_payments.get_success_payments(telegram_id=id))==0:
                        add_success_payment(telegram_id=id,payment_id=InvId,days=int(days),price=price,type_of_payment="FIRST PAY")
                        # update_price_list_with_id(id,"new_customer",price)
                        
                    else:
                        add_success_payment(telegram_id=id,payment_id=InvId,days=int(days),price=price,type_of_payment="SELF PAID")
                        
                        # update_price_list_with_id(id,"new_payment",price)
            except Exception as err:
                try:
                    wait_until_send(952863788,err.args[0])
                except:
                    wait_until_send(952863788,"ошибка была")
            # payment=add_payment(sub_type=3,telegram_id=str(id),active_until=end,days=days,payed=True,amount=price,link="None",payment_id=InvId)
            # signature = robokassa.calculate_signature(cost, id, signature)
            # if robokassa.check_signature_result(id, cost, signature, merchant_password_2):
            try:
                wait_until_send(id, text, parse_mode="html")
            except:
                pass
            return f'OK{InvId}'
        except Exception as err:
            console.log(err)
            logger.error(err)
            add_payment(sub_type=3, telegram_id=str(id), active_until=end, days=days,
                        payed=True, amount=price, payment_id=count_payments(), link="error")
            print(err)
            # wait_until_send(id,"Что-то пошло не так, попробуйте оплатить снова или напишите в поддержку")
            return "bad sign"
            pass
    except Exception as err:
        # console.log(err)
        print(err)
        # logger.error(err)
        # wait_until_send(
        #     id, "Что-то пошло не так, попробуйте оплатить снова или напишите в поддержку")
        return "bad sign"
        pass
    return json.dumps(0)


@app.route("/get_information_about_subs")
def get_information_about_subs():
    conn = ConnectDb()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Source")
    sources = cur.fetchall()
    dictionary = {}
    list_to_return = []
    for i in sources:
        name = i[1]
        price = i[3]
        source_id = i[2]
        all_users = get_tables({"Source_ID": i[2]})
        who_started = all_users[0]
        first_tap = all_users[1][0]["RegDate"]
        users_who_didnt_ended = get_tables(
            {"Source_ID": i[2], "RegDateFin": None})[0]
        who_ended_reigistrations = who_started-users_who_didnt_ended
        users_who_unsubscribe = get_tables(
            {"Source_ID": i[2], "IsActiveBot": 0})[0]
        percent_of_start = who_ended_reigistrations/who_started*100
        price_for_one_user = who_started/price
        percent_of_unsub = users_who_unsubscribe/who_ended_reigistrations
        price_for_reg = who_ended_reigistrations/price
        dictionary = {"source_name": name, "source_id": source_id, "price": price, "who_started": who_started, "first_tap": first_tap, "users_who_didnt_ended": users_who_didnt_ended,
                      "who_ended_reigistrations": who_ended_reigistrations, "users_who_unsubscribe": users_who_unsubscribe,
                      "price_for_one_tap": price_for_one_user, "percent_of_start": percent_of_start, "percent_for_unsub": percent_of_unsub, "price_for_reg": price_for_reg
                      }
        list_to_return.append(dictionary)
        dictionary = {}
    return(json.dumps(list_to_return))


@app.route("/set_table", methods=["POST"])
def set_table():
    err_log = ""
    data = request.get_json()
    id: int = data["id"]
    params: dict = data["params"]
    for i in params:
        try:
            horoscopeusr.ChUserInfo(id, i, params[i])
        except Exception as err:
            err_log += err
            pass
    if err_log == "":
        return(json.dumps({"success": True}))
    else:
        return(err_log)


@app.route("/get_last", methods=["GET", "POST"])
def get_amount_of_subs():
    try:
        conn = ConnectDb()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users")
        rec = cur.fetchall()
        return(json.dumps(len(rec)))
    finally:
        conn.commit()
        cur.close()


@app.route("/get_payments", methods=["POST"])
def get_payments():
    data = request.get_json()
    limit: int = data["limit"]
    offset: int = data["offset"]
    payments = []
    if offset+limit > 100:
        params = {"limit": 100, "status": "succeeded"}
        # payments=Pay.list(params)
        for i in range((limit+offset)/100-1):
            try:
                payment = Pay.list(params)
                cursor = payment.cursor
                # for j in payment.items:
                #     if j.metadata["price"]
                params = {"limit": 100,
                          "status": "succeeded", "cursor": cursor}
                payments.extend()
            except:
                return(json.dumps([]))
        payment = Pay.list(params)
        cursor = payment.cursor
        params = {"limit": 100, "status": "succeeded", "cursor": cursor}
        payments.extend(payment[offset % 100:min(offset+limit, 100)])
        limit = limit-offset
        for i in range((limit-offset)//100):
            payment = Pay.list(params)
            cursor = payment.cursor
            params = {"limit": 100, "status": "succeeded", "cursor": cursor}
            payments.extend(payment[0:min(offset+limit, 100)])
            limit = limit-offset
    if limit+offset > 100:
        payments = Pay.list(limit=limit+offset, status="succeeded")
        for i in range((limit+offset)/100):
            payments.extend(Pay.list(limit=limit+offset, status="succeeded"))

@app.route('/get_success_payments', methods=['POST', 'GET'])
def get_sucess_payments_route():
    try:
        # print("dfdfdfdfdf")
        data = request.get_json()

        telegram_id = data.get('telegram_id')
        source_id = data.get('source_id')
        amount=data.get("amount")
        payment_type = data.get('payment_type')
        rec_available=data.get("rec_available")

        to_date=data.get("to_date")
        from_date=data.get("from_date")
        return_excel=data.get("return_excel")


        if to_date is not None:
            to_date=datetime.strptime(to_date,DATE_FORMAT)
        if from_date is not None:
            from_date=datetime.strptime(from_date,DATE_FORMAT)

        payments = get_success_web_payments(telegram_id, source_id, payment_type,rec_available,from_date,to_date,amount)
        converted = alchemy_list_convert(payments)
        converted=converted[::-1]

        if return_excel==True:
            path='static/payments.xlsx'
            with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
                try:

                    df=alchemy_tuple(payments)
                    df = pd.DataFrame(df)
                    df.to_excel(writer, sheet_name='name')
                    return path
                except Exception as err:
                    logger.error(err)
                    return(err)


        return jsonify(converted[:100])

    except Exception as err:
        print(err)

@app.route('/get_sources', methods=['POST', 'GET'])
def get_sources_route():
    data = request.get_json()

    try:
        title = data.get('title')
        code = data.get('code')
        type = data.get('type')
        return_excel=data.get("return_excel")
        
        sources = get_web_sources(title, code, type=type)
        converted = alchemy_list_convert(sources)



        if return_excel==True:
            path='static/sources.xlsx'
            with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
                try:

                    df=alchemy_tuple(sources,"sources")
                    df = pd.DataFrame(df)
                    df.to_excel(writer, sheet_name='name')
                    return path
                except Exception as err:
                    return(err)
        return jsonify(converted[::-1])
    except Exception as e:
        return str(e)



@app.route('/add_source', methods=['POST'])
def add_source_route():
    data = request.get_json()

    try:
        title: str = data['title']
        code: str = data['code']
        price: int = data['price']
        date: str = data['date']
        type: str = data['type']

        new_source = add_web_source(title, code, price, date, type)
        t = new_source.title

        converted = alchemy_to_dict(new_source)
        return jsonify(converted)
    except Exception as e:
        return str(e), 400



@app.route("/get_amount_of_payments", methods=['POST'])
def get_amount_of_payments():
    data = request.get_json()
    try:
        telegram_id = data.get('telegram_id')
        source_id = data.get('source_id')

        payment_type = data.get('payment_type')
        rec_available=data.get("rec_available")

        to_date=data.get("to_date")
        from_date=data.get("from_date")

        amount=data.get("amount")
        if to_date is not None:
            to_date=datetime.strptime(to_date,DATE_FORMAT)
        if from_date is not None:
            from_date=datetime.strptime(from_date,DATE_FORMAT)

        payments = get_success_web_payments(telegram_id, source_id, payment_type,rec_available,from_date,to_date,amount)

    
        return str(len(payments))
    except Exception as err:
        return str(err)


@app.route("/get_amount_of_sources", methods=['POST'])
def get_amount_of_sources():

    data = request.get_json()

    try:
        title = data.get('title')
        code = data.get('code')
        type = data.get('type')
        price = data.get('price')
        
        sources = get_web_sources(title, code, price, type)
        
        return str(len(sources))
    except Exception as err:
        return str(err)


@app.route('/delete_source', methods=['POST'])
def delete_source_route():
    data = request.get_json()

    title = data.get('title')
    code = data.get('code')

    try:
        delete_web_source(code, title)

        return 'SUCCESS'
    except:
        return "Something went wrong", 400


@app.route('/update_sources', methods=['POST'])
def update_source_route():
    data = request.get_json()

    try:
        sources = data['sources']

        for source in sources:
            code = source['code']
            title = source.get('title')
            price = source.get('price')
            type_ = source.get('type')

            update_web_source(code, title, price, type_)

        return 'SUCCESS', 200

    except Exception as e:
        return str(e), 400

app.run(host=HOST, port=PORT,debug=True)
#app.run(debug=True)
