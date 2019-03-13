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

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger()

MMENUE, PHOTO, A, BIO = range(4)


def start(bot, update):
    reply_keyboard = [['سوالات متداول', 'پشتیبانی و رفع مشکل']]
    logger.info("شروع بات")
    update.message.reply_text(
        'لطفا ابتدا «سوالات متداول» را مطالعه فرمایید. در این بخش پرتکرار‌ترین سوالات به صورت کامل پاسخ داده شده‌اند.' +
        'در صورتی که پاسخ به سوال خود را در این بخش نیافتید و یا در فرایند ثبت‌نام خود با مشکل مواجه هستید، «درخواست پشتیبانی» را انتخاب نمایید.'
        ,
        reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return MMENUE


def mainmenue(bot, update):
    logger.info("main menue")
    reply_keyboard = [['درباره آزمون', 'شرایط سنی حضور در آزمون']]
    user = update.message.from_user
    logger.info("main menue  %s: %s", user.first_name, update.message.text)
    update.message.reply_text('یکی از موارد زیر را انتخاب کنید.',
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return PHOTO


def photo(bot, update):
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
    bot = Bot(token=BotConfig.bot_token,            #   "1239525175:e523a3ce66aae472c159d110ca4a24541f129a51",
              base_url=BotConfig.base_url ,         #   "https://tapi.bale.ai/",
              base_file_url="https://tapi.bale.ai/file/")
    updater = Updater(bot=bot)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MMENUE: [RegexHandler(pattern='^(سوالات متداول|پشتیبانی و رفع مشکل|Other)$', callback=mainmenue)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('رد کردن', skip_photo)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('انصراف', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling(poll_interval=2)
    updater.idle()


if __name__ == '__main__':
    main()
