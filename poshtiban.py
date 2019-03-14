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
import random
import os
from django.conf import settings
from django.apps import apps
import similarity

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

print(BotConfig.bot_token)
bot = Bot(token=BotConfig.bot_token,  # "1239525175:e523a3ce66aae472c159d110ca4a24541f129a51",
              base_url=BotConfig.base_url,  # "https://tapi.bale.ai/",
              base_file_url="https://tapi.bale.ai/file/")
updater = Updater(bot=bot)

dp = updater.dispatcher

from support.models import QA, Pepole

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger()

MMENUE, MOTADAVEL, RECOM, SEND = range(4)

supp = "پشتیبانی و رفع مشکل"
ques = "سوالات متداول"
tecn = "لیست متخصصین"



def start(bot, update):
    # reply_keyboard = [['سوالات متداول', 'پشتیبانی و رفع مشکل']]
    reply_keyboard = [[supp, ques, tecn]]
    logger.info("شروع بات")
    update.message.reply_text(
        'لطفا ابتدا «سوالات متداول» را مطالعه فرمایید. در این بخش پرتکرار‌ترین سوالات به صورت کامل پاسخ داده شده‌اند.' +
        'در صورتی که پاسخ به سوال خود را در این بخش نیافتید و یا در فرایند ثبت‌نام خود با مشکل مواجه هستید، «درخواست پشتیبانی» را انتخاب نمایید.'
        ,
        reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return MMENUE


def mainmenue(bot, update):
    logger.info("main menue")
    user = update.message.from_user
    logger.info("main menue  %s: %s", user.first_name, update.message.text)
    update.message.reply_text('سوال خود را وارد کنید.')
    return RECOM


def recommendation(bot, update):
    logger.info("recommendation")
    reply_keyboard = [[]]
    faq = list(QA.objects.all().values_list('title'))

    candidate_questions = []
    for l in faq:
        candidate_questions.append(l[0])

    update_question = update.message.text
    dp.user_data['question']=update.message.text
    similar_questions = similarity.get_top_similarity(update_question, candidate_questions, 2)
    if len(similar_questions) != 0:
        print('similar_questions:', similar_questions)
        reply_keyboard[0] = similar_questions
        reply_keyboard[0].append('خیر')
        reply_keyboard[0].append("بازگشت")
        user = update.message.from_user
        logger.info("main menue  %s: %s", user.first_name, update.message.text)
        update.message.reply_text('آیا سوال شما شبیه یکی از موارد هست؟ روی آن کلیک کنید',

                                  reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
        return MOTADAVEL
    else:
        # print("not similar")
        # return SEND
        sendsend(bot, update)


def sendsend(bot, update):
    list1 = list(Pepole.objects.filter(user_type=2).values_list('user_id'))
    tecnic_id = random.choice(list1)

    print(tecnic_id)
    bot.send_message(chat_id=tecnic_id[0], text=dp.user_data['question'])

    update.message.reply_text('به کارشناس ارسال شد')


def tecnic(bot, update):
    logger.info("tecnic")
    reply_keyboard = [[]]
    list1 = list(Pepole.objects.all().values_list('last_name'))
    print(list1)
    for l in list1:
        print(l[0])
        reply_keyboard[0].append(l[0])

    reply_keyboard[0].append("بازگشت")
    reply_keyboard[0].append("بازگشت به منو قبل")
    update.message.reply_text('یکی از متخصصین را انتخاب کنید',
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return MOTADAVEL


def motadavel(bot, update):
    logger.info("متداول")
    reply_keyboard = [[]]
    list1 = list(QA.objects.all().values_list('title'))
    for l in list1:
        reply_keyboard[0].append(l[0])

    user = update.message.from_user
    logger.info("سولات متداول  %s: %s", user.first_name, update.message.text)

    update.message.reply_text('یکی از موارد زیر را انتخاب کنید.',
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return MMENUE




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
    pass


if __name__ == '__main__':
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MMENUE: [RegexHandler(pattern='^({})$'.format(supp), callback=mainmenue),
                     RegexHandler(pattern='^({})$'.format(ques), callback=motadavel),
                     RegexHandler(pattern='^({})$'.format(tecn), callback=tecnic)],

            MOTADAVEL: [RegexHandler(pattern='^(aa)$', callback=motadavel),
                        RegexHandler(pattern='^({})$'.format('خیر'), callback=sendsend)],

            RECOM: [MessageHandler(Filters.text, recommendation)],

            SEND: [MessageHandler(Filters.text, sendsend)],

        },

        fallbacks=[RegexHandler(pattern='^({})$'.format('بازگشت'), callback=start)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # dispatcher.add_error_handler(error)
    # dispatcher.add_handler(conv_handler)

    updater.start_polling(poll_interval=1)
    updater.idle()
    run()
