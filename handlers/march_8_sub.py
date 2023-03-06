import sys
sys.path.append("../")
import config
from utils import *
from controller import *
import functions
import for_payments
mar_1={30:69,
        210:330,425:580}
mar_1_text='''
Доступно 3 варианта подписки: на 30, 180 и 365 дней.

✅ Стоимость подписки на месяц - 99, 69 рублей

✅ Стоимость подписки на пол года + месяц - 594, 330 ₽

✅ Стоимость подписки на год + 2 месяца - 1188. 580 ₽

Только 7 и 8 марта Вы получите дополнительно к полугодовой подписке 30 дней в подарок и к годовой подписке 60 дней в подарок.

Выбери подходящий тариф! Доступно 3 варианта продления подписки: на 30, 180 и 365 дней.'''
@dp.callback_query_handler(lambda call: call.data.split(";")[0] == "mar")
async def mar_subscribe(call):
    
    id=call.from_user.id
    sub_type=functions.GetUsers(id)[0]
    sub_type=int(sub_type["SubscrType_ID"])
    try:
        if id in delete_cache:
            for i in delete_cache[id]:
                bot.delete_message(id, i)
    except:
        pass
    if sub_type==1 or sub_type==2:
        keyboard=types.InlineKeyboardMarkup()
        but1=types.InlineKeyboardButton(text="Активировать подписку", callback_data="mar_2pt;"+str(sub_type))
        keyboard.row(but1)
        await wait_until_send(id, str(config.sub_type1_text(id)), reply_markup=keyboard)

    if sub_type == 100:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Активировать подписку", callback_data="mar_2pt;"+str(sub_type))
        keyboard.row(but1)
        await wait_until_send(id, config.sub_type3_text(id), reply_markup=keyboard)

    if sub_type == 3:
        keyboard = types.InlineKeyboardMarkup()
        # end_date = str(horoscopeproc.GetSubscrState(id)[0][2])
        but1 = types.InlineKeyboardButton(
            text="Продлить подписку", callback_data="mar_2pt;"+str(sub_type))
        but2 = types.InlineKeyboardButton(
            text="Отказаться от подписки", callback_data="mar_end")
        keyboard.row(but1, but2)
        await wait_until_send(id, config.sub_type3_text(id), reply_markup=keyboard)

    if sub_type == 4 or sub_type == 5:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Активировать подписку", callback_data="mar_2pt;"+str(sub_type))
        keyboard.row(but1)
        await wait_until_send(id, config.mare_type4_text(id), reply_markup=keyboard)



@dp.callback_query_handler(lambda call: call.data.split(";")[0] == "mar_sub")
async def mar_sub_options(call):
    try:

        id = call.from_user.id
        data = call.data
        data = data.split(";")
        is_new = data[1]
        days = int(data[2])
        delete_cache[id] = []

        if is_new == "n":
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(
                text="Да", callback_data="mar_ar"+";"+str(days))
            but2 = types.InlineKeyboardButton(
                text="Нет", callback_data="mar_net")
            but = types.InlineKeyboardButton(
                text="Назад", callback_data="mar_2pt")

            keyboard.row(but1, but2)
            keyboard.add(but)

            await wait_until_send(id, "Стоимость подписки  на "+str(days)+" дней составит"+str(mar_1[days]) + "рублей.\n\nПеред оплатой подписки, пожалуйста, ознакомьтесь со следующими документами:\n\nСоглашение на обработку персональных данных" +
                            config.url_for_all+"\n\nСоглашение на обработку платежей "+config.url_for_costs[days]+".\n\nВы подтверждаете что согласны с политикой обработки персональных данных и платежей?", parse_mode="html", reply_markup=keyboard)
    except Exception as err:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass
@dp.callback_query_handler(lambda call:call.data.find("mar_offer") != -1)
async def mar_offert(call):
    try:
        days=call.data.split(";")[1]
        id = call.from_user.id
        keyboard=types.InlineKeyboardMarkup()
        but=InlineKeyboardButton(text="Назад",callback_data="mar_ar;"+days)
        keyboard.add(but)
        await wait_until_send(id,config.offert,parse_mode="html",reply_markup=keyboard)
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass
@dp.callback_query_handler(lambda call: call.data.find("mar_inf") != -1)
async def mar_sub_info(call):
    try:
        id = call.from_user.id
        keyboard = types.InlineKeyboardMarkup()
        but = types.InlineKeyboardButton(
            text="Назад", callback_data="mar_2pt")
        keyboard.add(but)

        await wait_until_send(id, "В подписку входит общее описание дня с точки зрения расположения звезд и планет, звездная карта дня и ваш персональный гороскоп, который будет составляться и направляться вам каждый день в указанное вами время.", reply_markup=keyboard, parse_mode="html")
    except:

        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:

        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass

