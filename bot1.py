import telebot
from pymongo import MongoClient

import os

telegram_token = os.getenv("TELEGRAM_KEY")
print(telegram_token)
bot = telebot.TeleBot('telegram_token')


client = MongoClient('localhost', 27017)
db = client['Telegram']
students = db['Stud']
callback = "Если возникнут вопросы или проблемы,  Вы можете связаться с преподавателем."

rules = "Тест состоит из 10 вопросов.\nПосле прохождения теста вы сможете увидеть кол-во правильных ответов.\n" \
        "Для просмотра  отправьте /result"

start_menu = telebot.types.ReplyKeyboardMarkup()
start_menu.row('Тест', 'Правила')
start_menu.row('Результат', 'Обратная связь')


@bot.message_handler(commands=['start'])
def check_students(message):
    bot.send_message(message.from_user.id, "Добро пожаловать!\nДля прохождения теста необходима регистрация /reg\n"
                                           "Если вы уже были зарегистрированы наберите /log")

@bot.message_handler(commands=['log'])
def log_in(message):
    client1 = students.find_one({"tg_id": message.from_user.id})
    if not client1:
        print('no users')
        bot.register_next_step_handler(message, registr_func)
    elif client1:
        print('yes')
        global name
        global surname
        global group
        global tg_id
        name = client["UserName"]
        tg_id = client["tg_id"]
        group = client["StudentGroup"]
        surname = client["Surname"]
        bot.send_message(message.from_user.id, "Добро пожаловать в главное меню", reply_markup=start_menu)

@bot.message_handler(commands=['admin'])
def admin_mod(message):
    if message.from_user.id == 404616985:
        bot.send_message(message.from_user.id, "Welcome to the admin mode\n"
                                               "Чтобы показать людей прошедших тест введите  /find_by_group\n"
                                               "Чтобы удалить данные пользователя /delete_user_data")
        if message.text == "/delete_user_data":
            deletions()
    else:
        bot.send_message(message.from_user.id, "You have no rights")

@bot.message_handler(commands=['reg'])
def registr_func(message):
    client = students.find_one({"tg_id": message.from_user.id})
    if not client:
        bot.send_message(message.from_user.id, "Введите имя")
        bot.register_next_step_handler(message, get_surname)
    else:
        bot.send_message(message.from_user.id, "Вы уже зарегистрированны наберите  /log")
        menu(message)

def get_surname(message):
    global regName
    regName = message.text
    bot.send_message(message.from_user.id, "Введите фамилию")
    bot.register_next_step_handler(message, get_group)


def get_group(message):
    global regSurname
    regSurname = message.text
    bot.send_message(message.from_user.id, "Введите учебную группу")
    bot.register_next_step_handler(message, reg_end)

def reg_end(message):
    global regGroup
    regGroup = message.text
    bot.send_message(message.from_user.id, "Регистрация окончена.\nВаш уникальный номер {}\n"
                                           "Для продолжения наберите /log".format(message.from_user.id))
    insert_user(regName, regSurname, regGroup, message.from_user.id)
    log_in(message)

@bot.message_handler(content_types=["start_test"])
def start_test(message):
    bot.send_message(message.from_user.id, "Работает")

def insert_user(regName, regSurname, regGroup, tg_id):
    db.Stud.insert_one({"UserName": regName, "Surname": regSurname, "StudentGroup": regGroup, "tg_id": tg_id })

@bot.message_handler(commands=['delete_user_data'])
def deletions(message):
    if message.from_user.id == 404616985:
        bot.send_message(message.from_user.id, "Для удаления пользователя введите tg_id")
        bot.register_next_step_handler(message, delete_data)
    else:
        bot.send_message(message.from_user.id, "Нет прав")

def delete_data(message):
    global delete_id
    delete_id = int(message.text)
    try:
        db.Stud.delete_one({"tg_id": delete_id})
        bot.send_message(message.from_user.id, "Удалено")
    except:
        bot.send_message(message.from_user.id, "Неудачно")
    admin_mod(message)

