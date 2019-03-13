# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
main algorithm support bot
"""

import logging
from config import BotConfig
from telegram import (ReplyKeyboardMarkup, Bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import os
from django.conf import settings
from django.apps import apps

conf = {
    'INSTALLED_APPS': [
        'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'support',
        ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join('.', 'db.sqlite3'),
        }
    }
}

settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)


from  support.models import QA,Pepole

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger()

MMENUE, MOTADAVEL, BIO = range(3)

supp = "پشتیبانی و رفع مشکل"
ques = "سوالات متداول"
tecn="لیست متخصصین"


def start(bot, update):
    # reply_keyboard = [['سوالات متداول', 'پشتیبانی و رفع مشکل']]
    reply_keyboard = [[supp, ques,tecn]]
    logger.info("شروع بات")
    update.message.reply_text(
        'لطفا ابتدا «سوالات متداول» را مطالعه فرمایید. در این بخش پرتکرار‌ترین سوالات به صورت کامل پاسخ داده شده‌اند.' +
        'در صورتی که پاسخ به سوال خود را در این بخش نیافتید و یا در فرایند ثبت‌نام خود با مشکل مواجه هستید، «درخواست پشتیبانی» را انتخاب نمایید.'
        ,
        reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return MMENUE


def mainmenue(bot, update):
    logger.info("main menue")
    reply_keyboard = [[]]
    list1 = list(QA.objects.all().values_list('title'))
    print(list1)
    for l in list1:
         print(l[0])
         reply_keyboard[0].append( l[0])

    # reply_keyboard = [['درباره آزمون', 'شرایط سنی حضور در آزمون']]
    user = update.message.from_user
    logger.info("main menue  %s: %s", user.first_name, update.message.text)
    update.message.reply_text('یکی از موارد زیر را انتخاب کنید.',
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return MOTADAVEL


def tecnic(bot, update):
    logger.info("tecnic")
    reply_keyboard = [[]]
    list1 = list(Pepole.objects.all().values_list('title'))
    print(list1)
    for l in list1:
         print(l[0])
         reply_keyboard[0].append( l[0])

    # reply_keyboard = [['درباره آزمون', 'شرایط سنی حضور در آزمون']]
    user = update.message.from_user
    logger.info("main menue  %s: %s", user.first_name, update.message.text)
    update.message.reply_text('یکی از موارد زیر را انتخاب کنید.',
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return MOTADAVEL


def motadavel(bot, update):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    logger.info(photo_file)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')
    return bio


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')
    return bio


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, update.message)


def main():
    # Create the Updater and pass it your bot's token.
    print(BotConfig.bot_token)
    bot = Bot(token=BotConfig.bot_token,  # "1239525175:e523a3ce66aae472c159d110ca4a24541f129a51",
              base_url=BotConfig.base_url,  # "https://tapi.bale.ai/",
              base_file_url="https://tapi.bale.ai/file/")
    updater = Updater(bot=bot)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MMENUE: [RegexHandler(pattern='^({})$'.format(supp), callback=mainmenue),
                     RegexHandler(pattern='^({})$'.format(ques), callback=motadavel)
                     RegexHandler(pattern='^({})$'.format(tecn), callback=tecnic)],

            MOTADAVEL: [RegexHandler(pattern='^(aa)$', callback=motadavel),
                        CommandHandler('رد کردن', skip_photo)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('انصراف', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling(poll_interval=5)
    updater.idle()


if __name__ == '__main__':
    main()
