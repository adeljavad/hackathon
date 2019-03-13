class Command:
    help = "/help"
    start = "/start"
    menu = "/menu"


class ButtonAction:
    default = 0


class Patterns:
    return_to_main_menu = "^بازگشت به منوی اصلی$"
    description = ""
    address = ""
    phone = "^\d+$"
    add_description = "^ثبت توضیحات$"
    add_address = "^ثبت آدرس$"
    add_phone = "^ثبت شماره تلفن$"
    add_location = "^ثبت موقعیت$"
    info_register = "^ثبت اطلاعات شعب$"
    branch_id_pattern = "^[0-9۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩]*$"


class MimeType:
    image = "image/jpeg"
    csv = "text/csv"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


class BotMessage:
    not_found_contribution = "سابقه‌ای از مشارکت شما در بخش *{}* وجود ندارد!"
    select_from_blow = "یکی از موارد زیر را انتخاب کنید."
    last_description = "آخرین توضیحات ثبت شده توسط شما:\n*{}*"
    last_address = "آخرین آدرس ثبت شده:\n*{}*"
    last_phone = "آخرین تلفن ثبت شده:\n*{}*"
    confirmed_deleted = "باتشکر از مشارکت شما، {} ثبت شده برای شعبه *{} - کد {}* حذف شده است!"
    already_confirmed = "باتشکر از مشارکت شما، {} ثبت شده برای شعبه *{} - کد {}* قبلا توسط شما تایید شده بود!"
    successfully_confirmed = "باتشکر از مشارکت شما، {} ثبت شده برای شعبه *{} - کد {}* تایید شد."
    confirm = "{} ثبت شده برای شعبه *{} - کد {}* صحیح است؟"
    successfully_deleted = "با تشکر از مشارکت شما، {} شعبه *{} - کد {}* حذف شد."
    delete = "از حذف {} مربوط به شعبه *{} - کد {}* اطمینان دارید؟"
    wrong_branch_id = "کد شعبه وارد شده معتبر نیست!\n" \
                      "لطفا *کد شعبه* موردنظر را به صورت یک عدد وارد کنید." + u'🔢'
    ask_branch_id = "لطفا *کد شعبه* موردنظر را به صورت یک عدد وارد کنید." + u'🔢'
    wrong_answer = "جواب نامناسب"
    select_location_id = "شعبه موردنظر خود را انتخاب کنید:"
    full_report_body = "👥افراد فعال: {}   🏦شعب: {}\n⬇تغییرات کل: {}  ❌حذفیات کل: {}\n" \
                       "🗺موقعیت‌ها: {}  ☎تلفن‌ها: {}\n🏦آدرس‌ها:‌ {}     📝توضیحات: {}"
    daily_report_body = "امروز\n👥افراد فعال: {}   🏦شعب: {}\n⬇تغییرات: {}     ❌حذفیات: {}\n" \
                        "🗺موقعیت‌ها: {}  ☎تلفن‌ها: {}\n🏦آدرس‌ها:‌ {}     📝توضیحات: {}"
    upload_failed = "آپلود ناموفق بود"
    daily_report = "گزارش روزانه"
    branch_info_menu = "شعبه *{} - کد {}،*" \
                       " لطفا یکی از موارد زیر را انتخاب کنید."
    branch_menu = "شعبه مورد نظر شما: *{} - کد {}*\n" \
                  "لطفا یکی از گزینه‌های زیر را انتخاب کنید."
    choose_from_menu = "لطفا یکی از گزینه‌های زیر را انتخاب کنید."
    guide_text = "کافی است بعد از وارد کردن کد شعبه مورد نظر، در مرحله‌ی ثبت موقعیت، موقعیت شعبه مورد نظر را با انتخاب" \
                 " دکمه *+* موجود در پایین صفحه و سپس انتخاب گزینه *موقعیت* یا *location* ارسال نمایید."
    successfully_added = "{} شعبه *{} - کد {}* با موفقیت ثبت شد."
    wrong_description = "فرمت صحیح نیست!\n" \
                        "لطفا توضیحات مربوط به شعبه *{} - کد {}،* مانند ساعات کاری،" \
                        " امکانات شعبه، ادغام یا انحلال یا هر نکته‌ای دیگری که به نظرتان ذکر آن ضروری است، وارد نمایید."
    ask_description = "لطفا توضیحات مربوط به شعبه *{} - کد {}،* مانند ساعات کاری،" \
                      " امکانات شعبه، ادغام یا انحلال یا هر نکته‌ای دیگری که به نظرتان ذکر آن ضروری است، وارد نمایید."
    wrong_address = "فرمت صحیح نیست!\n" \
                    "لطفا آدرس شعبه *{} - کد {}* را به صورت کامل به همراه نام شهر، مشابه نمونه‌ی زیر وارد کنید:\n" \
                    "کاشان- …..."
    ask_address = "لطفا آدرس شعبه *{} - کد {}* را به صورت کامل به همراه نام شهر، مشابه نمونه‌ی زیر وارد کنید:\n" \
                  "کاشان- …..."
    wrong_city_code = "*کد شهر* به درستی وارد نشده است!\n" \
                      "لطفا شماره تلفن شعبه *{} - کد {}* را به صورت کامل *همراه با کد شهر،* مشابه نمونه‌ی زیر وارد کنید:\n" \
                      "۰۲۱۸۸۷۶۵۴۳۲"
    wrong_phone_city_code = "دقت داشته باشید که شماره تلفن باید به همراه *کد شهر* وارد شود!\n" \
                            "لطفا شماره تلفن شعبه *{} - کد {}* را به صورت کامل *همراه با کد شهر،* مشابه نمونه‌ی زیر وارد کنید:\n" \
                            "۰۲۱۸۸۷۶۵۴۳۲"
    wrong_phone = "فرمت صحیح نیست!\n" \
                  "لطفا شماره تلفن شعبه *{} - کد {}* را به صورت کامل *همراه با کد شهر،* مشابه نمونه‌ی زیر وارد کنید:\n" \
                  "۰۲۱۸۸۷۶۵۴۳۲"
    ask_phone = "لطفا شماره تلفن شعبه *{} - کد {}* را به صورت کامل به همراه کد شهر، مشابه نمونه‌ی زیر وارد کنید:\n" \
                "۰۲۱۸۸۷۶۵۴۳۲"
    far_away_location = "موقعیت ثبت شده معتبر نیست!\n" \
                        "لطفا *موقعیت* شعبه *{} - کد {}* را" \
                        "به کمک + موجود در پایین صفحه و سپس انتخاب موقعیت ارسال کنید." + u'📌🌍'
    wrong_location = "فرمت صحیح نیست!\n" \
                     "لطفا *موقعیت* شعبه *{} - کد {}* را" \
                     "به کمک + موجود در پایین صفحه و سپس انتخاب موقعیت ارسال کنید." + u'📌🌍'
    ask_location = "لطفا *موقعیت* شعبه *{} - کد {}* را" \
                   "به کمک + موجود در پایین صفحه و سپس انتخاب موقعیت ارسال کنید." + u'📌🌍'
    send_your_new_location = "لطفا *موقعیت* شعبه *{} - کد {}* را مجددا ارسال کنید." + u'📌🌍'
    greeting = "سلام، به بازوی ثبت اطلاعات شعب *بانک ملّی ایران* خوش آمدید." \
               " لطفاً یکی از گزینه‌های زیر را انتخاب کنید."