@bot.message_handler(commands=['find_by_group'])
def find_group(message):
    if message.from_user.id == 404616985:
        bot.send_message(message.from_user.id, "Введите группу для поиска")
        bot.register_next_step_handler(message, find_data)
    else:
        bot.send_message(message.from_user.id, "Нет прав")

def find_data(message):
    global find_by_group
    find_by_group = message.text
    try:
        fn = db.Stud.find_one({"StudentGroup": find_by_group})
        bot.send_message(message.from_user.id, f"Удачно\n{fn}")
    except:
        bot.send_message(message.from_user.id, "Неудачно")
    admin_mod(message)

def quest1(message, i):
    quest = ['ip', '1.1.1.1', '01.21.12', '31,123,31', 'ya.ru']
    quest_key = telebot.types.ReplyKeyboardMarkup()
    quest_key.row(quest[1], quest[2])
    quest_key.row(quest[3], quest[4])
    bot.send_message(message.from_user.id, quest[0], reply_markup=quest_key)
    bot.register_next_step_handler(message, quest2)

def quest2(message):
    global answer1
    answer1 = message.text
    quest = ['ip', '1.1.1.1', '01.21.12', '31,123,31', 'ya.ru']
    quest_key = telebot.types.ReplyKeyboardMarkup()
    quest_key.row(quest[1], quest[2])
    quest_key.row(quest[3], quest[4])
    bot.send_message(message.from_user.id, quest[0], reply_markup=quest_key)
    bot.register_next_step_handler(message, quest3)

def quest3(message):
    global answer2
    answer2 = message.text
    quest = ['ip', '1.1.1.1', '01.21.12', '31,123,31', 'ya.ru']
    quest_key = telebot.types.ReplyKeyboardMarkup()
    quest_key.row(quest[1], quest[2])
    quest_key.row(quest[3], quest[4])
    bot.send_message(message.from_user.id, quest[0], reply_markup=quest_key)
    bot.register_next_step_handler(message, finish)

def finish(message):
    global answer3
    answer3 = message.text
    db.Stud.update_one({"tg_id": tg_id}, {"$set": {"answer1": answer1, "answer2": answer2, "answer3": answer3}})
    res = check_result()
    bot.send_message(message.from_user.id, f'Твой тест окончен. Твоей результат {res}. Детальный отчет доступен по кнопке Результат', reply_markup=start_menu)
    check_result()


def check_result():
    good = 0
    no = 0
    tru = db.Stud.find_one({'tg_id': 404616985})
    if answer1 == tru[f'answer1']:
        good+=1
    else:
        no+=1
    if answer2 == tru[f'answer2']:
        good += 1
    else:
        no += 1
    if answer3 == tru[f'answer3']:
        good += 1
    else:
        no += 1
    return good


def result(message):
    a = db.Stud.find_one({'tg_id': message.from_user.id})
    tru = db.Stud.find_one({'tg_id': 404616985})
    i = 1
    while i <= 3:
        answer = a[f'answer{i}']
        tru_answer = tru[f'answer{i}']
        bot.send_message(message.from_user.id, f"tru:{tru_answer} --> your_answer: {answer}")
        i+=1
@bot.message_handler(content_types=['text'])
def menu(message):
    client = students.find_one({"tg_id": message.from_user.id})
    if not client:
        bot.register_next_step_handler(message, registr_func)
    else:
        global tg_id
        global name
        global get_surname
        global group
        client = students.find_one({"tg_id": message.from_user.id})
        surname = client["Surname"]
        group = client["StudentGroup"]
        name = client["UserName"]
        tg_id = client["tg_id"]
    global mess
    mess = message.text
    if message.text == "Обратная связь":
        bot.send_message(message.from_user.id, callback)
    elif message.text == "Правила":
        bot.send_message(message.from_user.id, rules, reply_markup=start_menu)
    elif message.text == "Тест":
        i = int(0)
        quest1(message, i)
    elif message.text == "Результат":
        result(message)

bot.polling(none_stop=True, interval=0)