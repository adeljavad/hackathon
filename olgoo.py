from db_handler import *
from utils import deftext
from utils.connections import *
from utils.utils import *

START_TIME_STEP, END_TIME_STEP, MAXIMUM_POSTS_STEP, PERIOD_TAG_STEP, CONFIRMATION_STEP, GET_POST_STEP, GET_PERIOD_TAG = range(
    7)


def admin_restricted(func):
    def restricted_function(*args, **kwds):
        update = kwds.get('update')
        if not update:
            update = args[1]
        if update and str(get_user_peer(update)) in config.root_admins:
            return func(*args, **kwds)

    return restricted_function


def conversation_starter(bot, update):
    user_id = get_user_peer(update)
    if str(user_id) in config.root_admins:
        reply_keyboard = [[deftext.post_management, deftext.add_post, deftext.ads_management]]
        reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
        update.message.reply_text(deftext.welcome, reply_markup=reply_markup)
    return ConversationHandler.END


@admin_restricted
def post_management(bot, update):
    reply_keyboard = [[deftext.time_management, deftext.post_numbers_management]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.post_management_info, reply_markup=reply_markup)
    return ConversationHandler.END


@admin_restricted
def ask_post_time_management(bot, update):
    reply_keyboard = [[deftext.back]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.ask_post_time_management_start, reply_markup=reply_markup)
    return START_TIME_STEP


@admin_restricted
def get_period_start(bot, update):
    start_time = update.message.text
    start_time = arabic_to_eng_number(start_time)
    hour, minuet = start_time.split(":")
    if not (0 <= int(hour) < 24 and 0 <= int(minuet) < 60):
        reply_keyboard = [[deftext.back]]
        reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
        update.message.reply_text(deftext.bad_time, reply_markup=reply_markup)
        return START_TIME_STEP

    dispatcher.user_data["start_time"] = start_time
    reply_keyboard = [[deftext.back]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.ask_post_time_management_end, reply_markup=reply_markup)
    return END_TIME_STEP


def bad_input(bot, update):
    reply_keyboard = [[deftext.back]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.bad_input, reply_markup=reply_markup)
    return ConversationHandler.END


@admin_restricted
def get_period_end(bot, update):
    end_time = update.message.text
    end_time = arabic_to_eng_number(end_time)
    hour, minuet = end_time.split(":")
    if not (0 <= int(hour) < 24 and 0 <= int(minuet) < 60):
        reply_keyboard = [[deftext.back]]
        reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
        update.message.reply_text(deftext.bad_time, reply_markup=reply_markup)
        return END_TIME_STEP

    start_time = dispatcher.user_data["start_time"]

    if datetime.datetime.strptime(start_time, "%H:%M") >= datetime.datetime.strptime(end_time, "%H:%M"):
        reply_keyboard = [[deftext.back]]
        reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
        update.message.reply_text(deftext.bad_start_end, reply_markup=reply_markup)
        return ConversationHandler.END

    dispatcher.user_data["end_time"] = end_time
    reply_keyboard = [[deftext.back]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.ask_maximum_posts, reply_markup=reply_markup)
    return MAXIMUM_POSTS_STEP


def get_maximum_post(bot, update):
    number_of_posts = update.message.text
    number_of_posts = arabic_to_eng_number(number_of_posts)
    dispatcher.user_data["max_post"] = number_of_posts

    reply_keyboard = [[deftext.back, deftext.no_tag_is_required]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.ask_tag, reply_markup=reply_markup)
    return PERIOD_TAG_STEP


def get_period_tag(bot, update):
    tag = update.message.text
    dispatcher.user_data["tag"] = tag
    return ask_confirmation(bot, update)


def no_tag_is_required(bot, update):
    dispatcher.user_data["tag"] = ""
    return ask_confirmation(bot, update)


