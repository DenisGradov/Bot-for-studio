import telebot, sqlite3,ast,re,math
from telebot import types,util
from config import *

us=0
change_to=0
change_from=0
sum=0
comm=0
connect=sqlite3.connect('db.db')
cursor=connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    tg_id INTEGER,
    referals TEXT,
    referalsCol INTEGER,
    referalsBal INTEGER,
    myReferal INTEGER,
    trades INTEGER,
    tradesSum INTEGER,
    ban INTEGER
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fromm TEXT,
    too TEXT,
    acsii TEXT,
    rule TEXT,
    refSystem INTEGER,
    refBonys INTEGER
)""")
connect.commit()


    
connect=sqlite3.connect('db.db')
cursor=connect.cursor()
cursor.execute(f"SELECT id FROM settings")
data=cursor.fetchone()
if data is None:
    connect  = sqlite3.connect('db.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO settings (fromm, too, acsii, rule, refSystem, refBonys) VALUES (?,?, ?, ?, ?,?)', ('[]','[]','[]','[]',1,5,))
    connect.commit() 

bot=telebot.TeleBot(token)

@bot.message_handler()
def ms(message):
    
    connect=sqlite3.connect('db.db')
    cursor=connect.cursor()
    cursor.execute(f"SELECT tg_id FROM users WHERE tg_id=?",(message.chat.id,))
    data=cursor.fetchone()
    cursor.execute(f"SELECT tg_id FROM users WHERE tg_id=?",(message.chat.id,))
    ban=cursor.fetchone()
    if data is None:
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute('INSERT INTO users (username, tg_id, referals, referalsCol, referalsBal, myReferal,trades,tradesSum, ban) VALUES (?, ?, ?, ?,?,?,?,?,?)', (message.from_user.username, message.chat.id, '[]', 0, 0, 0,0,0,0))
        connect.commit() 
        ban=0
        if notif_about_new_user:
            klava=types.InlineKeyboardMarkup()
            klava.add(types.InlineKeyboardButton(text=btn_new_user,url=f't.me/{message.from_user.username}'))
            text=new_user_ms.format(username=message.from_user.username, tg_id=message.chat.id)
            bot.send_message(logs, text, parse_mode='Markdown',reply_markup=klava)
    else:
        ban=ban[0]

    if ban==1:
        pass
    else:
        x = bot.get_chat_member(mast_sub_Id[1], message.chat.id)
        if (x.status == "member" or x.status == "creator" or x.status == "administrator")or(mast_sub==False):
            if message.text=='/start':
                menu(message)
            else:
                bot.send_message(message.chat.id, error_ms)
        else:
            klava=types.InlineKeyboardMarkup(row_width=1)
            btn1=types.InlineKeyboardButton(text=mast_sub_Id[0], url=mast_sub_Id[2])
            btn2=types.InlineKeyboardButton(text=mast_sub_Id[4], callback_data='check')
            klava.add(btn1,btn2)
            bot.send_message(message.chat.id, mast_sub_Id[3], reply_markup=klava, parse_mode='Markdown')
   


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global change_to, change_from, sum,comm
    message=call.message


    connect=sqlite3.connect('db.db')
    cursor=connect.cursor()
    cursor.execute(f"SELECT ban FROM users WHERE tg_id=?",(message.chat.id,))
    ban=cursor.fetchone()
    if ban is None:
        ban=0
    else:
        ban=ban[0]

    if ban==1:
        pass
    else:
        x = bot.get_chat_member(mast_sub_Id[1], call.from_user.id)
        if ((x.status == "member" or x.status == "creator" or x.status == "administrator")or(mast_sub==False))or(mast_sub==False): 
            if call.data=='check':
                menu(message)
            elif call.data==btn_start[0]:
                photo = open('data/profile.png', 'rb')
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT trades FROM users WHERE tg_id = ?', (message.chat.id,))
                trades=(cursor.fetchall())[0][0]
                cursor.execute(f'SELECT tradesSum FROM users WHERE tg_id = ?', (message.chat.id,))
                tradesSum=(cursor.fetchall())[0][0]
                cursor.execute(f'SELECT referalsCol FROM users WHERE tg_id = ?', (message.chat.id,))
                referalsCol=(cursor.fetchall())[0][0]
                cursor.execute(f'SELECT referalsBal FROM users WHERE tg_id = ?', (message.chat.id,))
                referalsBal=(cursor.fetchall())[0][0]
                cursor.execute(f'SELECT myReferal FROM users WHERE tg_id = ?', (message.chat.id,))
                myReferal=(cursor.fetchall())[0][0]
                connect.commit()
                text=profile_ms.format(tg_id=message.chat.id, trades=trades,tradesSum=tradesSum, referalsCol=referalsCol, referalsBal=referalsBal)
                klava=types.InlineKeyboardMarkup(row_width=1)
                if myReferal==0:
                    btn=types.InlineKeyboardButton(text=btn_profile[0], callback_data=btn_profile[0])
                    klava.add(btn)
                btn=types.InlineKeyboardButton(text=btn_profile[1], callback_data=btn_profile[1])
                klava.add(btn)

                bot.send_photo(message.chat.id, photo, text, parse_mode='Markdown',reply_markup=klava)
            elif call.data==btn_profile[0]:
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT myReferal FROM users WHERE tg_id = ?', (message.chat.id,))
                myReferal=(cursor.fetchall())[0][0]
                connect.commit()
                if myReferal==0:
                    photo = open('data/referal.png', 'rb')
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn=btn_referal
                    klava.add(btn)
                    referal_code=bot.send_photo(message.chat.id, photo, referal_ms, parse_mode='Markdown',reply_markup=klava)
                    bot.register_next_step_handler(referal_code,referal_code_def)
                else:
                    bot.send_message(message.chat.id, referal_error_ms)
                    menu(message)
            elif call.data==btn_profile[1]:
                menu(message)
            elif call.data==btn_settings and call.message.chat.id==adminId:
                photo = open('data/settings.png', 'rb')
                klava=types.InlineKeyboardMarkup()
                for i in btn_admin:
                    if i==btn_admin[3]:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        btn2=types.InlineKeyboardButton(text=btn_rules, callback_data=btn_rules)
                        klava.add(btn,btn2)
                        btn1=types.InlineKeyboardButton(text=btn2_admin[0], callback_data=btn2_admin[0])
                        btn2=types.InlineKeyboardButton(text=btn2_admin[1], callback_data=btn2_admin[1])
                        klava.add(btn1,btn2)
                    else:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        klava.add(btn)
                bot.send_photo(message.chat.id, photo, admin_ms, parse_mode='Markdown', reply_markup=klava)
            elif call.data==btn_admin[0] and message.chat.id==adminId:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(btn_to_input)
                from_input=bot.send_message(message.chat.id, to_input_ms, reply_markup=klava, parse_mode='Markdown')
                bot.register_next_step_handler(from_input,from_input_def)
            elif call.data==btn_admin[1] and message.chat.id==adminId:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(btn_to_input)
                to_input=bot.send_message(message.chat.id, from_input_ms, reply_markup=klava, parse_mode='Markdown')
                bot.register_next_step_handler(to_input,to_input_def)
            elif call.data==btn_admin[2] and message.chat.id==adminId:
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT refSystem FROM settings')
                refSystem=(cursor.fetchone())
                cursor.execute(f'SELECT refBonys FROM settings')
                refBonys=(cursor.fetchone())[0]
                connect.commit()
                klava=types.InlineKeyboardMarkup(row_width=1)
                if int(refSystem[0])==1:
                    btn1=types.InlineKeyboardButton(text=btn_ref_system[0],callback_data=btn_ref_system[0])
                    btn2=types.InlineKeyboardButton(text=btn_ref_system[2],callback_data=btn_ref_system[2])
                    btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
                    klava.add(btn1,btn2,btn3)
                    text=ref_system_on_ms.format(refSystem=refSystem, refBonys=refBonys)
                else:
                    btn1=types.InlineKeyboardButton(text=btn_ref_system[1],callback_data=btn_ref_system[1])
                    btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
                    klava.add(btn1,btn3)
                    text=ref_system_on_ms.format(refSystem=refSystem, refBonys=refBonys)
                photo = open('data/ref-system.png', 'rb')
                bot.send_photo(message.chat.id, photo, text,reply_markup=klava,parse_mode='Markdown')
            elif ((call.data==btn_ref_system[0] or call.data==btn_ref_system[1]) and message.chat.id==adminId):
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT refSystem FROM settings')
                refSystem=(cursor.fetchone())
                cursor.execute(f'SELECT refBonys FROM settings')
                refBonys=(cursor.fetchone())[0]
                connect.commit()
                klava=types.InlineKeyboardMarkup(row_width=1)
                if call.data==btn_ref_system[1]:
                    btn1=types.InlineKeyboardButton(text=btn_ref_system[0],callback_data=btn_ref_system[0])
                    btn2=types.InlineKeyboardButton(text=btn_ref_system[2],callback_data=btn_ref_system[2])
                    btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
                    klava.add(btn1,btn2,btn3)
                    text=ref_system_on_ms.format(refSystem=refSystem, refBonys=refBonys)
                    refs=1
                else:
                    btn1=types.InlineKeyboardButton(text=btn_ref_system[1],callback_data=btn_ref_system[1])
                    btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
                    klava.add(btn1,btn3)
                    text=ref_system_of_ms.format(refSystem=refSystem, refBonys=refBonys)
                    refs=0
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute('UPDATE settings SET refSystem = (?)', (refs, )) 
                connect.commit()
                photo = open('data/ref-system.png', 'rb')
                bot.send_photo(message.chat.id, photo, text,reply_markup=klava,parse_mode='Markdown')
            elif call.data==btn_ref_system[2] and message.chat.id==adminId:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(btn_ref_bonys)
                ref_bonys=bot.send_message(message.chat.id,ref_bonys_ms, reply_markup=klava, parse_mode='Markdown')
                bot.register_next_step_handler(ref_bonys,ref_bonys_def)
            elif call.data==btn_ref_system[3]:
                photo = open('data/settings.png', 'rb')
                klava=types.InlineKeyboardMarkup()
                for i in btn_admin:
                    if i==btn_admin[3]:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        btn2=types.InlineKeyboardButton(text=btn_rules, callback_data=btn_rules)
                        klava.add(btn,btn2)
                        btn1=types.InlineKeyboardButton(text=btn2_admin[0], callback_data=btn2_admin[0])
                        btn2=types.InlineKeyboardButton(text=btn2_admin[1], callback_data=btn2_admin[1])
                        klava.add(btn1,btn2)
                    else:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        klava.add(btn)
                bot.send_photo(message.chat.id, photo, admin_ms, parse_mode='Markdown', reply_markup=klava)
            elif call.data==btn_admin[3]:
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT acsii FROM settings')
                acsii=(cursor.fetchone())[0]
                connect.commit()
                
                if acsii=='[]':
                    text=acsii_noth_ms
                else:
                    text=acsii
                klava=types.InlineKeyboardMarkup(row_width=1)
                for i in btn_acsii:
                    klava.add(types.InlineKeyboardButton(text=i, callback_data=i))
                photo = open('data/acs.png', 'rb')
                bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
            elif call.data==btn_start[2]:
                
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT acsii FROM settings')
                acsii=(cursor.fetchone())[0]
                connect.commit()
                
                if acsii=='[]':
                    text=acsii_noth_ms
                else:
                    text=acsii
                klava=types.InlineKeyboardMarkup(row_width=1)
                klava.add(types.InlineKeyboardButton(text=btn_acsii[1], callback_data=btn_acsii[1]))
                photo = open('data/acs.png', 'rb')
                bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
            elif call.data==btn_start[3]:
                
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT rule FROM settings')
                rules=(cursor.fetchone())[0]
                connect.commit()
                
                if rules=='[]':
                    text=rule_noth_ms
                else:
                    text=rules
                klava=types.InlineKeyboardMarkup(row_width=1)
                klava.add(types.InlineKeyboardButton(text=btn_rule[1], callback_data=btn_rule[1]))
                photo = open('data/rule.png', 'rb')
                bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
            elif call.data==btn_acsii[0]:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(btn_acsii_beh)
                add_aksii=bot.send_message(message.chat.id,add_acsii,parse_mode='Markdown', reply_markup=klava)
                bot.register_next_step_handler(add_aksii,add_aksii_def)
            elif call.data==btn_acsii[1]:
                menu(message)
            elif call.data==btn_admin[4]:
                menu(message)
            elif call.data==btn_rules:
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT rule FROM settings')
                rule=(cursor.fetchone())[0]
                connect.commit()
                
                if rule=='[]':
                    text=rule_noth_ms
                else:
                    text=rule
                klava=types.InlineKeyboardMarkup(row_width=1)
                for i in btn_rule:
                    klava.add(types.InlineKeyboardButton(text=i, callback_data=i))
                photo = open('data/rule.png', 'rb')
                bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
            elif call.data==btn_rule[0]:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(btn_rule_beh)
                add_rulee=bot.send_message(message.chat.id,add_rule,parse_mode='Markdown', reply_markup=klava)
                bot.register_next_step_handler(add_rulee,add_rule_def)
            elif call.data==btn_rule[1]:
                menu(message)
            elif call.data==btn_start[1]:
                photo = open('data/change.png', 'rb')
                
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT fromm FROM settings')
                fromm=(cursor.fetchone())[0]
                cursor.execute(f'SELECT too FROM settings')
                too=(cursor.fetchone())[0]
                connect.commit()

                if too=='[]' or fromm=='[]':
                    bot.send_message(message.chat.id, btrn_error_not_val,parse_mode='Markdown')
                    menu(message)
                else:

                    



                    print(too)
                    x2=fromm.split(',')
                    klava=types.InlineKeyboardMarkup(row_width=2)
                    items_list=fromm
                    buttons = []
                    for i in range(0, len(x2), 2):
                        button_row = []
                        ca=f"['{x2[i]}','fromm']"
                        button_row.append(types.InlineKeyboardButton(text=x2[i], callback_data=ca))
                        if i+1 < len(x2):
                            ca=f"['{x2[i+1]}','fromm']"
                            button_row.append(types.InlineKeyboardButton(text=x2[i+1], callback_data=ca))
                        try:
                            klava.add(button_row[0],button_row[1])
                        except:
                            klava.add(button_row[0])
                    klava.add(types.InlineKeyboardButton(text=btn_change_beh,callback_data=btn_change_beh))
                    bot.send_photo(message.chat.id, photo,how_crypto_change_ms,reply_markup=klava,parse_mode='Markdown')
            elif call.data==btn_change_beh:
                menu(message)
            elif call.data==btn_form[1]:
                menu(message)
            elif call.data==btn_form[0]:
                klava=types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,form_suc_ms,parse_mode='Markdown',reply_markup=klava)
                text=for_admin_form_ms.format(username=call.from_user.username, tg_id=message.chat.id, fromm=change_from, too=change_to, sum=sum,comm=comm)
                klava=types.InlineKeyboardMarkup()
                btn1=types.InlineKeyboardButton(text=btn_for_admin_form[0],url=f't.me/{call.from_user.username}')
                btn2=types.InlineKeyboardButton(text=btn_for_admin_form[1],callback_data=str(f"['{btn_for_admin_form[1]}','{message.chat.id}','{sum}']"))
                btn3=types.InlineKeyboardButton(text=btn_for_admin_form[2],callback_data=str(f"['{btn_for_admin_form[2]}','{message.chat.id}']"))
                klava.add(btn1,btn2,btn3)
                bot.send_message(logs,text,parse_mode='Markdown',reply_markup=klava)
                bot.delete_message(message.chat.id, message.message_id)
                menu(message)
            elif call.data==btn2_admin[0]:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add('◀️Назад')
                ads=bot.send_message(message.chat.id,'✏️ Введи текст своей рассылки. Если хочешь, что бы у рассылки была фотография - отправь фотографию, добавив к ней текст (одним сообщением)',reply_markup=klava)
                bot.register_next_step_handler(ads,ads_f)
            elif call.data==btn2_admin[1]:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(input_id_beh)
                inputid=bot.send_message(message.chat.id,input_id,reply_markup=klava)
                bot.register_next_step_handler(inputid,inputid_def)
            else:
                    x2=ast.literal_eval(call.data)
                    if x2[1]=='fromm':
                        print('s')
                        change_from=x2[0]
                        photo = open('data/change.png', 'rb')
                        
                        connect  = sqlite3.connect('db.db')
                        cursor = connect.cursor()
                        cursor.execute(f'SELECT fromm FROM settings')
                        fromm=(cursor.fetchone())[0]
                        cursor.execute(f'SELECT too FROM settings')
                        too=(cursor.fetchone())[0]
                        connect.commit()

                        if too=='[]' or fromm=='[]':
                            bot.send_message(message.chat.id, btrn_error_not_val,parse_mode='Markdown')
                            menu(message)
                        else:


                            print(too)
                            x2=too.split(',')
                            klava=types.InlineKeyboardMarkup(row_width=2)
                            items_list=fromm
                            buttons = []
                            for i in range(0, len(x2), 2):
                                button_row = []
                                ca=f"['{x2[i]}','too']"
                                button_row.append(types.InlineKeyboardButton(text=x2[i], callback_data=ca))
                                if i+1 < len(x2):
                                    ca=f"['{x2[i+1]}','too']"
                                    button_row.append(types.InlineKeyboardButton(text=x2[i+1], callback_data=ca))
                                try:
                                    klava.add(button_row[0],button_row[1])
                                except:
                                    klava.add(button_row[0])
                            klava.add(types.InlineKeyboardButton(text=btn_change_beh,callback_data=btn_change_beh))
                            bot.send_photo(message.chat.id, photo, how_crypto_change_take_ms, parse_mode='Markdown',reply_markup=klava)
                    elif x2[1]=='too':
                        print('s')
                        change_to=x2[0]
                        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                        klava.add(btn_change_beh2)
                        how_sum=bot.send_message(message.chat.id,choose_sum_ms,parse_mode='Markdown',reply_markup=klava)
                        bot.register_next_step_handler(how_sum,how_sum_def)
                    elif x2[0]==btn_for_admin_form[1]:
                        connect  = sqlite3.connect('db.db')
                        cursor = connect.cursor()
                        cursor.execute(f'SELECT refSystem FROM settings')
                        refSystem=(cursor.fetchone())[0]
                        cursor.execute(f'SELECT refBonys FROM settings')
                        refBonys=(cursor.fetchone())[0]
                        connect.commit()
                        if refSystem==1:

                            id=(x2[1])
                            connect  = sqlite3.connect('db.db')
                            cursor = connect.cursor()
                            cursor.execute(f'SELECT myReferal FROM users WHERE tg_id =?',(id,))
                            id=(cursor.fetchone())[0]

                            if id!=0:
                                cursor.execute(f'SELECT referalsBal FROM users WHERE tg_id =?',(id,))
                                refBal=(cursor.fetchone())
                                cursor.execute(f'SELECT trades FROM users WHERE tg_id =?',(x2[1],))
                                trades=(cursor.fetchone())[0]
                                cursor.execute(f'SELECT tradesSum FROM users WHERE tg_id =?',(x2[1],))
                                tradesSum=(cursor.fetchone())[0]
                                cursor.execute(f'SELECT username FROM users WHERE tg_id =?',(x2[1],))
                                username=(cursor.fetchone())[0]
                                connect.commit()
                                pros=(int(refBonys))/100
                                summa=int(x2[2])*pros
                                summa=math.ceil(summa)
                                print(pros)
                                refBal=int(refBal[0])+int(summa)
                                text=fromReferalBonys.format(username=username,referal=x2[1], summa=summa, refBal=refBal)
                                bot.send_message(x2[1],trade_conf,parse_mode='Markdown')
                                bot.send_message(id,text,parse_mode='Markdown')
                                tradesSum=int(tradesSum)+int(x2[2])
                                trades=trades+1
                                connect  = sqlite3.connect('db.db')
                                cursor = connect.cursor()
                                cursor.execute('UPDATE users SET referalsBal = (?) WHERE tg_id=(?)', (refBal,id )) 
                                connect.commit()
                                cursor.execute('UPDATE users SET trades = (?) WHERE tg_id=(?)', (trades,x2[1] )) 
                                connect.commit()
                                cursor.execute('UPDATE users SET tradesSum = (?) WHERE tg_id=(?)', (tradesSum,x2[1] )) 
                                connect.commit()

                                bot.send_message(logs,'% выплачен (с рефералом)')
                            else:  
                                cursor.execute(f'SELECT referalsBal FROM users WHERE tg_id =?',(id,))
                                refBal=(cursor.fetchone())
                                cursor.execute(f'SELECT trades FROM users WHERE tg_id =?',(x2[1],))
                                trades=(cursor.fetchone())[0]
                                cursor.execute(f'SELECT tradesSum FROM users WHERE tg_id =?',(x2[1],))
                                tradesSum=(cursor.fetchone())[0]
                                cursor.execute(f'SELECT username FROM users WHERE tg_id =?',(x2[1],))
                                username=(cursor.fetchone())[0]
                                connect.commit()
                                pros=(int(refBonys))/100
                                summa=int(x2[2])*pros
                                summa=math.ceil(summa)
                                print(pros)
                                bot.send_message(x2[1],trade_conf,parse_mode='Markdown')
                                tradesSum=int(tradesSum)+int(x2[2])
                                trades=trades+1
                                connect  = sqlite3.connect('db.db')
                                cursor = connect.cursor()
                                connect.commit()
                                cursor.execute('UPDATE users SET trades = (?) WHERE tg_id=(?)', (trades,x2[1] )) 
                                connect.commit()
                                cursor.execute('UPDATE users SET tradesSum = (?) WHERE tg_id=(?)', (tradesSum,x2[1] )) 
                                connect.commit()
                                bot.send_message(logs,'Добавлено в статистику (без реферала)')

                        else:  
                            bot.answer_callback_query(call.id, show_alert=True, text=ref_system_of_ms)
                    elif x2[0]==btn_for_admin_form[2]:
                        connect  = sqlite3.connect('db.db')
                        cursor = connect.cursor()
                        cursor.execute('UPDATE users SET ban = (?) WHERE tg_id=(?)', (1,x2[1] )) 
                        connect.commit()
                    elif x2[0]==btn_user_inf[0]:
                        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                        klava.add(input_id_beh)
                        global us
                        us=x2[1]
                        input_money=bot.send_message(message.chat.id,money_input,reply_markup=klava)
                        bot.register_next_step_handler(input_money,input_money_def)
                    elif x2[0]==btn_user_inf[1]:
                        
                        connect  = sqlite3.connect('db.db')
                        cursor = connect.cursor()
                        cursor.execute(f'SELECT ban FROM users WHERE tg_id =?',(x2[1],))
                        ban=(cursor.fetchone())
                        connect.commit()
                        try:
                            ban=ban[0]
                            if ban==0:
                                ban=1
                                text='Юзер был забанен'
                            else:
                                ban=0
                                text='Юзер был разбанен'
                            connect  = sqlite3.connect('db.db')
                            cursor = connect.cursor()
                            cursor.execute('UPDATE users SET ban = (?) WHERE tg_id=(?)', (ban,x2[1] )) 
                            connect.commit()
                            bot.send_message(message.chat.id,text,parse_mode='Markdown')
                            menu(message)
                            
                        except:
                            menu(message)
                    elif x2[0]==btn_user_inf[2]:
                        menu(message)       


                    print('ERROR 404!!') 
        else:
            klava=types.InlineKeyboardMarkup(row_width=1)
            btn1=types.InlineKeyboardButton(text=mast_sub_Id[0], url=mast_sub_Id[2])
            btn2=types.InlineKeyboardButton(text=mast_sub_Id[4], callback_data='check')
            klava.add(btn1,btn2)
            bot.send_message(message.chat.id, mast_sub_Id[3], reply_markup=klava, parse_mode='Markdown')


def input_money_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(input_id_beh)
        input_money=bot.send_message(message.chat.id,money_input,reply_markup=klava)
        bot.register_next_step_handler(input_money,input_money_def)
    elif not message.text.isnumeric():
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(input_id_beh)
        input_money=bot.send_message(message.chat.id,money_input,reply_markup=klava)
        bot.register_next_step_handler(input_money,input_money_def)
    else:
        try:
            global us
            print(f'ss{us}')
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET referalsBal = (?) WHERE tg_id=(?)', (message.text, us,)) 
            connect.commit()
            klava=types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id,money_input_suc,parse_mode='Markdown')
        except:
            print('error')
        menu(message)

def inputid_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(input_id_beh)
        inputid=bot.send_message(message.chat.id,f'{input_id}',reply_markup=klava)
        bot.register_next_step_handler(inputid,inputid_def)
    elif message.text==input_id_beh:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        menu(message)
    elif not message.text.isnumeric():
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(input_id_beh)
        inputid=bot.send_message(message.chat.id,input_id,reply_markup=klava)
        bot.register_next_step_handler(inputid,inputid_def)
    else:
        try:
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute(f'SELECT tg_id FROM users WHERE tg_id =?',(message.text,))
            tg_id=(cursor.fetchone())
            cursor.execute(f'SELECT username FROM users WHERE tg_id =?',(message.text,))
            username=(cursor.fetchone())
            cursor.execute(f'SELECT referals FROM users WHERE tg_id =?',(message.text,))
            referals=(cursor.fetchone())
            cursor.execute(f'SELECT referalsCol FROM users WHERE tg_id =?',(message.text,))
            referalsCol=(cursor.fetchone())
            cursor.execute(f'SELECT referalsBal FROM users WHERE tg_id =?',(message.text,))
            referalsBal=(cursor.fetchone())
            cursor.execute(f'SELECT myReferal FROM users WHERE tg_id =?',(message.text,))
            myReferal=(cursor.fetchone())
            cursor.execute(f'SELECT trades FROM users WHERE tg_id =?',(message.text,))
            trades=(cursor.fetchone())
            cursor.execute(f'SELECT tradesSum FROM users WHERE tg_id =?',(message.text,))
            tradesSum=(cursor.fetchone())
            cursor.execute(f'SELECT ban FROM users WHERE tg_id =?',(message.text,))
            ban=(cursor.fetchone())
            connect.commit()
            if id is None:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(input_id_beh)
                inputid=bot.send_message(message.chat.id,input_id,reply_markup=klava)
                bot.register_next_step_handler(inputid,inputid_def)
            else:
                text=user_inf.format(username=username[0], tg_id=message.text, referals=referals[0], referalsCol=referalsCol[0], referalsBal=referalsBal[0],  myReferal=myReferal[0], trades=trades[0], tradesSum=tradesSum[0], ban=ban[0])
                klava=types.InlineKeyboardMarkup()
                cu=f"['{btn_user_inf[0]}','{tg_id[0]}']"
                btn1=types.InlineKeyboardButton(text=btn_user_inf[0],callback_data=cu)
                cu=f"['{btn_user_inf[1]}','{tg_id[0]}']"
                btn2=types.InlineKeyboardButton(text=btn_user_inf[1],callback_data=cu)
                cu=f"['{btn_user_inf[2]}','{tg_id[0]}']"
                btn3=types.InlineKeyboardButton(text=btn_user_inf[2],callback_data=cu)
                klava.add(btn1,btn2,btn3)
                bot.send_message(message.chat.id, text, parse_mode='Markdown',reply_markup=klava)
        except:
            
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add(input_id_beh)
            inputid=bot.send_message(message.chat.id,f'Неверный id. {input_id}',reply_markup=klava)
            bot.register_next_step_handler(inputid,inputid_def)

        

photo_status=''
photo_id=''
description=''

def ads_f(message):
    global photo_status
    global photo_id
    global description
    if message.content_type!='photo' and message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        ads=bot.send_message(message.chat.id,'✏️ Введи текст своей рассылки. Если хочешь, что бы у рассылки была фотография - отправь фотографию, добавив к ней текст (одним сообщением)',reply_markup=klava)
        bot.register_next_step_handler(ads,ads_f)

    elif message.text=='◀️Назад':
        
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        menu(message)
    elif message.content_type=='photo':
        bot.send_photo(message.chat.id, message.photo[0].file_id, message.caption)
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='✅ Создаем'
        button2='⬅️ Вернуться'
        klava.add(button1,button2)
        photo_status=1
        description=message.caption
        photo_id=message.photo[0].file_id
        ads_y=bot.send_message(message.chat.id,'Вот так будет выглядеть рассылка. Проверь и подтверди старт рекламы', reply_markup=klava)
        bot.register_next_step_handler(ads_y,ads_yf)
    else:
        bot.send_message(message.chat.id, message.text)
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='✅ Создаем'
        button2='⬅️ Вернуться'
        klava.add(button1,button2)
        photo_status=0
        description=message.text
        ads_y=bot.send_message(message.chat.id,'Вот так будет выглядеть рассылка. Проверь и подтверди старт рекламы', reply_markup=klava)
        bot.register_next_step_handler(ads_y,ads_yf)

def ads_yf(message):
    if message.text is None:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        menu(message)
    elif message.text=='⬅️ Вернуться':
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        menu(message)
    else:

        global photo_status
        global photo_id
        global description

        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT id FROM users ORDER BY id DESC LIMIT 1')
        connect.commit()
        i=1
        i2=int((cursor.fetchall())[0][0])
        try_false=0
        try_true=0
        for i in range(i2+1):
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute(f'SELECT tg_id FROM users WHERE id = ?', (i,))
            connect.commit()
            if photo_status==1:
                try_true=try_true+1
                try:
                    bot.send_photo(cursor.fetchall()[0][0],photo_id,description)
                except Exception as error:
                    try_false=try_false+1

            else:
                try_true=try_true+1
                try:
                    bot.send_message(cursor.fetchall()[0][0],description)
                except Exception as error:
                    try_false=try_false+1
        
        text=f'📭 Рассылка была отправлена `{try_true-1}` пользователям!\n✅ Успешно доставлено: `{try_true-try_false}`\n❌ Не дошло: `{try_false-1}`'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        menu(message)



def how_sum_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_change_beh2)
        how_sum=bot.send_message(message.chat.id,choose_sum_ms,parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(how_sum,how_sum_def)
    elif message.text==btn_change_beh2:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        menu(message)
    elif not (message.text).isnumeric():
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_change_beh2)
        how_sum=bot.send_message(message.chat.id,choose_sum_ms,parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(how_sum,how_sum_def)
    else:
        global sum
        sum=message.text
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_change_beh2)
        commm=bot.send_message(message.chat.id,comment_ms,parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(commm,commm_def)

def commm_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_change_beh2)
        commm=bot.send_message(message.chat.id,comment_ms,parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(commm,commm_def)
    elif message.text==btn_change_beh2:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        menu(message)
    else:
        global comm,sum,change_from,change_to
        comm=message.text
        text=form_ms.format(too=change_to,fromm=change_from,comm=comm,sum=sum)
        klava=types.InlineKeyboardMarkup()
        btn1=types.InlineKeyboardButton(text=btn_form[0],callback_data=btn_form[0])
        btn2=types.InlineKeyboardButton(text=btn_form[1],callback_data=btn_form[1])
        klava.add(btn1,btn2)
        photo = open('data/change.png', 'rb')
        bot.send_photo(message.chat.id, photo, text, parse_mode='Markdown',reply_markup=klava)



def add_rule_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_rule_beh)
        add_rule=bot.send_message(message.chat.id,add_rule,parse_mode='Markdown', reply_markup=klava)
        bot.register_next_step_handler(add_rule,add_rule_def)
    elif message.text==btn_rule_beh:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_rule_beh_ms,reply_markup=klava,parse_mode='Markdown')
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT rule FROM settings')
        rule=(cursor.fetchone())[0]
        connect.commit()
        
        if rule=='[]':
            text=rule_noth_ms
        else:
            text=rule
        klava=types.InlineKeyboardMarkup(row_width=1)
        for i in btn_rule:
            klava.add(types.InlineKeyboardButton(text=i, callback_data=i))
        photo = open('data/rule.png', 'rb')
        bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
    else:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,add_rule_sec,reply_markup=klava,parse_mode='Markdown')
        
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute('UPDATE settings SET rule = (?)', (message.text, )) 
        connect.commit()
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT rule FROM settings')
        rule=(cursor.fetchone())[0]
        connect.commit()
        
        if rule=='[]':
            text=rule_noth_ms
        else:
            text=rule
        klava=types.InlineKeyboardMarkup(row_width=1)
        for i in btn_rule:
            klava.add(types.InlineKeyboardButton(text=i, callback_data=i))
        photo = open('data/rule.png', 'rb')
        bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
        
def add_aksii_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_acsii_beh)
        add_aksii=bot.send_message(message.chat.id,add_acsii,parse_mode='Markdown', reply_markup=klava)
        bot.register_next_step_handler(add_aksii,add_aksii_def)
    elif message.text==btn_acsii_beh:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,btn_acsii_beh_ms,reply_markup=klava,parse_mode='Markdown')
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT acsii FROM settings')
        acsii=(cursor.fetchone())[0]
        connect.commit()
        
        if acsii=='[]':
            text=acsii_noth_ms
        else:
            text=acsii
        klava=types.InlineKeyboardMarkup(row_width=1)
        for i in btn_acsii:
            klava.add(types.InlineKeyboardButton(text=i, callback_data=i))
        photo = open('data/acs.png', 'rb')
        bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
    else:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,add_acsii_sec,reply_markup=klava,parse_mode='Markdown')
        
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute('UPDATE settings SET acsii = (?)', (message.text, )) 
        connect.commit()
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT acsii FROM settings')
        acsii=(cursor.fetchone())[0]
        connect.commit()
        
        if acsii=='[]':
            text=acsii_noth_ms
        else:
            text=acsii
        klava=types.InlineKeyboardMarkup(row_width=1)
        for i in btn_acsii:
            klava.add(types.InlineKeyboardButton(text=i, callback_data=i))
        photo = open('data/acs.png', 'rb')
        bot.send_photo(message.chat.id,photo,text,reply_markup=klava,parse_mode='Markdown')
        


def ref_bonys_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_ref_bonys)
        ref_bonys=bot.send_message(message.chat.id,ref_bonys_ms, reply_markup=klava, parse_mode='Markdown')
        bot.register_next_step_handler(ref_bonys,ref_bonys_def)
    elif message.text==btn_ref_bonys:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, beg_ref_bonys, parse_mode='Markdown', reply_markup=klava)
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT refSystem FROM settings')
        refSystem=(cursor.fetchone())
        cursor.execute(f'SELECT refBonys FROM settings')
        refBonys=(cursor.fetchone())[0]
        connect.commit()
        klava=types.InlineKeyboardMarkup(row_width=1)
        if int(refSystem[0])==1:
            btn1=types.InlineKeyboardButton(text=btn_ref_system[0],callback_data=btn_ref_system[0])
            btn2=types.InlineKeyboardButton(text=btn_ref_system[2],callback_data=btn_ref_system[2])
            btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
            klava.add(btn1,btn2,btn3)
            text=ref_system_on_ms.format(refSystem=refSystem, refBonys=refBonys)
        else:
            btn1=types.InlineKeyboardButton(text=btn_ref_system[1],callback_data=btn_ref_system[1])
            btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
            klava.add(btn1,btn3)
            text=ref_system_on_ms.format(refSystem=refSystem, refBonys=refBonys)
        photo = open('data/ref-system.png', 'rb')
        bot.send_photo(message.chat.id, photo, text,reply_markup=klava,parse_mode='Markdown')
    elif not (message.text).isnumeric():
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_ref_bonys)
        ref_bonys=bot.send_message(message.chat.id,ref_bonys_ms, reply_markup=klava, parse_mode='Markdown')
        bot.register_next_step_handler(ref_bonys,ref_bonys_def)
    elif int(message.text)<1  or int(message.text)>100:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_ref_bonys)
        ref_bonys=bot.send_message(message.chat.id,ref_bonys_ms, reply_markup=klava, parse_mode='Markdown')
        bot.register_next_step_handler(ref_bonys,ref_bonys_def)
    else:
        refBonys=message.text
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute('UPDATE settings SET refBonys = (?)', (message.text, )) 
        connect.commit()
        text=new_ref_bonys_ms.format(refBonys=refBonys)
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=klava)
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT refSystem FROM settings')
        refSystem=(cursor.fetchone())
        cursor.execute(f'SELECT refBonys FROM settings')
        refBonys=(cursor.fetchone())[0]
        connect.commit()
        klava=types.InlineKeyboardMarkup(row_width=1)
        if int(refSystem[0])==1:
            btn1=types.InlineKeyboardButton(text=btn_ref_system[0],callback_data=btn_ref_system[0])
            btn2=types.InlineKeyboardButton(text=btn_ref_system[2],callback_data=btn_ref_system[2])
            btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
            klava.add(btn1,btn2,btn3)
            text=ref_system_on_ms.format(refSystem=refSystem, refBonys=refBonys)
        else:
            btn1=types.InlineKeyboardButton(text=btn_ref_system[1],callback_data=btn_ref_system[1])
            btn3=types.InlineKeyboardButton(text=btn_ref_system[3],callback_data=btn_ref_system[3])
            klava.add(btn1,btn3)
            text=ref_system_on_ms.format(refSystem=refSystem, refBonys=refBonys)
        photo = open('data/ref-system.png', 'rb')
        bot.send_photo(message.chat.id, photo, text,reply_markup=klava,parse_mode='Markdown')




            

def to_input_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_to_input)
        to_input=bot.send_message(message.chat.id, to_input_ms, reply_markup=klava, parse_mode='Markdown')
        bot.register_next_step_handler(to_input,to_input_def)
    elif message.text==btn_to_input:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,to_input_beh,parse_mode='Markdown',reply_markup=klava)
        photo = open('data/settings.png', 'rb')
        klava=types.InlineKeyboardMarkup()
        for i in btn_admin:
            if i==btn_admin[3]:
                btn=types.InlineKeyboardButton(text=i, callback_data=i)
                btn2=types.InlineKeyboardButton(text=btn_rules, callback_data=btn_rules)
                klava.add(btn,btn2)
                btn1=types.InlineKeyboardButton(text=btn2_admin[0], callback_data=btn2_admin[0])
                btn2=types.InlineKeyboardButton(text=btn2_admin[1], callback_data=btn2_admin[1])
                klava.add(btn1,btn2)
            else:
                btn=types.InlineKeyboardButton(text=i, callback_data=i)
                klava.add(btn)
        bot.send_photo(message.chat.id, photo, admin_ms, parse_mode='Markdown', reply_markup=klava)
    else:
        
            x=f"'[{message.text}]'"
            x2=ast.literal_eval(x)
            items_list = message.text.split(',')
            x2=[]
            for i2 in items_list:
                x2.append(f'{i2}')
            klava=types.InlineKeyboardMarkup(row_width=2)

            buttons = []
            for i in range(0, len(items_list), 2):
                button_row = []
                button_row.append(types.InlineKeyboardButton(text=items_list[i], callback_data=items_list[i]))
                if i+1 < len(items_list):
                    button_row.append(types.InlineKeyboardButton(text=items_list[i+1], callback_data='1Ca4^23zxfc@#$sdf4%@fks@vk%asht$2'))
                try:
                    klava.add(button_row[0],button_row[1])
                except:
                    klava.add(button_row[0])
            try:
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute('UPDATE settings SET too = (?)', ((message.text), )) 
                connect.commit()

                bot.send_message(message.chat.id,ti_input_primer,reply_markup=klava,parse_mode='Markdown')
               
                klava=types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,to_input_beh,parse_mode='Markdown',reply_markup=klava)
                photo = open('data/settings.png', 'rb')
                klava=types.InlineKeyboardMarkup()
                for i in btn_admin:
                    if i==btn_admin[3]:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        btn2=types.InlineKeyboardButton(text=btn_rules, callback_data=btn_rules)
                        klava.add(btn,btn2)
                        btn1=types.InlineKeyboardButton(text=btn2_admin[0], callback_data=btn2_admin[0])
                        btn2=types.InlineKeyboardButton(text=btn2_admin[1], callback_data=btn2_admin[1])
                        klava.add(btn1,btn2)
                    else:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        klava.add(btn)
                bot.send_photo(message.chat.id, photo, admin_ms, parse_mode='Markdown', reply_markup=klava)
                
            except:
                klava=types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,to_input_nac,reply_markup=klava,parse_mode='Markdown')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(btn_to_input)
                to_input=bot.send_message(message.chat.id, to_input_ms, reply_markup=klava, parse_mode='Markdown')
                bot.register_next_step_handler(to_input,to_input_def)


def from_input_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add(btn_to_input)
        to_input=bot.send_message(message.chat.id, to_input_ms, reply_markup=klava, parse_mode='Markdown')
        bot.register_next_step_handler(to_input,to_input_def)
    elif message.text==btn_to_input:
        
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,to_input_beh,parse_mode='Markdown',reply_markup=klava)
        photo = open('data/settings.png', 'rb')
        klava=types.InlineKeyboardMarkup()
        for i in btn_admin:
            if i==btn_admin[3]:
                btn=types.InlineKeyboardButton(text=i, callback_data=i)
                btn2=types.InlineKeyboardButton(text=btn_rules, callback_data=btn_rules)
                klava.add(btn,btn2)
                btn1=types.InlineKeyboardButton(text=btn2_admin[0], callback_data=btn2_admin[0])
                btn2=types.InlineKeyboardButton(text=btn2_admin[1], callback_data=btn2_admin[1])
                klava.add(btn1,btn2)
            else:
                btn=types.InlineKeyboardButton(text=i, callback_data=i)
                klava.add(btn)
        bot.send_photo(message.chat.id, photo, admin_ms, parse_mode='Markdown', reply_markup=klava)
    else:
        
            x=f"'[{message.text}]'"
            x2=ast.literal_eval(x)
            items_list = message.text.split(',')
            klava=types.InlineKeyboardMarkup(row_width=2)

            x2=[]
            for i2 in items_list:
                x2.append(f'{i2}')
            buttons = []
            for i in range(0, len(items_list), 2):
                button_row = []
                button_row.append(types.InlineKeyboardButton(text=items_list[i], callback_data=items_list[i]))
                if i+1 < len(items_list):
                    button_row.append(types.InlineKeyboardButton(text=items_list[i+1], callback_data='1Ca4^23zxfc@#$sdf4%@fks@vk%asht$2'))
                try:
                    klava.add(button_row[0],button_row[1])
                except:
                    klava.add(button_row[0])
            try:
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute('UPDATE settings SET fromm = (?)', ((message.text), )) 
                connect.commit()


                bot.send_message(message.chat.id,ti_input_primer,reply_markup=klava,parse_mode='Markdown')
               
                klava=types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,to_input_beh,parse_mode='Markdown',reply_markup=klava)
                photo = open('data/settings.png', 'rb')
                klava=types.InlineKeyboardMarkup()
                for i in btn_admin:
                    if i==btn_admin[3]:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        btn2=types.InlineKeyboardButton(text=btn_rules, callback_data=btn_rules)
                        klava.add(btn,btn2)
                        btn1=types.InlineKeyboardButton(text=btn2_admin[0], callback_data=btn2_admin[0])
                        btn2=types.InlineKeyboardButton(text=btn2_admin[1], callback_data=btn2_admin[1])
                        klava.add(btn1,btn2)
                    else:
                        btn=types.InlineKeyboardButton(text=i, callback_data=i)
                        klava.add(btn)
                bot.send_photo(message.chat.id, photo, admin_ms, parse_mode='Markdown', reply_markup=klava)
                
            except:
                klava=types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,to_input_nac,reply_markup=klava,parse_mode='Markdown')
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                klava.add(btn_to_input)
                to_input=bot.send_message(message.chat.id, to_input_ms, reply_markup=klava, parse_mode='Markdown')
                bot.register_next_step_handler(to_input,to_input_def)



def referal_code_def(message):
    if message.text is None:
        photo = open('data/referal.png', 'rb')
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn=btn_referal
        klava.add(btn)
        referal_code=bot.send_photo(message.chat.id, photo, referal_ms, parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(referal_code,referal_code_def)
    elif message.text==btn_referal:
        klava=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,referal_beg_ms,parse_mode='Markdown', reply_markup=klava)
        photo = open('data/profile.png', 'rb')
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT trades FROM users WHERE tg_id = ?', (message.chat.id,))
        trades=(cursor.fetchall())[0][0]
        cursor.execute(f'SELECT tradesSum FROM users WHERE tg_id = ?', (message.chat.id,))
        tradesSum=(cursor.fetchall())[0][0]
        cursor.execute(f'SELECT referalsCol FROM users WHERE tg_id = ?', (message.chat.id,))
        referalsCol=(cursor.fetchall())[0][0]
        cursor.execute(f'SELECT referalsBal FROM users WHERE tg_id = ?', (message.chat.id,))
        referalsBal=(cursor.fetchall())[0][0]
        cursor.execute(f'SELECT myReferal FROM users WHERE tg_id = ?', (message.chat.id,))
        myReferal=(cursor.fetchall())[0][0]
        connect.commit()
        text=profile_ms.format(tg_id=message.chat.id, trades=trades,tradesSum=tradesSum, referalsCol=referalsCol, referalsBal=referalsBal)
        klava=types.InlineKeyboardMarkup(row_width=1)
        if myReferal==0:
            btn=types.InlineKeyboardButton(text=btn_profile[0], callback_data=btn_profile[0])
            klava.add(btn)
        btn=types.InlineKeyboardButton(text=btn_profile[1], callback_data=btn_profile[1])
        klava.add(btn)
        bot.send_message(message.chat.id, text, parse_mode='Markdown',reply_markup=klava)
    elif str(message.text)==str(message.chat.id):
        bot.send_message(message.chat.id,referal_error2_ms, parse_mode='Markdown')
        photo = open('data/referal.png', 'rb')
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn=btn_referal
        klava.add(btn)
        referal_code=bot.send_photo(message.chat.id, photo, referal_ms, parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(referal_code,referal_code_def)
    else:
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT username FROM users WHERE tg_id = ?', (message.text,))
        myReferal=(cursor.fetchone())
        connect.commit()
        print(myReferal)
        if myReferal is None: 
            photo = open('data/referal.png', 'rb')
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn=btn_referal
            klava.add(btn)
            referal_code=bot.send_photo(message.chat.id, photo, referal_ms, parse_mode='Markdown',reply_markup=klava)
            bot.register_next_step_handler(referal_code,referal_code_def)
        else:
            
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute(f'SELECT referalsCol FROM users WHERE tg_id = ?', (message.text,))
            referalsCol=(cursor.fetchone())[0]

            cursor.execute(f'SELECT referals FROM users WHERE tg_id = ?', (message.text,))
            referals=(cursor.fetchone())[0]

            if referals=='[]':
                referals=[]
            else:
                referals=ast.literal_eval(referals)
            referals.append(message.chat.id)

            referalsCol=int(referalsCol)+1
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET myReferal = (?) WHERE tg_id = (?)', (message.text,message.chat.id, )) 
            connect.commit()
            cursor.execute('UPDATE users SET referals = (?) WHERE tg_id = (?)', (str(referals),message.text, )) 
            connect.commit()
            cursor.execute('UPDATE users SET referalsCol = (?) WHERE tg_id = (?)', (referalsCol,message.text, )) 
            connect.commit()
            klava=types.ReplyKeyboardRemove()
            text=referal_good_ms.format(username=myReferal[0], tg_id=message.text)
            bot.send_message(message.chat.id,text, parse_mode='Markdown',reply_markup=klava)
            text=referal_good2_ms.format(username=message.from_user.username, tg_id=message.chat.id, referalsCol=referalsCol)
            bot.send_message(message.text,text, parse_mode='Markdown')
            
            photo = open('data/profile.png', 'rb')
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute(f'SELECT trades FROM users WHERE tg_id = ?', (message.chat.id,))
            trades=(cursor.fetchall())[0][0]
            cursor.execute(f'SELECT tradesSum FROM users WHERE tg_id = ?', (message.chat.id,))
            tradesSum=(cursor.fetchall())[0][0]
            cursor.execute(f'SELECT referalsCol FROM users WHERE tg_id = ?', (message.chat.id,))
            referalsCol=(cursor.fetchall())[0][0]
            cursor.execute(f'SELECT referalsBal FROM users WHERE tg_id = ?', (message.chat.id,))
            referalsBal=(cursor.fetchall())[0][0]
            cursor.execute(f'SELECT myReferal FROM users WHERE tg_id = ?', (message.chat.id,))
            myReferal=(cursor.fetchall())[0][0]
            connect.commit()
            text=profile_ms.format(tg_id=message.chat.id, trades=trades,tradesSum=tradesSum, referalsCol=referalsCol, referalsBal=referalsBal)
            klava=types.InlineKeyboardMarkup(row_width=1)
            if myReferal==0:
                btn=types.InlineKeyboardButton(text=btn_profile[0], callback_data=btn_profile[0])
                klava.add(btn)
            btn=types.InlineKeyboardButton(text=btn_profile[1], callback_data=btn_profile[1])
            klava.add(btn)

            bot.send_photo(message.chat.id, photo, text, parse_mode='Markdown',reply_markup=klava)




def menu(message):
    klava=types.InlineKeyboardMarkup(row_width=2)
    for i in btn_start:
        if i==btn_start[2]:
            btn=types.InlineKeyboardButton(text=i, callback_data=i)
            btn2=types.InlineKeyboardButton(text=btn_start[3], callback_data=btn_start[3])
            klava.add(btn,btn2)
            break
        else:
            btn=types.InlineKeyboardButton(text=i, callback_data=i)
            klava.add(btn)
    btn=types.InlineKeyboardButton(text=btn_owner[0], url=btn_owner[1])
    klava.add(btn)
    if message.chat.id==adminId:
        btn=types.InlineKeyboardButton(text=btn_settings, callback_data=btn_settings)
        klava.add(btn)
    
    photo = open('data/menu.png', 'rb')
    bot.send_photo(message.chat.id, photo,start_ms,parse_mode='Markdown',reply_markup=klava)

bot.polling()