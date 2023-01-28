import telebot, sqlite3,ast,re,math,json,random,string
from telebot import types
from config import *
from db import *

artistr=0
TK=0
room=[]
roominfo=[]

bot= telebot.TeleBot(token=TOKEN)


connect=sqlite3.connect('db.db')
cursor=connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    tg_id INTEGER,
    username TEXT,
    status INTEGER,
    deal TEXT
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    code TEXT,
    customer TEXT,
    atistr TEXT,
    status TEXT,
    TK TEXT
)""")
connect.commit()


@bot.message_handler()
def ms(message):
    data=(select_db('name', 'users', 'tg_id', message.chat.id))
    if data==False:
        insert_db('name, tg_id, username, status, deal','users',(message.from_user.first_name, message.chat.id, message.from_user.username,0,0), '?,?,?,?,?')
        bot.send_message(logs,f'Новый юзер - {message.from_user.first_name} ({message.chat.id}), @{message.from_user.username}')
        user_menu(message)
    elif message.text=='➕Создать комнату' and admin_check(message):
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи id *исполнителя*:',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, artistr_id)
    elif message.text=='📚Комнаты' and admin_check(message):
        max=count_db('id','orders')
        text=''
        if max==0:
            bot.send_message(message.chat.id,'В боте еще нет комнат')
        for i in range(max):
            status=(select_db('status', 'orders', 'id', i+1))
            if status=='open':
                name=(select_db('name', 'orders', 'id', i+1))
                customer=(select_db('customer', 'orders', 'id', i+1))
                atistr=(select_db('atistr', 'orders', 'id', i+1))
                code=(select_db('code', 'orders', 'id', i+1))
                TK=(select_db('TK', 'orders', 'id', i+1))
                text=text+f'\n\n*Комната*: `{name}`\n*Код комнаты:* `{code}`\n*Исполнитель*: `{customer}`\n*Заказчик*: `{atistr}`\n*ТЗ*: `{TK}`'
            if i+1==max:
                if text=='':
                    text='У вас нет открытых комнат'
                    bot.send_message(message.chat.id,text,parse_mode='Markdown')
                    user_menu(message)
                    break
                else:
                    text=f'Список открытых комнат:{text}'
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    klava.add('⬅️Назад','🔒Закрыть комнату')
                    ms=bot.send_message(message.chat.id,text,reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ms, choose_room)
                    break
       
    elif message.text=='🧔🏿‍♂️Исполнители' and admin_check(message):
        artist_menu(message)
    elif message.text=='/id':
        bot.send_message(message.chat.id,f'`{message.chat.id}`',parse_mode='Markdown')
    else:
        status=(select_db('status', 'users', 'tg_id', message.chat.id))
        deal=(select_db('deal', 'users', 'tg_id', message.chat.id))
        name=(select_db('name', 'orders', 'code', deal))
        if status==1 and deal!= '0':
            atistr=(select_db('atistr', 'orders', 'code', deal))
            if atistr is None:
                bot.send_message(message.chat.id,'⚠️Заказчик еще не зашел в комнату!\nКак это случится - бот отправит тебе уведомление!')
            else:
                big_ms(atistr,f'Сообщение от исполнителя:\n{message.text}')
                
                klava=types.InlineKeyboardMarkup()
                klava.add(types.InlineKeyboardButton(text='✉️Написать', url=f't.me/{message.from_user.username}'))
                bot.send_message(logs, f'*Комната*: `{name} `\n*Отправитель*: `Исполнитель`',parse_mode='Markdown',reply_markup=klava)
                bot.forward_message(logs, message.chat.id, message.message_id)
        elif status==1 and deal=='0':
            user_menu(message)
        else:
            user_menu(message)



#Закрытие комнаты
def choose_room(message):
    if message.text is None:
        max=count_db('id','orders')
        text=''
        if max==0:
            bot.send_message(message.chat.id,'В боте еще нет комнат')
        for i in range(max):
            status=(select_db('status', 'orders', 'id', i+1))
            if status=='open':
                name=(select_db('name', 'orders', 'id', i+1))
                customer=(select_db('customer', 'orders', 'id', i+1))
                atistr=(select_db('atistr', 'orders', 'id', i+1))
                code=(select_db('code', 'orders', 'id', i+1))
                TK=(select_db('TK', 'orders', 'id', i+1))
                text=text+f'\n\n*Комната*: `{name}`\n*Код комнаты:* `{code}`\n*Исполнитель*: `{customer}`\n*Заказчик*: `{atistr}`\n*ТЗ*: `{TK}`'
            if i+1==max:
                if text=='':
                    text='У вас нет открытых комнат'
                    bot.send_message(message.chat.id,text,reply_markup=klava,parse_mode='Markdown')
                    user_menu(message)
                    break
                else:
                    text=f'Список открытых комнат:{text}'
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    klava.add('⬅️Назад','🔒Закрыть комнату')
                    ms=bot.send_message(message.chat.id,text,reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ms, choose_room)
                    break
    elif message.text=='⬅️Назад':
        user_menu(message)
    elif message.text=='🔒Закрыть комнату':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи  код комнаты, которую нужно закрыть.\nОбрати внимание, что после того как ты введешь код - комната сразу же будет закрыта',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, input_code_room)
    else:
        max=count_db('id','orders')
        text=''
        if max==0:
            bot.send_message(message.chat.id,'В боте еще нет комнат')
        for i in range(max):
            status=(select_db('status', 'orders', 'id', i+1))
            if status=='open':
                name=(select_db('name', 'orders', 'id', i+1))
                customer=(select_db('customer', 'orders', 'id', i+1))
                atistr=(select_db('atistr', 'orders', 'id', i+1))
                code=(select_db('code', 'orders', 'id', i+1))
                TK=(select_db('TK', 'orders', 'id', i+1))
                text=text+f'\n\n*Комната*: `{name}`\n*Код комнаты:* `{code}`\n*Исполнитель*: `{customer}`\n*Заказчик*: `{atistr}`\n*ТЗ*: `{TK}`'
            if i+1==max:
                if text=='':
                    text='У вас нет открытых комнат'
                    bot.send_message(message.chat.id,text,reply_markup=klava,parse_mode='Markdown')
                    user_menu(message)
                    break
                else:
                    text=f'Список открытых комнат:{text}'
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    klava.add('⬅️Назад','🔒Закрыть комнату')
                    ms=bot.send_message(message.chat.id,text,reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ms, choose_room)
                    break


#Ввод кода для закрытия комнаты
def input_code_room(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи  код комнаты, которую нужно закрыть.\nОбрати внимание, что после того как ты введешь код - комната сразу же будет закрыта',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, input_code_room)
    elif message.text=='⬅️Назад':
        max=count_db('id','orders')
        text=''
        if max==0:
            bot.send_message(message.chat.id,'В боте еще нет комнат')
        for i in range(max):
            status=(select_db('status', 'orders', 'id', i+1))
            if status=='open':
                name=(select_db('name', 'orders', 'id', i+1))
                customer=(select_db('customer', 'orders', 'id', i+1))
                atistr=(select_db('atistr', 'orders', 'id', i+1))
                code=(select_db('code', 'orders', 'id', i+1))
                TK=(select_db('TK', 'orders', 'id', i+1))
                text=text+f'\n\n*Комната*: `{name}`\n*Код комнаты:* `{code}`\n*Исполнитель*: `{customer}`\n*Заказчик*: `{atistr}`\n*ТЗ*: `{TK}`'
            if i+1==max:
                if text=='':
                    text='У вас нет открытых комнат'
                    bot.send_message(message.chat.id,text,reply_markup=klava,parse_mode='Markdown')
                    user_menu(message)
                    break
                else:
                    text=f'Список открытых комнат:{text}'
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    klava.add('⬅️Назад','🔒Закрыть комнату')
                    ms=bot.send_message(message.chat.id,text,reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ms, choose_room)
                    break
    else:
        name = select_db('name', 'orders', 'code', message.text)
        atistr = select_db('atistr', 'orders', 'code', message.text)
        customer = select_db('customer', 'orders', 'code', message.text)
        if name==False:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('⬅️Назад')
            ms=bot.send_message(message.chat.id,'Введи  код комнаты, которую нужно закрыть.\nОбрати внимание, что после того как ты введешь код - комната сразу же будет закрыта',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(ms, input_code_room)
        else:
            update_db('status', 'orders', 'code', message.text, 'close')
            update_db('deal', 'users', 'tg_id', atistr, '0')
            update_db('deal', 'users', 'tg_id', customer, '0')
            bot.send_message(message.chat.id,f'Комната *{name}* была успешно закрыта!',parse_mode='Markdown')
            bot.send_message(atistr,f'Ваш заказ был завершен, а комната *{name}* была закрыта!')
            bot.send_message(customer,f'Ваш заказ был завершен, а комната *{name}* была закрыта!',parse_mode='Markdown')
            bot.send_message(logs,f'Комната *{name}* была закрыта!',parse_mode='Markdown')
            user_menu(message)

            



#Реакция на кнопки в Настройка исполнителей
def artistr_list(message):
    if message.text is None:
        artist_menu(message)
    elif message.text=='➕Добавить москаля':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи ID москаля, и мы дадим ему 🍌*банан* и 🧊*стакан воды*!',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms,add_artistr)
    elif message.text=='🔪Убрать москаля':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи ID москаля, мы заберем у него все его вещи!',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms,dell_artistr)
    elif message.text=='⬅️Назад':
        user_menu(message)
    elif message.text=='🗒Мои москали':
        text=''
        max=count_db('id','users')
        for i in range(max):
            status=select_db('status', 'users', 'id', i+1)
            if status==1:
                name=select_db('name', 'users', 'id', i+1)
                username=select_db('username', 'users', 'id', i+1)
                tg_id=select_db('tg_id', 'users', 'id', i+1)
                text=text+f'\n⛏ {name} (`{tg_id}`) - @{username}'
            if i+1==max:
                if text=='':
                    text='😢😢😢Все ваши москали куда-то убежали(((9('
                else:
                    text=f'👮🏻‍♀️Вот список ваших москальов:\n{text}'
                bot.send_message(message.chat.id,text,parse_mode='Markdown')
                artist_menu(message)
                break
    else:
        artist_menu(message)


#добавление исполнителя
def add_artistr(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи ID москаля, и мы дадим ему 🍌*банан* и 🧊*стакан воды*!',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms,add_artistr)
    elif message.text=='⬅️Назад':
        artist_menu(message)
    else:
        if message.text.isnumeric():
            status=select_db('status', 'users', 'tg_id', int(message.text))
            name=select_db('name', 'users', 'tg_id', int(message.text))
            if str(status)=='1':
                bot.send_message(message.chat.id,'👑Эот москаль уже твой!\nДавай найдем другого')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add('⬅️Назад')
                ms=bot.send_message(message.chat.id,'Введи ID москаля, и мы дадим ему 🍌*банан* и 🧊*стакан воды*!',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(ms,add_artistr)
            elif str(status)=='0':
                bot.send_message(message.chat.id,f'⛓москаль *{name}* повелся на *банан* и *воду*. Мы заковали его в цепи и доставили на плантацию. Теперь он твой!',parse_mode='Markdown')
                update_db('status', 'users', 'tg_id', int(message.text), 1)
                artist_menu(message)
                
            else:
                bot.send_message(message.chat.id,'🤬Этот москаль не с нашей плантации!\nВведи правильный айди')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add('⬅️Назад')
                ms=bot.send_message(message.chat.id,'Введи ID москаля, и мы дадим ему 🍌*банан* и 🧊*стакан воды*!',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(ms,add_artistr)
        else:
            bot.send_message(message.chat.id,'🙅‍♂️Мне нужен айди москаля. (Айди - это число, если что..)\nВведи правильный айди')
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('⬅️Назад')
            ms=bot.send_message(message.chat.id,'Введи ID москаля, и мы дадим ему 🍌*банан* и 🧊*стакан воды*!',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(ms,add_artistr)


#удаление исполнителя
def dell_artistr(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи ID москаля, мы заберем у него все его вещи!',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms,dell_artistr)
    elif message.text=='⬅️Назад':
        artist_menu(message)
    else:
        if message.text.isnumeric():
            status=select_db('status', 'users', 'tg_id', int(message.text))
            name=select_db('name', 'users', 'tg_id', int(message.text))
            if str(status)=='0':
                bot.send_message(message.chat.id,'🧔🏿‍♂️Этот москаль и так без банана.\nДавай отберем банан у другого москаля')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add('⬅️Назад')
                ms=bot.send_message(message.chat.id,'Введи ID москаля, мы заберем у него все его вещи!',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(ms,dell_artistr)
            elif str(status)=='1':
                bot.send_message(message.chat.id,f'🔫москаль *{name}* добровольно (почти) отдал банан и воду. Теперь он свободен!',parse_mode='Markdown')
                update_db('status', 'users', 'tg_id', int(message.text), 0)
                artist_menu(message)
                
            else:
                bot.send_message(message.chat.id,'🤬Этот москаль не с нашей плантации!\nВведи правильный айди')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add('⬅️Назад')
                ms=bot.send_message(message.chat.id,'Введи ID москаля, мы заберем у него все его вещи!',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(ms,dell_artistr)
        else:
            bot.send_message(message.chat.id,'🙅‍♂️Мне нужен айди москаля. (Айди - это число, если что..)\nВведи правильный айди')
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('⬅️Назад')
            ms=bot.send_message(message.chat.id,'Введи ID москаля, мы заберем у него все его вещи!',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(ms,dell_artistr)


#ну теперь точно создание комнаты
def create_room_finish(message):
    global room,roominfo,TK
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('✅Создаем','❌Отменяем')
        ms=bot.send_message(artistr,f'Вот ваша будущаяя комната:\n\n*Имя:* `{roominfo[0]}`\n*Код*: `{roominfo[1]}`\n*Исполнитель*: `{roominfo[2]}`\n*ТЗ*: `{TK}`\n\nСоздаем?',reply_markup=klava,parse_mode='Markdown',disable_web_page_preview=True)
        bot.register_next_step_handler(ms,create_room_finish)
    elif message.text=='✅Создаем':
        insert_db('name, code, customer, status, TK','orders',(roominfo[0],roominfo[1],roominfo[2],'open',roominfo[3]), '?,?,?,?,?')
        update_db('deal', 'users', 'tg_id', int(roominfo[2]), roominfo[1])
        #deal
        klava=types.ReplyKeyboardRemove()
        ms=bot.send_message(roominfo[2],f'Вы были указаны как исполнитель для комнаты `{roominfo[0]}`. Задание выполняется согласно ТЗ ( {TK} ). Если заказчик хочет как-то изменить ТЗ, добавить что-то и так далее - ему необходимо связаться с куратором (кроме случаев с небольшими изменениями, которые не влияют на сложность / продолжительность твоей работы). Еще раз напомним про [правила исполнителей]({customerRules}), за нарушения которых вы будете исключены из проекта, без выплаты за проделанную работу. С момента когда заказчик подключится в чат - все ваши сообщения отправленные в бота будут автоматически отправлены заказчику. Так же все ваши сообщения логируются в специальном канале\nПосле выполнения заказа оповестите куратора. Удачной работы!',parse_mode='Markdown',disable_web_page_preview=True,reply_markup=klava)
        bot.pin_chat_message(chat_id=roominfo[2], message_id=ms.message_id)
        bot.send_message(message.chat.id,f'москаль успешно получил уведомление о заказе. Передай этот код заказчику: `{roominfo[1]}`',parse_mode='Markdown')
        bot.send_message(logs,f'Новая комната успешно создана!\n\n*Имя:* `{roominfo[0]}`\n*Код*: `{roominfo[1]}`\n*Исполнитель*: `{roominfo[2]}`\n*ТЗ*: `{TK}`',parse_mode='Markdown')
        user_menu(message)

#Создание комнаты
def create_room(message):
    global artistr, room, roominfo,TK
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад','🎬скип')
        ms=bot.send_message(message.chat.id,'Введи название комнаты:',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, create_room)
    elif message.text=='⬅️Назад':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи cсылку на ТЗ:',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, adding_TK)
    else:
        data=(select_db('code', 'orders', 'name', message.text))
        if message.text=='🎬скип':
            data=False
        if data==False:
            code=f'{str(random.randint(1,999))}{generate_random_string(3)}{str(random.randint(1,999))}{generate_random_string(3)}{str(random.randint(1,999))}{generate_random_string(3)}{str(random.randint(1,999))}{generate_random_string(3)}{str(random.randint(1,999))}{generate_random_string(3)}'
            if message.text=='🎬скип':
                message.text=code
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('✅Создаем','❌Отменяем')
            ms=bot.send_message(message.chat.id,f'Вот ваша будущаяя комната:\n\n*Имя:* `{message.text}`\n*Код*: `{code}`\n*Исполнитель*: `{artistr}`\n*ТЗ*: `{TK}`\n\nСоздаем?',reply_markup=klava,parse_mode='Markdown')
            roominfo=[message.text,code,artistr,TK]
            bot.register_next_step_handler(ms,create_room_finish)
        else:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('⬅️Назад','🎬скип')
            ms=bot.send_message(message.chat.id,'Комната с таким названием уже существует. Введи другое название!',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(ms, create_room)


#Добавление ТЗ к проекту
def adding_TK(message):
    global TK, artistr
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи cсылку на ТЗ:',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, adding_TK)
    elif message.text=='⬅️Назад':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи id *исполнителя*:',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, artistr_id)
    else:
        TK=message.text
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад','🎬скип')
        ms=bot.send_message(message.chat.id,'Введи название комнаты:',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, create_room)


#создание комнаты 1 шаг
def artistr_id(message):
    global artistr
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('⬅️Назад')
        ms=bot.send_message(message.chat.id,'Введи id *исполнителя*:',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(ms, artistr_id)
    elif message.text=='⬅️Назад':
        user_menu(message)
    else:
        if message.text.isnumeric():
            status=select_db('status', 'users', 'tg_id', int(message.text))
            if str(status)=='1':
                deal=select_db('deal', 'users', 'tg_id', int(message.text))
                if str(deal)=='0':
                    artistr=message.text 
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    klava.add('⬅️Назад')
                    ms=bot.send_message(message.chat.id,'Введи cсылку на ТЗ:',reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ms, adding_TK)
                else:
                    bot.send_message(message.chat.id,'💪Этот москаль конечно крутой, но на 1 банане он не вытянет 2 задания. Пусть закончит то, что уже делает')
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    klava.add('⬅️Назад')
                    ms=bot.send_message(message.chat.id,'Введи id *исполнителя*:',reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ms, artistr_id)

            elif str(status)=='0':
                bot.send_message(message.chat.id,'😅Этот порядочный клиент не москаль, зачем ты так с ним? Что он тебе сделал?')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add('⬅️Назад')
                ms=bot.send_message(message.chat.id,'Введи id *исполнителя*:',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(ms, artistr_id)
            else:
                bot.send_message(message.chat.id,'🦍Этого москаля нет в нашем гареме(')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add('⬅️Назад')
                ms=bot.send_message(message.chat.id,'Введи id *исполнителя*:',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(ms, artistr_id)
        else:
            bot.send_message(message.chat.id,'🙅‍♂️Мне нужен айди москаля. (Айди - это число, если что..)\nВведи правильный айди')
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('⬅️Назад')
            ms=bot.send_message(message.chat.id,'Введи id *исполнителя*:',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(ms, artistr_id)

#меню исполнителя
def artist_menu(message):
    klava=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    klava.add('➕Добавить москаля','🗒Мои москали','🔪Убрать москаля','⬅️Назад')
    ms=bot.send_message(message.chat.id,'Настройка исполнителей:',reply_markup=klava,parse_mode='Markdown')
    bot.register_next_step_handler(ms, artistr_list)

#Вводим код комнаты
def input_code(message):
    if message.text is None:
        klava=types.ReplyKeyboardRemove()
        ms=bot.send_message(message.chat.id,'Введите код комнаты, который вам дал куратор:',reply_markup=klava)
        bot.register_next_step_handler(ms,input_code)
    else:
        status=(select_db('status', 'orders', 'code', message.text))
        customer=(select_db('customer', 'orders', 'code', message.text))
        atistr=(select_db('atistr', 'orders', 'code', message.text))
        if (customer==False or status=='close') or atistr is not None:
            klava=types.ReplyKeyboardRemove()
            ms=bot.send_message(message.chat.id,'❌Ошибка, не верный код!',reply_markup=klava)
            message.text='/start'
            user_menu(message)
        else:
            update_db('atistr', 'orders', 'code', (message.text), message.chat.id)
            update_db('deal', 'users', 'tg_id', (message.chat.id), message.text)
            bot.send_message(customer,'❗️Заказчик зашел в комнату!\nТеперь все отправленные вами сообщения будут отправляться заказчику!')
            name=(select_db('name', 'orders', 'code', message.text))
            bot.send_message(message.chat.id,f'Вы зашли в комнату "{name}"!\nВсе ваши последующие сообщения будут переданы исполнителю\nЕще раз напомним, что по поводу изменения ТЗ, обсуждения цены можно общаться только с куратором\nПопытки обмена контактами так же запрещены\nС уважением, администрация')
            

#меню юзера
def user_menu(message):
    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
    status=(select_db('status', 'users', 'tg_id', message.chat.id))
    deal=(select_db('deal', 'users', 'tg_id', message.chat.id))
    name=(select_db('name', 'orders', 'code', deal))
    if status==0 and deal=='0' and message.text=='🚪Войти в комнату' and not admin_check(message):
        klava=types.ReplyKeyboardRemove()
        ms=bot.send_message(message.chat.id,'Введите код комнаты, который вам дал куратор:',reply_markup=klava)
        bot.register_next_step_handler(ms,input_code)
    else:
        if status==0 and deal=='0':
            klava.add('🚪Войти в комнату')    
            if admin_check(message):
                klava.add('➕Создать комнату','📚Комнаты','🧔🏿‍♂️Исполнители')
            bot.send_message(message.chat.id, 'Меню:',reply_markup=klava)
        elif status==0 and deal!='0':
            customer=(select_db('customer', 'orders', 'code', deal))
            big_ms(customer,f'Сообщение от заказчика:\n{message.text}')
            klava=types.InlineKeyboardMarkup()
            klava.add(types.InlineKeyboardButton(text='✉️Написать', url=f't.me/{message.from_user.username}'))
            bot.send_message(logs, f'*Комната*: `{name}`\n*Отправитель*: `Заказчик`',parse_mode='Markdown',reply_markup=klava)
            bot.forward_message(logs, message.chat.id, message.message_id)
        elif status==1 and deal=='0':
            klava=types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id,'⛔️Когда ты возьмешь заказ - тебе откроется доступ к боту',reply_markup=klava)
        

        
#Отправка длинного сообщения
def big_ms(to,ms):
    if len(ms) > 4096:
        for x in range(0, len(ms), 4096):
            bot.send_message(to, ms[x:x+4096])
    else:
        bot.send_message(to, ms)

#Проверка на админ-статус
def admin_check(message):
    for i in admin:
        if i==message.chat.id:
            return True

#генерация рандомной строки
def generate_random_string(length):
    letters = string.ascii_uppercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return(rand_string)

if __name__== "__main__":
   bot.polling(bot)