def ask_confirmation(bot, update):
    number_of_posts = dispatcher.user_data["max_post"]
    start_time = dispatcher.user_data["start_time"]
    end_time = dispatcher.user_data["end_time"]
    tag = dispatcher.user_data["tag"]
    reply_keyboard = [[deftext.confirm, deftext.reject]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.period_info.format(tag=tag,
                                                         start=start_time,
                                                         end=end_time,
                                                         posts=number_of_posts), reply_markup=reply_markup)
    return CONFIRMATION_STEP


def data_confirmed(bot, update):
    record_period_data()
    reply_keyboard = [[deftext.back]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.success_set_time, reply_markup=reply_markup)
    return ConversationHandler.END


def record_period_data():
    maximum_posts = dispatcher.user_data["max_post"]
    start_time = dispatcher.user_data["start_time"]
    end_time = dispatcher.user_data["end_time"]
    tag = dispatcher.user_data["tag"]
    set_period(start_time, end_time, maximum_posts, tag)
    return ConversationHandler.END


@admin_restricted
def ask_for_posts(bot, update):
    periods = get_periods()
    reply_keyboard = []
    if periods is None or len(periods) == 1:
        message = deftext.wait_for_post
    else:
        message = deftext.ask_period
        for period in periods:
            btn = period.tag if period.tag.strip() else "{} الی {}".format(period.start, period.end)
            reply_keyboard.append(btn)

    reply_keyboard.append(deftext.back)
    reply_keyboard = [reply_keyboard]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)
    return GET_PERIOD_TAG


def get_tag(bot, update):
    tag = update.message.text
    period = get_period_by_tag(tag)
    if not period and "الی" in tag:
        user_input = tag.split("الی")
        start = user_input[0].strip()
        end = user_input[1].strip()
        period = get_period_by_start_end(start, end)

    if period:
        dispatcher.user_data["selected_tag"] = period.id
    else:
        dispatcher.user_data["selected_tag"] = 1
        get_user_posts(bot, update)
        return ConversationHandler.END

    reply_keyboard = [[deftext.back]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.wait_for_post, reply_markup=reply_markup)
    return ConversationHandler.END


@admin_restricted
def ads_management(bot, update):
    reply_keyboard = [[deftext.register_card_number, deftext.set_ad_price, deftext.set_ad_time]]
    reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
    update.message.reply_text(deftext.ad_management_info, reply_markup=reply_markup)
    return ConversationHandler.END


@admin_restricted
def get_user_posts(bot, update):
    post = update.message.to_dict()
    period_id = dispatcher.user_data["selected_tag"] or 1
    if post.get("text"):
        insert_message(post.get("text"), caption=None, message_type=config.PostTypes.text_message,
                       post_period=period_id)
    elif post.get("photo"):
        insert_message(str(post.get("photo")[0].get("file_id")), caption=post.get("caption"),
                       message_type=config.PostTypes.photo_message, post_period=period_id)
    elif post.get("video"):
        insert_message(str(post.get("video").get("file_id")), caption=post.get("caption"),
                       message_type=config.PostTypes.video_message, post_period=period_id)
    elif post.get("voice"):
        insert_message(str(post.get("voice").get("file_id")), caption=post.get("caption"),
                       message_type=config.PostTypes.voice_message, post_period=period_id)
    elif post.get("document"):
        insert_message(str(post.get("document").get("file_id")), caption=post.get("caption"),
                       message_type=config.PostTypes.document_message, post_period=period_id)


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, update.message)


