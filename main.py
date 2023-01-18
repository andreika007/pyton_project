print('Загрузка программы...') 
import telebot 
from telebot import types 
import sqlite3 
bot = telebot.TeleBot('5418533436:AAHulotrkbczRAPkOn1TkIAMVXFdu4M6kBQ') 
conn = sqlite3.connect('data.db', check_same_thread=False) 
cur = conn.cursor() 
print('Бот запущен!') 
 
def get_user(uid): 
    cur.execute('SELECT * FROM users WHERE id = ?', (uid,)) 
    user = cur.fetchone() 
    return user 
 
def get_users(limit): 
    if limit > 0: 
        cur.execute('SELECT * FROM users ORDER BY money DESC LIMIT ?', (limit,)) 
        users = cur.fetchone() 
    else: 
        cur.execute('SELECT * FROM users') 
        users = cur.fetchone() 
    return users 
 
def controler_keyboard(name_kb): 
    if name_kb == 'main': 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        b1 = types.KeyboardButton('Попросить денег (+27₽)') 
        b2 = types.KeyboardButton('Рейтинг') 
        b3 = types.KeyboardButton('Мой профиль') 
        b4 = types.KeyboardButton('Настройки') 
        markup.add(b1) 
        markup.add(b2, b3, b4) 
        return markup 
 
@bot.message_handler(commands=['start']) 
def start(message): 
    uid = message.chat.id 
    name = message.from_user.first_name 
 
    if get_user(uid) == None: 
        cur.execute('INSERT INTO users(id, name, score, money) VALUES(?, ?, ?, ?)', (uid, name, 0, 0,)) 
        conn.commit() 
        bot.send_message(uid, 'Добро пожаловать в игру!\nДля продолжения нажмите на кнопку:', reply_markup=controler_keyboard('main')) 
    else: 
        bot.send_message(uid, 'С возвращением, ' + name, reply_markup=controler_keyboard('main')) 
 
def utabl(): 
    text = 'Рейтинг пользователей:\n\n' 
    for user in get_users(0): 
        text += str(user[1]) + ' | ' + str(user[3]) + '₽\n' 
    return text 
 
 
@bot.message_handler(content_types=['text']) 
def main_controler(message): 
    uid = message.chat.id 
    name = message.from_user.first_name 
 
    if get_user(uid) == None: 
        bot.send_message(uid, 'Извините, вы еще не зарегистрированы!\nДля начала игры нажмите /start') 
    else: 
        if message.text == 'Попросить денег (+27₽)': 
            user = get_user(uid) 
            money = user[3] 
            money = money + 27
            cur.execute('UPDATE users SET money = ? WHERE id = ?', (money, uid,)) 
            conn.commit() 
            bot.send_message(uid, 'Вам дали 27₽\nВаш баланс: ' + str(money) + '₽', reply_markup=controler_keyboard('main')) 
        if message.text == 'Рейтинг': 
            bot.send_message(uid, utabl(), reply_markup=controler_keyboard('main')) 
 
bot.infinity_polling()