class ConversationData:
    branch_id = "branch_id"
    location_id = "location_id"
    reg_location = "reg_location"
    name = "name"


class InfoTypes:
    phone_number = "شماره تلفن"
    location = 'موقعیت'
    phone = 'شماره'
    address = 'آدرس'
    description = 'توضیحات'


class ButtonMessage:
    back_contribution = "بازگشت به مشارکت‌ها"
    back_to_branch_menu = "بازگشت به تنظیمات شعبه {}"
    description = "توضیحات"
    address = "آدرس"
    phone = "شماره تلفن"
    location = "موقعیت"
    delete = u'❎' + " حذف "
    confirm = u'✅' + " تایید "
    edit = "ویرایش "
    add_description = "ثبت توضیحات"
    add_address = "ثبت آدرس"
    add_phone = "ثبت شماره تلفن"
    add_location = "ثبت موقعیت"
    contributions = "مشارکت‌های قبلی"
    info_register = "ثبت اطلاعات شعب"
    report = u'📜' + "گزارش"
    yes = u'✅' + "بله"
    return_to_main_menu = "بازگشت به منوی اصلی"
    guide = "راهنما"
    location_register = "ثبت موقعیت"
    location_edit = u'♻️' + "ویرایش موقعیت"


class SendingAttempt:
    first = 1