@dp.callback_query_handler(lambda call: call.data.find("mar_end") != -1)
async def mar_end_sub(call):
    try:
        id = call.from_user.id
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="да", callback_data="mar_fin_sub")
        but2 = types.InlineKeyboardButton(
            text="нет", callback_data="mar_del")
        keyboard.row(but1, but2)
        await wait_until_send(id, '''Обращаем внимание, что при отказе от подписки денежные средства, оставшиеся до окончания подписки, не возвращаются.

Вы точно хотите отказаться от подписки?''', reply_markup=keyboard)
    except Exception as err:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass
@dp.callback_query_handler(lambda call: call.data.find("mar_fin_sub")!=-1)
async def mar_fin_sub(call):
    try:
        id = call.from_user.id
        delete_sub(id=id)
        add_payment(sub_type=3,telegram_id=id,payment_id=str(count_payments()),active_until="01.10.1000",days=30,payed=True,amount=0,link="UNSUB")
        delete_period_sub(id)
        await wait_until_send(id,'Подписка отменена. Вы можете в любой момент активировать ее заново через раздел меню "подписка".')
    except:
        await wait_until_send(id,"Мы не обнаружили у вас подписку")
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass
@dp.callback_query_handler(lambda call: call.data.find("mar_del") != -1)
async def mar_delete(call):
    try:
        id = call.from_user.id
        await wait_until_send(
            id, "Спасибо, что продолжаете пользоваться Астроботом!")
    except:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass

@dp.callback_query_handler(lambda call: call.data.find("mar_end") != -1)
async def mar_fin_end(call):
    try:
        id = call.from_user.id
        await wait_until_send(
            id, "Ваша подписка отменена. Вы можете в любой момент активировать ее заново через  раздел меню 'подписка'.")
    except:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass
@dp.callback_query_handler(lambda call: call.data.find("mar_SUBSCR_ACT") != -1)#mar_SUBSCR_ACT
async def mar_active_sub(call):
    id=call.from_user.id
    # print(functions.GetUsers(id)[0]["SubscrType_ID"])
    sub_type=int(functions.GetUsers(id)[0]["SubscrType_ID"])
    try:
        if id in delete_cache:
            for i in delete_cache[id]:
                bot.delete_message(id, i)
    except:
        pass
    if sub_type==1 or sub_type==2:
        # print("here")
        keyboard=types.InlineKeyboardMarkup()
        but1=types.InlineKeyboardButton(text="Активировать подписку", callback_data="mar_2pt;"+str(sub_type))
        keyboard.row(but1)
        # print(config.sub_type1_text(id))
        await wait_until_send(id, str(config.sub_type1_text(id)), reply_markup=keyboard)

    if sub_type == 100:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Активировать подписку", callback_data="mar_2pt;"+str(sub_type))
        keyboard.row(but1)
        await wait_until_send(id, config.sub_type3_text(id), reply_markup=keyboard)

    if sub_type == 3:
        keyboard = types.InlineKeyboardMarkup()
        # end_date = str(horoscopeproc.GetSubscrState(id)[0][2])
        but1 = types.InlineKeyboardButton(
            text="Продлить подписку", callback_data="mar_2pt;"+str(sub_type))
        but2 = types.InlineKeyboardButton(
            text="Отказаться от подписки", callback_data="mar_end")
        keyboard.row(but1, but2)
        await wait_until_send(id, config.sub_type3_text(id), reply_markup=keyboard)

    if sub_type == 4 or sub_type == 5:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Активировать подписку", callback_data="mar_2pt;"+str(sub_type))
        keyboard.row(but1)
        await wait_until_send(id, config.sub_type4_text(id), reply_markup=keyboard)

        # await wait_until_send(id,"тут будет оплата")
@dp.callback_query_handler(lambda call: call.data.find("mar_ret") != -1)
async def mar_ret(call):
    try:
        id = call.from_user.id
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="30 дней", callback_data="mar_sub;n;30")
        but2 = types.InlineKeyboardButton(
            text="180 дней + месяц", callback_data="mar_sub;n;210")
        but3 = types.InlineKeyboardButton(
            text="365 дней + 2 месяца ", callback_data="mar_sub;n;425")
        but4 = types.InlineKeyboardButton(
            text="Что входит в подписку?", callback_data="mar_inf")
        but5 = types.InlineKeyboardButton(
            text="Назад", callback_data="mar_full_back")
        keyboard.row(but1, but2, but3)
        keyboard.add(but4)
        keyboard.add(but5)
        # if id in delete_cache:
        #     for i in delete_cache[id]:
        #         bot.delete_message(id, i)
            # delete_cache[id] = []
        await wait_until_send(id, 'Спасибо, что пользуетесь Астроботом.\n\nВ данный момент у вас действует пробный период подписки. Для вас доступны все функции бота!\n\nДо конца пробного периода осталось еще N дней.\n\nВы можете прямо сейчас активировать платную подписку.\n\nВ таком случае оставшееся время пробного периода суммируется с временем подписки.', reply_markup=keyboard)
    except Exception as err:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass

