import telebot
import requests
import json
import os.path
import os
from base64 import b64decode
import time
from config import *
import spmapi

bot = telebot.TeleBot(bot_token)
print('Бот Запущен')

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Онлайн', 'Время и Погода')
keyboard.row('Проверить кто онлайн', 'Чат')
keyboard.row('Разное', 'Настройки')
keyboard.row('Помощь')

keyboardChat = telebot.types.ReplyKeyboardMarkup(True)
keyboardChat.row('Последнее сообщение')
keyboardChat.row('Последних 5 сообщений', 'Последних 10 сообщений')
keyboardChat.row('Последних 25 сообщений', 'Последних 50 сообщений')
keyboardChat.row('Назад')

keyboardHelp = telebot.types.ReplyKeyboardMarkup(True)
keyboardHelp.row('Информация о боте')
keyboardHelp.row('Проверка онлайна по списку')
keyboardHelp.row('Раздел "Разное"')
keyboardHelp.row('Раздел "Настройки"')
keyboardHelp.row('Баги API')
keyboardHelp.row('Назад')

keyboardRazn = telebot.types.ReplyKeyboardMarkup(True)
keyboardRazn.row('Проверить онлайн по нику', 'Скачать скин игрока')
keyboardRazn.row('Назад')

keyboardOpt = telebot.types.ReplyKeyboardMarkup(True)
keyboardOpt.row('Добавить ник', 'Удалить ВСЕ ники')
keyboardOpt.row('Назад')

keyboardBack = telebot.types.ReplyKeyboardMarkup(True)
keyboardBack.row('Назад')