class Step:
    choose_branch = "choose_branch"
    show_contributions = "show_contributions"
    finish_delete_info = "finish_delete_info"
    finish_confirm_info = "finish_confirm_info"
    finish_add_info = "finish_add_info"
    info_menu = "info_menu"
    branch_info_menu = "branch_info_menu"
    ask_branch_id = "ask_branch_id"
    edit_or_register_loc = "edit_or_register:location"
    edit_or_register = "edit_or_register"
    select_location_id = "select_location_id"
    showing_report = "showing_report"
    upload_fail = "upload_fail"
    finish_and_register = "finish_and_register"
    wrong_location = "wrong_location"
    finish_and_relocate = "finish_and_relocate"
    finish_and_delete = "finish_and_delete"
    delete_location = "delete_location"
    ask_relocate = "ask_relocate"
    select_edit_or_delete = "select_edit_or_delete"
    ask_location = "ask_location"
    location_id_not_same_as_before = "location_id_not_same_as_before"
    location_id_inserted_already = "location_id_inserted_already"
    location_id_not_found = "location_id_not_found"
    wrong_location_id_fomat = "wrong_location_id_fomat"
    ask_location_id = "ask_location_id"
    show_guide = "show_guide"
    showing_menu = "showing_menu"
    conversation_starter = "conversation_starter"


class LogMessage:
    info_confirmed = "info confirmed successfully"
    info_deleted = "info deleted successfully"
    info_added = "info added successfully"
    user_register = "successful user register"
    failed_report_sending = "failed_report_sending"
    successful_report_sending = "successful_report_sending"
    failed_report_upload = "failed report uploading"
    successful_report_upload = "successful report uploading"
    location_deleting = "location deleted successfully"
    location_updating = "successful updating of location"
    location_registering = "successful registering of location"
    successful_sending = "successful sending of message:"
    failed_sending = "failed sending of message:"
    successful_step_message_sending = "successful step message sending"
    failed_step_message_sending = "failure step message sending"


class UserData:
    succedent_message = "succedent_message"
    branch_id = "branch_id"
    record_changes_num = "record_changes_num"
    url = "url"
    file_id = "file_id"
    latitude = "latitude"
    longitude = "longitude"
    location_id = "location_id"
    bot = "bot"
    send_message = "send_message"
    logger = "logger"
    session = "session"
    ask_picture = "ask_picture"
    message_type = "message_type"
    message_id = "message_id"
    sending_set_time = "sending_set_time"
    base_message = "base_message"
    db_msg = "db_msg"
    random_id = "random_id"
    sending_attempt = "sending_attempt"
    kwargs = "kwargs"
    user_id = "user_id"
    user_peer = "user_peer"
    step_name = "step_name"
    message = "message"
    attempt = "attempt"
    report_attempt = "report_attempt"
    doc_message = "doc_message"
    file_url = "file_url"
