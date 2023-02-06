import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from config import token

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('lGztgN5bdl8NwDg75TiEbD6iYektgvUv', config_dict)
mgr = owm.weather_manager()
bot = telebot.TeleBot('5968347444:AAELkETNU2oma1FMMadxNRdHqlwWJHigqlU')


@bot.message_handler(commands=['start'])
def city(message):
    msg = bot.send_message(message.chat.id, "Пожалуйста, укажите ваш город.")
    bot.register_next_step_handler(msg, send_echo)


def send_echo(message):
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    tempMin = w.temperature('celsius')["temp_min"]
    tempMax = w.temperature('celsius')["temp_max"]
    WindSpeed = w.wind()["speed"]

    answer = "В городе " + message.text + " сейчас " + w.detailed_status
    answer += "\nТемпература на улице, примерно " + str(temp) + " градусов."
    answer += "\nМаксимальная температура " + str(tempMax) + " градусов."
    answer += "\nМинимальная температура " + str(tempMin) + " градусов."
    answer += "\nСкорость ветра " + str(WindSpeed) + " метров в секунду.\n\n"

    if temp < 5:
        answer += "Сейчас довольно холодно, не забудь одеть шапку!"
    elif temp < 20:
        answer += "На улице прохладно, одевайся теплее."
    else:
        answer += "Температура комфортная для прогулки!"

    bot.send_message(message.chat.id, answer)


bot.polling()
