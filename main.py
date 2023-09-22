#!/usr/bin/python3.11
import telebot                                                                                      #Подключение библиотеки pyTelegramBotAPI
from telebot import types                                                                           #Подключение метода types из библитеки выше
import sqlite3                                                                                      #Подключение библиотеки для работы с БД
import requests                                                                                     #Подключение библиотеки для работы со сторонними ресурсами
import json                                                                                         #Подключение библиотеки для работы с json объектами

TestBot = telebot.TeleBot('TelegramApiToken')                         #Указание токена бота для работы с ним (лучше вынести в отдельный файл)
API_weather = 'WeatherToken'                                                    #Указание токена стороннего ресурса (лучше вынести в отдельный файл)
name_home = ''
adress_home = ''
order_time= ''
operator_id = ''
user_first_name = ''
user_last_name = ''
user_id = ''                                                                                        #Объявление глобальных переменных

@TestBot.message_handler(commands=['start'])                                                        #Обработчик начальной команды бота
def helloworld(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)                                        #Объявление клавиатуры
    weatherBtn = types.KeyboardButton('Погода в Абакане')                                           #Кнопка "погода в абакане"
    eatBtn = types.KeyboardButton('Где покушать?')                                                  #Кнопка "где покушать"
    markup.row(weatherBtn, eatBtn)                                                            #Помещение этих кнопок в одну строку
    webAppTest = types.WebAppInfo("https://itleonix.ru/testbot/")                                   # создаем webappinfo - формат хранения url
    markup.row(types.KeyboardButton('Хочу кушать!', web_app=webAppTest))                       # создаем кнопку типа webapp
    orderBtn = types.KeyboardButton('Заказать столик')                                              #Кнопка "заказать столик"
    markup.row(orderBtn)                                                                            #Помещение кнопки на новую строку и ниже приветственное сообщение
    TestBot.send_message(message.chat.id, 'Здравствуйте! Я создан для демонстрации общих возможностей чат-бота.\nЕсли Вы не нашли здесь какой-то функции или я Вас заинтересовал, то обратитесь к моему разработчику <b>@itleonix</b>.\nЧтобы узнать обо мне подробнее, введите /help или выберите в списке команд.', parse_mode='html', reply_markup=markup)


@TestBot.message_handler(commands=['about'])                                                        #Обработчик команды /about
def about(message):                                                                                 #Функция обработчика
    botname = TestBot.get_my_name().name                                                            #Получение имени бота
    botdesc = TestBot.get_my_description().description                                              #Получение описания бота
    TestBot.send_message(message.chat.id, f'Имя этого бота {botname}. {botdesc}')              #Вывод сообщения пользователю

@TestBot.message_handler(commands=['help'])                                                         #Обработчик команды /help
def help(message):                                                                                  #Функция обработчика и ниже текст выводимого сообщения
    text_help = 'Здесь приведено описание каждой функции, которую я могу выполнять.\n\nКнопка <b>Погода в Абакане</b> - демонстрирует работу со сторонним сервисов, при условии, что разработчики сервиса это позволяют. В данном случае из стороннего ресурса берется актуальная температура воздуха в г. Абакан.\n\nКнопка <b>Где покушать?</b> - демонстрирует работу с базой данных, кроме основных функций добавить запись (кнопка "Запомнить новое") и удалить запись (кнопка "Забыть") можно реализовать выборку и вывод информации по определенным условиям, а содержание базы данных может быть любым.\n\nКнопка <b>Хочу кушать!</b> - демонстрирует работу внутреннего приложения Telegram, где я могу подключится к Вашему сайту или специально созданному для меня ресурсу.\n\nКнопка <b>Заказать столик</b> - в этой функции я связываюсь с кем-то из Вашего заведения и сообщаю, что мой собеседник хочет заказать столик, а этот кто-то уже решает принять заказ или нет. Перед заказом я могу сообщать клиенту какую-то информацию, ведь я всегда здесь.\n\nВесь остальной функционал зависит только от Ваших фантазии и потребностей.'
    commands = TestBot.get_my_commands()                                                            #Получение списка команд в виде листа
    commandecho = []                                                                                #Объявление листа
    for commandslist in commands:                                                                   #Цикл перебора всех значений
        commandecho.append('/<b>' + commandslist.command + '</b>' + ' - ' + commandslist.description)       #Добавление элементов в список в читаемом виде
    TestBot.send_message(message.chat.id, f'{text_help}\n\n<b>Список команд</b>\n\n'+'\n'.join(commandecho) , parse_mode='html')    #Вывод сообщения пользователю