@bot.message_handler(content_types=['text'])
def send_text(message):
    chatlog = str(f'<code>{message.chat.id}</code> @{str(message.chat.username)} {str(message.chat.first_name)} {str(message.chat.last_name)}')
    bot.register_next_step_handler(message, send_text)
    text = message.text
    if text == '/start' or text == '/restart':
        bot.send_message(message.chat.id, u'<b>Приветствую!</b> Вы запустили бота который использует <b>SPapi</b>.\nВ этом боте можно узнать: <b>онлайн</b>, <b>время и погоду</b>, <b>последние сообщения из чата</b>.\nТакже можно проверять <b>онлайн определеных игроков</b>(например своего города), или одного игрока и <b>скачивать скины</b>.\nПоодробней во вкладке "Помощь"', parse_mode="HTML", reply_markup=keyboard)
        bot.send_message(log_channel, f'{chatlog},\nЗапустил бота', parse_mode= 'HTML')
    elif text ==  'Онлайн' or text == '/online' or text == '/players':
        try:
            spmOnline = spmapi.online.all()
            playersList = str()
            for number in range(spmOnline["count"]-1):
                playersList += f'{spmOnline["players"][number]["nick"]}\n'
            playersList += f'\nИгроков на сервере: <b>{spmOnline["count"]-1}</b> из <b>{spmOnline["max"]}</b>'
            bot.send_message(message.chat.id, playersList, parse_mode= 'HTML', reply_markup=keyboard)
        except:
            bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил Онлайн', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
    elif text == 'Время и Погода' or text == '/weather' or text == '/time':
        try:
            spmTime = spmapi.world.all()
            if spmTime["time"] == "DAY":
                time = "День"
            elif spmTime["time"] == "NIGHT":
                time = "Ночь"
            else:
                time = "Ошибка"
            if spmTime["weather"] == "CLEAR":
                weather = "Ясно"
            elif spmTime["weather"] == "RAIN":
                weather = "Дождь"
            elif spmTime["weather"] == "THUNDER":
                weather = "Гроза"
            else:
                weather = "Ошибка"
            bot.send_message(message.chat.id, f'Время суток: <b>{time}</b>\nТики: <b>{spmTime["ticks"]}</b>\nПогода: <b>{weather}</b>', parse_mode= 'HTML', reply_markup=keyboard)
        except:
            bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        bot.send_message(log_channel, f'{chatlog},\nЗапросил Время и Погоду', parse_mode= 'HTML')
    elif text == 'Чат':
        bot.send_message(message.chat.id, "Переход в чат", reply_markup=keyboardChat)
    elif text == 'Последнее сообщение' or text == '/last':
        try: 
            spmChat = spmapi.chat.last()
            bot.send_message(message.chat.id, f'<b>{spmChat["name"]}:</b> {spmChat["message"]}', parse_mode= 'HTML')
        except:
            bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил последнее сообщение', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
    elif text == 'Последних 5 сообщений' or text == '/last5':
        try: 
            spmChat = spmapi.chat.chat()
            chatList = str()
            for number in range(45, 50):
                chatList += f'<b>{spmChat[number]["name"]}:</b> {spmChat[number]["message"]}\n \n'
            bot.send_message(message.chat.id, chatList, disable_web_page_preview=True, parse_mode= 'HTML')
        except:
            bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил последних 5 сообщений', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
    elif text == 'Последних 10 сообщений' or text == '/last10':
        try: 
            spmChat = spmapi.chat.chat()
            chatList = str()
            for number in range(40, 50):
                chatList += f'<b>{spmChat[number]["name"]}:</b> {spmChat[number]["message"]}\n \n'
            bot.send_message(message.chat.id, chatList, disable_web_page_preview=True, parse_mode= 'HTML')
        except:
            bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил последних 10 сообщений', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
    elif text == 'Последних 25 сообщений' or text == '/last25':
        try: 
            spmChat = spmapi.chat.chat()
            chatList = str()
            for number in range(25, 50):
                chatList += f'<b>{spmChat[number]["name"]}:</b> {spmChat[number]["message"]}\n \n'
            bot.send_message(message.chat.id, chatList, disable_web_page_preview=True, parse_mode= 'HTML')
        except:
            bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил последних 25 сообщений', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
    elif text == 'Последних 50 сообщений' or text == '/last50':
        try: 
            spmChat = spmapi.chat.chat()
            chatList = str()
            for number in range(0, 50):
                chatList += f'<b>{spmChat[number]["name"]}:</b> {spmChat[number]["message"]}\n \n'
            bot.send_message(message.chat.id, chatList, disable_web_page_preview=True, parse_mode= 'HTML')
        except:
            bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил последних 50 сообщений', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
    elif text == 'Назад':
        bot.send_message(message.chat.id, "Переход в главное меню", reply_markup=keyboard)
    elif text == '/find' or text == 'Проверить онлайн по нику':
        bot.send_message(message.chat.id, "Введите ник", reply_markup=keyboardBack)
        bot.register_next_step_handler(message, nick_check)
    elif text == '/skin' or text == 'Скачать скин игрока':
        bot.send_message(message.chat.id, "Введите ник", reply_markup=keyboardBack)
        bot.register_next_step_handler(message, skin_req)
    elif text == '/addnick' or text == 'Добавить ник':
        bot.send_message(message.chat.id, "Введите ник", reply_markup=keyboardBack)
        bot.register_next_step_handler(message, add_nick)
    elif text == '/check' or text == 'Проверить кто онлайн':
        if os.path.exists(f'profiles/{message.chat.id}.txt') == 0:
            bot.send_message(message.chat.id, '<b>У вас не добавлены ники</b>\nПерейдите в настроки чтобы их добавить:\n/options', parse_mode= 'HTML')
        else:
            try:
                playerOnline = str()
                playerList = open(f'profiles/{message.chat.id}.txt').readlines()
                spmOnline = spmapi.online.all()
                for line in playerList: 
                    uuid = line.strip()
                    uuidTrim = uuid[:8]+uuid[9:13]+uuid[14:18]+uuid[19:23]+uuid[24:36]
                    nameReq = json.loads(requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuidTrim}').text)
                    onlineStatus = 0
                    for player in range(0, spmOnline["count"]-1):
                        if str(f' {spmOnline["players"][player]["uuid"]}').find(uuid) != -1:
                            onlineStatus += 1
                    if onlineStatus >= 1:
                        playerOnline += str(f'<b>{nameReq["name"]} - Онлайн</b>\n')
                    elif onlineStatus == 0:
                        playerOnline += str(f'{nameReq["name"]} - Офлайн\n')
                bot.send_message(message.chat.id, playerOnline, parse_mode= 'HTML', reply_markup=keyboard)
            except:
                bot.send_message(message.chat.id, 'Ошибка, повторите через несколько секунд', parse_mode= 'HTML')
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил ники', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
    elif text == '/delnicks' or text == 'Удалить ВСЕ ники':
        try:
            os.remove(f'profiles/{message.chat.id}.txt')
            bot.send_message(message.chat.id, 'Ники удалены', parse_mode= 'HTML')
            try:
                bot.send_message(log_channel, f'{chatlog},\nУдалил ники', parse_mode= 'HTML')
            except:
                print('Ошибка при отправке сообщения в чат')
        except:
            bot.send_message(message.chat.id, 'Ошибка, возможно у вас не было добавленых ников', parse_mode= 'HTML')
    elif text == 'Инфо' or text == '/info' or text == 'Помощь' or text == '/help':
        bot.send_message(message.chat.id, "Переход в помощь", reply_markup=keyboardHelp)
    elif text == 'Баги API':
        bot.send_message(message.chat.id, "- У SPapi есть баг, что сообщения в чате могут вывестись не те что были на сервере, а случайные.\n<code>(возможно уже пофикшено)</code>", parse_mode='HTML')
    elif text == 'Информация о боте':
        bot.send_message(message.chat.id, "Этот бот использует весь функционал <b>SPapi</b>.\nАвтор бота: <b>@karilaa</b>\n", parse_mode= 'HTML')
    elif text == 'Проверка онлайна по списку':
        bot.send_message(message.chat.id, u'Команда "<b>Проверить кто онлайн</b>" позволяет проверять онлайн людей которых вы добавите в список.<code>\nЕсли человек поменяет ник, то в боте он автоматически изменится</code>.\n1. Вам надо добавить ник, для этого перейдите в раздел "Настройки"\n2. Чтобы проверить онлайн людей которых вы добавили, нажмите на кнопку или напишите команду /check\n', parse_mode='HTML')
    elif text == 'Раздел "Настройки"':
        bot.send_message(message.chat.id, '<b>В этом разделе вы можете:</b>\n- Добавить ник в список для проверки.\n- Удалить ВСЕ ники из списка', parse_mode= 'HTML')
    elif text == 'Раздел "Разное"':
        bot.send_message(message.chat.id, '<b>В этом разделе вы можете:</b>\n- Проверить онлайн ли человек на сервере.\n- Скачать скин по нику', parse_mode= 'HTML')
    elif text == 'Разное' or text == '/razn':
        bot.send_message(message.chat.id, "Переход в разное", reply_markup=keyboardRazn)
    elif text == 'Настройки' or text == '/options':
        bot.send_message(message.chat.id, "Переход в настройки", reply_markup=keyboardOpt)
