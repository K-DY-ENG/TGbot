from glob import glob
import logging
from random import choice
import sys

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
try:

    #Запись логов
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                                                    level=logging.INFO,
                                                    filename='bot.log'
                                                    )

    #Функция /start
    def greet_user(bot, update, user_data):

        smile = get_user_emoji(user_data)
        user_data['smile'] = smile    
        
        send_text = 'Здравствуйте! Это мой первый телеграмм-бот!{}'.format(smile)
        update.message.reply_text(send_text)

        text = 'Вызван /start'
        logging.info('Вызван /start')

    #Эхо-ответы пользователю
    def talk_to_me(bot, update, user_data):
        smile = get_user_emoji(user_data)

        user_text = ("Привет, {} {}! Ты написал(а): {} ").format (update.message.chat.first_name, 
                                                                    smile, update.message.text)
        
        logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                                               update.message.chat.id, update.message.text)
        
        update.message.reply_text(user_text)

    def main():
            mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
            logging.info('Бот запущен')

            dp = mybot.dispatcher
            dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
            dp.add_handler(CommandHandler("owl", send_owl_picture, pass_user_data=True))
            dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
           
            mybot.start_polling()
            mybot.idle()

    #Отправка изображения из папки пользователю
    def send_owl_picture(bot, update, user_data):
        olw_list = glob('images/owls/owl*.jp*g')
        random_owl = choice(olw_list)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(random_owl, 'rb'))
        logging.info("User: %s, Chat id: %s, Отпралено изображение {}".format(random_owl),
                                     update.message.chat.username, update.message.chat.id)

    #Проверка налиция emoji
    def get_user_emoji(user_data):
        if 'smile' in user_data:
            return user_data['smile']
        else:
            user_data['smile'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
            return user_data['smile']

    main()

except KeyboardInterrupt:
    logging.info("Завершение работы бота")
    sys.exit