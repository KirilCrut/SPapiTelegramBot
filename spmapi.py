#наработки потенциальной библиотеки для спапи
import requests
import json
class chat:
    def chat():
        return json.loads(requests.get('https://sp-api.ru/spm/chat').text)['messages']
    def last():
        return json.loads(requests.get('https://sp-api.ru/spm/chat').text)['messages'][49] 
class world:
#запрос тиков
    def ticks():
        return json.loads(requests.get('https://sp-api.ru/spm/time').text)['ticks']
#запрос времени суток
    def time():
        return json.loads(requests.get('https://sp-api.ru/spm/time').text)['time']
#запрос погоды
    def weather():
        return json.loads(requests.get('https://sp-api.ru/spm/weather').text)['weather']
#вывод времени и погоды
    def all():
        time = json.loads(requests.get('https://sp-api.ru/spm/time').text)
        weather = json.loads(requests.get('https://sp-api.ru/spm/weather').text)
        result = dict(ticks=time['ticks'], time=time['time'], weather=weather['weather'])
        return result
#запрос онлайна
class online:
#максимальный онлайн
    def max():
        return json.loads(requests.get('https://sp-api.ru/spm/online').text)['max'] 
#текуший онлайн(-1 для из-за бага в самом апи)
    def count():
        return json.loads(requests.get('https://sp-api.ru/spm/online').text)['count']-1
#список людей онлайн
    def players():
        players = json.loads(requests.get('https://sp-api.ru/spm/online').text)['players']
        del players[len(players)-1]
        return players
#запрос без изменений
    def all():
        return json.loads(requests.get('https://sp-api.ru/spm/online').text)
#проверка статуса человека
class check:
#по никнейму
    def nick(nickname):
        online = json.loads(requests.get('https://sp-api.ru/spm/online').text)
        result = False
        for number in range(0, online["count"]-1):
            if online["players"][number]["nick"].lower() == nickname.lower():
                result = True
        return result
#по uuid
    def uuid(uuid):
        online = json.loads(requests.get('https://sp-api.ru/spm/online').text)
        result = False
        for number in range(0, online["count"]-1):
            if online["players"][number]["uuid"] == uuid:
                result = True
        return result
