import telebot
import random
import requests

key = "any_key"
token = "any_token"
proxy = "any_proxy"

if proxy is not None:
    telebot.apihelper.proxy = {'http': proxy, 'https': proxy}

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет"u'\U0001F9DC\U0001F3FB\U0000200D\U00002640\U0000FE0F')


@bot.message_handler(commands=['weather'])
def send_weather(message):
    mes = "Напиши город, в котором хочешь узнать погоду"u'\U0001F33F'
    f = bot.send_message(message.chat.id, mes)
    bot.register_next_step_handler(f, weather)


def weather(message):
    apikey = "&key=" + key
    url = "https://api.weatherbit.io/v2.0/current?city={}".format(message.text) + apikey
    try:
        smile = ''
        res = requests.get(url)
        data = res.json()
        if 'cloud' in data['data'][0]['weather']['description']:
            smile += u'\U00002601'
        if 'snow' in data['data'][0]['weather']['description']:
            smile += u'\U00002744\U0000FE0F'
        if 'rain' in data['data'][0]['weather']['description']:
            smile += u'\U0001F4A6'
        if 'Clear' in data['data'][0]['weather']['description']:
            smile += u'\U00002600\U0000FE0F'
        temp = str(data['data'][0]['temp']) + smile
        bot.send_message(message.chat.id, temp)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный город"u'\U0001F937\U0000200D\U00002640\U0000FE0F')


@bot.message_handler(content_types=["sticker"])
def echo_sticker(message):
    sti = message.sticker.set_name
    array = bot.get_sticker_set(sti)
    random_sticker = random.choice(array.stickers).file_id
    bot.send_sticker(message.chat.id, random_sticker)

bot.polling()
