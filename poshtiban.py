# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, Bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger()

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(bot, update):
    reply_keyboard = [['سوالات متداول', 'پشتیبانی و رفع مشکل' ]]
    logger.info("start called")
    update.message.reply_text('لطفا ابتدا «سوالات متداول» را مطالعه فرمایید. در این بخش پرتکرار‌ترین سوالات به صورت کامل پاسخ داده شده‌اند.'+
                              'در صورتی که پاسخ به سوال خود را در این بخش نیافتید و یا در فرایند ثبت‌نام خود با مشکل مواجه هستید، «درخواست پشتیبانی» را انتخاب نمایید.'
        ,
        reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return GENDER


def gender(bot, update):
    logger.info("in gender")
    reply_keyboard = [['درباره آزمون', 'شرایط سنی حضور در آزمون']]
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text( 'یکی از موارد زیر را انتخاب کنید.',
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
    bot = Bot(token="1239525175:e523a3ce66aae472c159d110ca4a24541f129a51",
              base_url="https://tapi.bale.ai/",
              base_file_url="https://tapi.bale.ai/file/")
    updater = Updater(bot=bot)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [RegexHandler(pattern='^(سوالات متداول|پشتیبانی و رفع مشکل|Other)$', callback=gender)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=2)
    # you can replace above line with commented below lines to use webhook instead of polling
    # updater.bot.set_webhook(url="{}{}".format(os.getenv('WEB_HOOK_DOMAIN', "https://testwebhook.bale.ai"),
    #                                           os.getenv('WEB_HOOK_PATH', "/get-upd")))
    # updater.start_webhook(listen=os.getenv('WEB_HOOK_IP', ""), port=int(os.getenv('WEB_HOOK_PORT', "")),
    #                       url_path=os.getenv('WEB_HOOK_PATH', ""))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