@dp.callback_query_handler(lambda call: call.data.find("mar_full_back") != -1)
async def mar_full_back(call):
    id = call.from_user.id
    await wait_until_send(
        id, "Для использования бота выберите кнопку в меню")
    try:
        await bot.delete_message(chat_id=id, message_id=call.message.message_id)
    except:
        pass

@dp.callback_query_handler(lambda call: call.data.find("mar_2pt") != -1)
async def mar_opt2(call):
    try:
        id=call.from_user.id
        sub_type=int(functions.GetUsers(id)[0]["SubscrType_ID"])
        # sub_type=functions.GetUsers(id)[0]["SubscrType_ID"]
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="30 дней", callback_data="mar_ar;30")
        but2 = types.InlineKeyboardButton(
            text="180 дней", callback_data="mar_ar;210")
        but3 = types.InlineKeyboardButton(
            text="365 дней", callback_data="mar_ar;425")
        but4 = types.InlineKeyboardButton(
            text="Что входит в подписку?", callback_data="mar_inf")
        but5 = types.InlineKeyboardButton(
            text="Назад", callback_data="mar_full_back")
        keyboard.row(but1, but2, but3)
        keyboard.add(but4)
        keyboard.add(but5)
        if sub_type==1:
            await wait_until_send(id,'Спасибо, что пользуетесь ботом "Твой гороскоп"\n\nВ данный момент у вас действует пробный период, подписки.'+ mar_1_text,reply_markup=keyboard,parse_mode="html")     
        elif sub_type==2 or sub_type==4 or sub_type==5 or sub_type==3:
            await wait_until_send(id,mar_1_text,reply_markup=keyboard,parse_mode="html")
        # elif sub_type==2:
        #     await wait_until_send(id,"Ваш пробный период использования бота 'Твой гороскоп' подошел к концу.\n\nЕсли Вы хотите дальше получать Ваш персональный ежедневный гороскоп, необходимо оплатить подписку.\n\nВ данный момент доступно 3 варианта подписки: на 30, 180 и 365 дней.\n\nСтоимость на 30 дней - 69 рублей\n\nСтоимость на 180 дней - (зачеркнутная цена) актуальная цена\n\nСтоимость на 365 дней - (зачеркнутная цена) актуальная цена.\n\nНа какой срок Вы бы хотели активировать подписку?",reply_markup=keyboard)
    # bot.send_message
    except:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass

@dp.callback_query_handler(lambda call: call.data.find("mar_ar") != -1)
async def mar_areement(call):
    try:
        
        
        data = call.data.split(";")
        days = int(data[1])
        id = call.from_user.id
        active_until = functions.GetUsers(id)[0]["ActiveUntil"]
        date_format = '%Y-%m-%d'
        active_until = datetime.strftime(active_until, DATE_FORMAT)                
        url=for_payments.make_recurse_pay(id=id,days=days,amount=mar_1[days],test=0)
        keyboard=types.InlineKeyboardMarkup()
        
        but1=types.InlineKeyboardButton(text="Назад",callback_data="mar_2pt;"+str(days))
        but=types.InlineKeyboardButton(text="Оплата",url=url)
        but2=types.InlineKeyboardButton(text="Офферта",callback_data="mar_offer;"+str(days))
        keyboard.row(but,but2)
        keyboard.add(but1)
        mess=await wait_until_send(id, "Стоимость подписки  на "+str(days)+" дней составит "+str(mar_1[days]) + " рублей.", reply_markup=keyboard)
        if id in delete_cache:
            for i in delete_cache[id]:
                bot.delete_message(id, i)
        delete_cache[id] = []
    except Exception as err:
        from traceback import format_exc
        print(err)
        format_exc(err)
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
    finally:
        try:
            await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        except:
            pass
@dp.callback_query_handler(lambda call: call.data.find("mar_net") != -1)
async def mar_no_agr(call):
    try:
        id = call.from_user.id
        mes = await wait_until_send(
            id, "К сожалению, вы не можете активировать подписку, пока не согласитесь с условиями обработки персональных данных и платежей. Нажмите 'Да', чтобы подтвердить согласие с условиями.")
        delete_cache[id].append(mes.id)
    except:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0