@TestBot.message_handler(content_types=['text'])                                                    #Обработчик воспринимаего ботом текста
def weatherBtn(message):                                                                            #Соответствующая фнукицю
    if (message.text == 'Погода в Абакане'):                                                        #Если пользователь ввел "Погода в Абакане" то...
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=abakan&appid={API_weather}&units=metric&lang=ru')        #Отправка запроса к ресурсу с указанным токеном
        data = json.loads(res.text)                                                                 #Получение json объекта и использование нужной информации
        weather_mess = f'Меня подключили к внешнему сервису метеорологов, теперь я могу показать актуальную погоду на текущий момент 🌤🌥🌦🌧\n\nТемпература за окном <b>{int(data["main"]["temp"])} &#176;C.</b>\n\nКонечно, можно сделать, чтобы картинка менялась в соответствии с погодой, и прочие фичи.'
        fotoAbk = open('./Abakan.jpg', 'rb')                                                        #Открытие фотографии
        TestBot.send_photo(message.chat.id, fotoAbk, weather_mess, parse_mode='html')               #Отправка пользователю фото с текстом
    elif message.text == 'Где покушать?':                                                           #Если пользователь ввел "Где покушать?"
        try:                                                                                        #Обработчик исключений
            conn = sqlite3.connect('testbot.db')                                                    #Подключение к БД
            cur = conn.cursor()                                                                     #Указание курсора

            cur.execute('SELECT * FROM foodhome')                                                   #Запрос к БД с выводом всей информации из таблицы
            foodhomelist = cur.fetchall()
            food_home_mess = ''                                                                     #Объявление переменной
            for row in foodhomelist:                                                                #Формирование текста для сообщения
                food_home_mess += f'<b>{row[1]}</b> ожидает Вас по адресу: <b>{row[2]}</b>. Время работы {row[3]}. 🍗🍕🍔 Регистрационный № {row[0]}'+'\n\n'

            cur.close()
            conn.close()                                                                            #Ввыход и БД

            inssert_food_home = types.InlineKeyboardMarkup()                                        #Объявление кнопок под сообщением
            inssert_food_btn = types.InlineKeyboardButton('Запомнить новое', callback_data='insert')
            del_food_btn = types.InlineKeyboardButton('Забыть', callback_data='delete')         #2 кнопки с задаными значениям
            inssert_food_home.row(inssert_food_btn, del_food_btn)                               #Помещение кнопок на одну строку и вывод сообщения пользователю
            TestBot.send_message(message.chat.id,f'Меня подключили к базе данных, и теперь я могу запоминать и выводить информацию. Вот, смотрите  \n\n{food_home_mess}',parse_mode='html', reply_markup=inssert_food_home)


        except Exception as ex:                                                                         #Обработчик ошибки подключения к БД
            TestBot.send_message(message.chat.id, '<b>Error connecting to database</b>', parse_mode='html')
            cur.close()
            conn.close()

    elif message.text == 'Заказать столик':                                                             #Если пользователь ввел "Заказать столик"
        global user_id
        user_id = message.chat.id                                                                       #Запись id чата в глобальную переменную
        TestBot.send_message(message.chat.id, 'На какое время Вам нужен столик? (Например: 12:30)', parse_mode='html')      #Вывод сообщения пользователю
        TestBot.register_next_step_handler(message, order_mes)                                          #Переход к указанной функции

    else: TestBot.send_message(message.chat.id, 'Я Вас не понимаю. Обратитесь к команде /help', parse_mode='html')  #обработка некорректного ввода