def loop_check_time(*a):
    periods = get_periods()
    duration = 60
    if periods:
        for period in periods:
            if datetime.datetime.strptime("{} {}".format(datetime.date.today(), period.start),
                                          "%Y-%m-%d %H:%M") <= datetime.datetime.now() <= datetime.datetime.strptime(
                    "{} {}".format(datetime.date.today(), period.end), "%Y-%m-%d %H:%M"):
                if period.maximum_posts >= get_number_of_sent_messages(period.start, period.end):
                    next_post = get_next_message(period.id)
                    if next_post:
                        send_next_message(next_post)

                duration = (datetime.datetime.strptime(period.end, "%H:%M") - datetime.datetime.strptime(period.start,
                                                                                                         "%H:%M")).seconds / period.maximum_posts
                if datetime.datetime.now() + datetime.timedelta(seconds=duration) > datetime.datetime.strptime(
                        "{} {}".format(datetime.date.today(), period.end), "%Y-%m-%d %H:%M"):
                    duration = (datetime.datetime.strptime("{} {}".format(datetime.date.today(), period.end),
                                                           "%Y-%m-%d %H:%M") - datetime.datetime.now()).seconds

    else:
        next_post = get_next_message()
        if next_post:
            send_next_message(next_post)
    updater.job_queue.run_once(loop_check_time, duration)


def send_next_message(next_post):
    if next_post.post_type == config.PostTypes.text_message:
        bot.send_message(config.channel_address, next_post.content)
    elif next_post.post_type == config.PostTypes.photo_message:
        bot.send_photo(config.channel_address, next_post.content, caption=next_post.caption)
    elif next_post.post_type == config.PostTypes.video_message:
        bot.send_video(config.channel_address, next_post.content, caption=next_post.caption)
    elif next_post.post_type == config.PostTypes.document_message:
        bot.send_document(config.channel_address, next_post.content, caption=next_post.caption)
    elif next_post.post_type == config.PostTypes.voice_message:
        bot.send_voice(config.channel_address, next_post.content, caption=next_post.caption)
    return


if __name__ == "__main__":
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', conversation_starter),
                      RegexHandler("^({})$".format(deftext.back), conversation_starter),
                      RegexHandler("^({})$".format(deftext.post_management), post_management),
                      RegexHandler("^({})$".format(deftext.ads_management), ads_management),
                      RegexHandler("^({})$".format(deftext.time_management), ask_post_time_management),
                      RegexHandler("^({})$".format(deftext.add_post), ask_for_posts),
                      MessageHandler(Filters.all, get_user_posts)
                      ],

        states={
            START_TIME_STEP: [RegexHandler(pattern="^\d{2}:\d{2}$", callback=get_period_start),
                              RegexHandler(pattern="^({})$".format(deftext.back), callback=conversation_starter),
                              MessageHandler(Filters.all, bad_input)
                              ],

            END_TIME_STEP: [RegexHandler(pattern="^\d{2}:\d{2}$", callback=get_period_end),
                            RegexHandler(pattern="^({})$".format(deftext.back), callback=conversation_starter),
                            MessageHandler(Filters.all, bad_input)
                            ],

            MAXIMUM_POSTS_STEP: [RegexHandler(pattern="^\d*$", callback=get_maximum_post),
                                 RegexHandler(pattern="^({})$".format(deftext.back), callback=conversation_starter),
                                 MessageHandler(Filters.all, bad_input)
                                 ],

            PERIOD_TAG_STEP: [MessageHandler(Filters.text, callback=get_period_tag),
                              RegexHandler(pattern="^({})$".format(deftext.back), callback=conversation_starter),
                              MessageHandler(Filters.all, bad_input)
                              ],

            CONFIRMATION_STEP: [RegexHandler("^({})$".format(deftext.confirm), data_confirmed),
                                RegexHandler("^({})$".format(deftext.reject), conversation_starter),
                                MessageHandler(Filters.all, bad_input)
                                ],

            GET_PERIOD_TAG: [MessageHandler(Filters.text, get_tag),
                             RegexHandler(pattern="^({})$".format(deftext.back), callback=conversation_starter),
                             MessageHandler(Filters.all, bad_input)
                             ]

        },

        fallbacks=[RegexHandler(deftext.back, conversation_starter)]
    )

    dispatcher.add_error_handler(error)
    dispatcher.add_handler(conv_handler)
    loop_check_time()
    run()
