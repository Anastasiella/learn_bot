import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import ephem
from datetime import datetime

logging.basicConfig(filename="bot.log", level=logging.DEBUG)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_NAME, 'password': settings.PROXY_PASSWORD}}

PLANETS = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun', 'Moon', 'Phobos',
           'Deimos', 'Io', 'Europa', 'Ganymede', 'Callisto', 'Mimas', 'Enceladus', 'Tethys', 'Dione', 'Rhea', 'Titan',
           'Hyperion', 'Iapetus', 'Ariel', 'Umbriel', 'Titania', 'Oberon', 'Miranda']


def greet_user(update,context):
    print("Вызван /start")
    update.message.reply_text("Здравствуй, пользователь!")


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def date():
    dt_now = datetime.now()
    return dt_now.strftime('%Y/%m/%d')


def astronomy(update, context):
    my_planet = update.message.text.split(' ')[1].capitalize()
    if my_planet in PLANETS:
        random_planet = getattr(ephem, my_planet)(date())
        stars = ephem.constellation(random_planet)[1]
        update.message.reply_text(f'Сегодня планета {my_planet} в созвездии {stars}')


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    db = mybot.dispatcher
    db.add_handler(CommandHandler("start", greet_user))
    db.add_handler(CommandHandler("planet", astronomy))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стратовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()