@TestBot.callback_query_handler(func=lambda callback: True)                                             #Обработчик решения о принятии заказа
def order_otv_mes(callback):
    if callback.data == 'order_success':                                                                #Если нажата кнопка со значением order_success
        TestBot.delete_message(operator_id, callback.message.message_id)                                #Удаляется сообщение-запрос
        TestBot.send_message(operator_id, f'Вы приняли заказ! Ожидайте гостя с именем {user_first_name} {user_last_name} в {order_time}')   #Остается уведомлении о принятии заказа
        TestBot.send_message(user_id, f'Ваш столик заказан. Будем ожидать Вас в {order_time}')     #Отправка пользователю сообщения
    elif callback.data == 'order_error':                                                                #Если нажата кнопка со значением order_error
        order_err_btn = types.InlineKeyboardMarkup()                                                    #Создается кнопка
        order_err_mes = types.InlineKeyboardButton('Выбрать другое время', callback_data='order_err_mes')
        order_err_btn.row(order_err_mes)
        TestBot.delete_message(operator_id, callback.message.message_id)                                #Удаляется сообщение
        TestBot.send_message(operator_id, f'Вы отказали гостю с именем {user_first_name} {user_last_name}. Надеюсь это было обоснованно')   #У оператора остается уведомление об отказе клиенту
        TestBot.send_message(user_id, f'К сожалению, на {order_time} нет свободных столиков. Может быть другое время?', reply_markup=order_err_btn)  #Пользователю предлагается выбрать другое время
    elif callback.data == 'order_err_mes':                                                              #Если пользователь нажал выбрать другое время
        TestBot.send_message(callback.message.chat.id, 'На какое время Вам нужен столик? (Например: 12:30)', parse_mode='html')
        TestBot.register_next_step_handler(callback.message, order_mes)                                 #Запускается указанная функция
    else:
        TestBot.send_message(callback.message.chat.id, 'Я Вас не понимаю. Обратитесь к команде /help', parse_mode='html') #Обработка ошибки

@TestBot.callback_query_handler(func=lambda callback: True)
def callback_food_home(callback):                                                                          #Функция работы с БД
    if callback.data == 'insert':
        TestBot.send_message(callback.message.chat.id, 'Введите название заведения', parse_mode='html')
        TestBot.register_next_step_handler(callback.message, name_food_home)
    elif callback.data == 'delete':
        TestBot.send_message(callback.message.chat.id, 'Введите регистрационный номер заведения, которое нужно забыть', parse_mode='html')
        TestBot.register_next_step_handler(callback.message, index_food_home)
    else: TestBot.send_message(callback.message.chat.id, 'Я Вас не понимаю. Обратитесь к команде /help', parse_mode='html')

def order_mes(message):                                                                                    #Функция работы с оператором
    global order_time
    global operator_id
    global user_first_name
    global user_last_name
    order_time = message.text.strip()
    #operator_id = '1278985873'
    operator_id ='6191695022'
    TestBot.send_message(message.chat.id, f'Одну минуту, я уточну есть ли свободный столик на {order_time}.\n\nДемонстрационный бот, поэтому время ответа может быть увеличено, спапсибо за ожидание.', parse_mode='html')
    order = types.InlineKeyboardMarkup()
    order_success = types.InlineKeyboardButton('Принять заказ', callback_data='order_success')
    order_error = types.InlineKeyboardButton('Отказать', callback_data='order_error')
    order.row(order_success, order_error)
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    TestBot.send_message(operator_id, f'<b>Внимание ЗАКАЗ!!!</b>\n\n<b>{user_first_name} {user_last_name}</b> хочет заказать столик на <b>{order_time}</b>. Есть свободные?', parse_mode='html', reply_markup=order)

def name_food_home(message):
    global name_home
    name_home = message.text.strip()
    TestBot.send_message(message.chat.id, 'Теперь нужен адрес', parse_mode='html')
    TestBot.register_next_step_handler(message, adress_food_home)

def adress_food_home(message):
    global adress_home
    adress_home = message.text.strip()
    TestBot.send_message(message.chat.id, 'И время работы', parse_mode='html')
    TestBot.register_next_step_handler(message, timework_food_home)

def timework_food_home(message):
    timework_home = message.text.strip()
    try:
        conn = sqlite3.connect('testbot.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO foodhome (name, adress, timework) VALUES ('%s', '%s', '%s')" % (name_home, adress_home, timework_home))
        conn.commit()
        cur.close()
        conn.close()

        TestBot.send_message(message.chat.id, 'Запомнил', parse_mode='html')

    except Exception as ex:
        TestBot.send_message(message.chat.id, '<b>Error connecting to database</b>', parse_mode='html')
        cur.close()
        conn.close()

def index_food_home(message):
    index_del = message.text.strip()
    dele = int(index_del)
    try:
        conn = sqlite3.connect('testbot.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM foodhome WHERE id = '%d'" % (dele))
        conn.commit()
        cur.close()
        conn.close()

        TestBot.send_message(message.chat.id, 'Забыл', parse_mode='html')

    except Exception as ex:
        TestBot.send_message(message.chat.id, '<b>Error connecting to database</b>', parse_mode='html')
        cur.close()
        conn.close()




TestBot.polling(none_stop=True)