def skin_req(message):
    if message.text != 'Назад':
        chatlog = str(f'<code>{message.chat.id}</code> @{str(message.chat.username)} {str(message.chat.first_name)} {str(message.chat.last_name)}')
        try:
            userJson = json.loads(requests.get(f'https://api.mojang.com/users/profiles/minecraft/{message.text}').text)
            skinBase64 = json.loads(requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{userJson["id"]}').text)["properties"][0]["value"]
            skin = json.loads(b64decode(skinBase64))
            url = skin["textures"]["SKIN"]["url"]
            with open(f'skins/{skin["profileName"]}.png', 'wb') as f:
                f.write(requests.get(url).content)
            sendskin = open(f'skins/{userJson["name"]}.png', 'rb')
            bot.send_document(message.chat.id, sendskin, reply_markup=keyboardRazn)
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка, проверьте правильность написания ника', reply_markup=keyboardRazn)
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил скин {message.text}', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
def nick_check(message):
    if message.text != 'Назад':
        chatlog = str(f'<code>{message.chat.id}</code> @{str(message.chat.username)} {str(message.chat.first_name)} {str(message.chat.last_name)}')
        try:
            req = json.loads(requests.get(f'https://api.mojang.com/users/profiles/minecraft/{message.text}').text)
            text_result = f'{req["name"]} <b>Офлайн</b>'
            if spmapi.check.nick(message.text) == True:
                text_result = f'{req["name"]} <b>Онлайн</b>'
            bot.send_message(message.chat.id, text_result, parse_mode= 'HTML', reply_markup=keyboardRazn)
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка, проверьте правильность написания ника', reply_markup=keyboardRazn)
        try:
            bot.send_message(log_channel, f'{chatlog},\nЗапросил ник {message.text}', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
def add_nick(message):
    if message.text != 'Назад':
        chatlog = str(f'<code>{message.chat.id}</code> @{str(message.chat.username)} {str(message.chat.first_name)} {str(message.chat.last_name)}')
        try:
            nameReq = json.loads(requests.get(f'https://api.mojang.com/users/profiles/minecraft/{message.text}').text)
            nick = nameReq["name"]
            uuidTemp = nameReq["id"]
            uuid = str(f'{uuidTemp[:8]}-{uuidTemp[8:12]}-{uuidTemp[12:16]}-{uuidTemp[16:20]}-{uuidTemp[20:]}')
            open(f'profiles/{message.chat.id}.txt', "a+").write(f'{uuid}\n')
            bot.send_message(message.chat.id, f'Игрок <b>{nick}</b> добавлен', parse_mode= 'HTML', reply_markup=keyboardOpt)
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка, проверьте правильность написания ника', reply_markup=keyboardOpt)
        try:
            bot.send_message(log_channel, f'{chatlog},\nДобавил ник {nick}', parse_mode= 'HTML')
        except:
            print('Ошибка при отправке сообщения в чат')
bot.polling(none_stop=True)