from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, CallbackQueryHandler

# توکن ربات تلگرام خود را وارد کنید
TOKEN = "7238431582:AAFgVxhNrh2pcghpajAyfbj-aweTj5jxOJU"

# آیدی ادمین (کسی که پیام‌های کاربران را دریافت می‌کند)
ADMIN_ID = 5353177208

import requests

# توکن ربات تلگرام خود را وارد کنید
token = "7238431582:AAFgVxhNrh2pcghpajAyfbj-aweTj5jxOJU"

# URL پروژه شما در Vercel
webhook_url = "https://telgram-klnyt03to-achilles-projects-12012821.vercel.app/"  # URL پروژه Vercel

# تنظیم Webhook برای ربات تلگرام
set_webhook_url = f"https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}"

# ارسال درخواست برای تنظیم Webhook
response = requests.get(set_webhook_url)

# نمایش نتیجه درخواست (برای بررسی که آیا Webhook به درستی تنظیم شده است یا خیر)
print(response.json())


# ذخیره آیدی کاربرانی که ربات را استارت کرده‌اند
user_ids = set()  # استفاده از set برای ذخیره منحصر به فرد آیدی‌ها

# ذخیره پیام‌های کاربران که منتظر پاسخ ادمین هستند
user_messages = {}

# ذخیره زبان کاربر
user_languages = {}

# دیکشنری‌های زبان
LANGUAGES = {
    "en": {
        "start": "Hello, how can I assist you today?",
        "help": "Hello! I'm a support bot. Here are some features you can use:\n\n/start: Start the bot\n/help: Get help with the bot\nSend a message to admin: Send a message to the admin\nSend media: Send images, videos, files, etc.",
        "language": "Your language has been changed to English.",
        "error": "An error occurred. Please try again later."
    },
    "fa": {
        "start": "سلام، چطور می‌توانم به شما کمک کنم؟",
        "help": "سلام! من یک ربات پشتیبان هستم. اینجا برخی از ویژگی‌هایی که می‌توانید از آنها استفاده کنید:\n\n/start: استارت ربات\n/help: دریافت کمک\nارسال پیام به ادمین: ارسال پیام به ادمین\nارسال رسانه: ارسال عکس، ویدیو، فایل و غیره",
        "language": "زبان شما به فارسی تغییر کرد.",
        "error": "یک خطا رخ داده است. لطفاً بعداً دوباره امتحان کنید."
    }
}

# دستور /start
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_ids.add(user_id)  # اضافه کردن کاربر به لیست

    # بررسی زبان کاربر
    language_code = user_languages.get(user_id, "fa")  # پیش‌فرض فارسی است

    if user_id == ADMIN_ID:
        # نمایش پیام خاص برای ادمین
        await update.message.reply_text(
                 "سلام ایلیای عزیز، وقتتون بخیر باشه🌹\n\n"
            "امروز چه کاری می تونم براتون انجام بدم؟\n\n"
            "/status - وضعیت افرادی که ربات را استارت کرده اند\n"
            "/sendmessage (user ID) - ارسال پیام به یک شخص خاص\n"
            "/broadcast - ارسال پیام همگانی"
        )
    else:
        # دکمه‌ها برای کاربران
        keyboard = [
            [InlineKeyboardButton("ثبت تیکت", callback_data='create_ticket')]  # دکمه "ثبت تیکت" اضافه شد
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "سلام ☺️\nچطور می‌توانم به شما کمک کنم؟\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=reply_markup
        )

# دستور /help
async def help(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # بررسی زبان کاربر
    language_code = user_languages.get(user_id, "fa")  # پیش‌فرض فارسی است

    await update.message.reply_text(LANGUAGES[language_code]["help"])

# دستور تغییر زبان به انگلیسی
async def change_language_en(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # ذخیره زبان انگلیسی برای کاربر
    user_languages[user_id] = "en"
    await update.message.reply_text(LANGUAGES["en"]["language"])

# دستور تغییر زبان به فارسی
async def change_language_fa(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # ذخیره زبان فارسی برای کاربر
    user_languages[user_id] = "fa"
    await update.message.reply_text(LANGUAGES["fa"]["language"])

# دستور /message برای ارسال پیام از طرف ادمین به کاربر
async def admin_message(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:  # بررسی اینکه آیا فرستنده پیام ادمین است
        # بررسی پارامترهای پیام /message
        if len(context.args) < 2:
            await update.message.reply_text("Please provide both user ID and message.\nFormat: /message <user_id> <message>")
            return

        user_id = context.args[0]  # آیدی کاربری که پیام به آن ارسال می‌شود
        message = " ".join(context.args[1:])  # پیام ادمین به کاربر

        # ارسال پیام به کاربر هدف
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            await update.message.reply_text(f"Your message has been sent to user {user_id}.")
        except Exception as e:
            await update.message.reply_text(f"Error sending message to user: {e}")
            # ارسال پیام خطا به ادمین
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"Error occurred while sending message to user {user_id}: {e}")
    else:
        await update.message.reply_text("You don't have permission to send messages.")

# دستور /status برای نمایش تعداد کاربران و آیدی‌ها
async def status(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:  # بررسی اینکه آیا فرستنده پیام ادمین است
        num_users = len(user_ids)  # تعداد کاربران استارت‌کننده ربات
        user_ids_list = "\n".join([str(user_id) for user_id in user_ids])  # تبدیل آیدی‌ها به رشته برای نمایش

        if num_users == 0:
            await update.message.reply_text("هیچ کاربری ربات را استارت نکرده است.")
        else:
            await update.message.reply_text(
                f"تعداد کاربرانی که ربات را استارت کرده‌اند: {num_users}\n\n"
                f"آیدی‌های کاربران:\n{user_ids_list}"
            )
    else:
        await update.message.reply_text("شما دسترسی به این دستور را ندارید.")

# دریافت پیام از کاربر و ارسال به ادمین
async def user_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_message = update.message.text  # دریافت متن پیام کاربر

    # بررسی زبان کاربر
    language_code = user_languages.get(user_id, "fa")  # پیش‌فرض فارسی است

    try:
        # ارسال پیام متنی به ادمین
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Message from user {user_id} ({update.message.from_user.full_name}):\n\n{user_message}")

        # ذخیره پیام در لیست پیام‌ها برای پاسخ دادن به آن
        user_messages[user_id] = user_message

        # ارسال تایید به کاربر
        await update.message.reply_text(LANGUAGES[language_code]["start"])

    except Exception as e:
        # ارسال پیام خطا به کاربر در صورت بروز مشکل
        await update.message.reply_text(LANGUAGES[language_code]["error"])
        # ارسال پیام خطا به ادمین
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Error occurred while processing message from user {user_id}: {e}")

# بررسی و ارسال انواع پیام‌ها (عکس، ویدیو، گیف، ویس، فایل)
async def handle_media(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_message = ""
    media_type = None

    try:
        # بررسی اینکه آیا پیام عکس است
        if update.message.photo:
            media_type = "PHOTO"
            file_id = update.message.photo[-1].file_id  # بزرگترین اندازه عکس
            user_message = update.message.caption if update.message.caption else ""

        # بررسی اینکه آیا پیام ویدیو است
        elif update.message.video:
            media_type = "VIDEO"
            file_id = update.message.video.file_id
            user_message = update.message.caption if update.message.caption else ""

        # بررسی اینکه آیا پیام گیف است
        elif update.message.animation:
            media_type = "GIF"
            file_id = update.message.animation.file_id
            user_message = update.message.caption if update.message.caption else ""

        # بررسی اینکه آیا پیام ویس است
        elif update.message.voice:
            media_type = "VOICE"
            file_id = update.message.voice.file_id
            user_message = update.message.caption if update.message.caption else ""

        # بررسی اینکه آیا پیام فایل است
        elif update.message.document:
            media_type = "DOCUMENT"
            file_id = update.message.document.file_id
            user_message = update.message.caption if update.message.caption else ""

        if media_type:
            # ارسال رسانه به ادمین
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"{media_type} from user {user_id} ({update.message.from_user.full_name}):\n\n{user_message}"
            )

            # ارسال فایل یا رسانه به ادمین بسته به نوع آن
            if media_type == "PHOTO":
                await context.bot.send_photo(chat_id=ADMIN_ID, photo=file_id, caption=user_message)
            elif media_type == "VIDEO":
                await context.bot.send_video(chat_id=ADMIN_ID, video=file_id, caption=user_message)
            elif media_type == "GIF":
                await context.bot.send_animation(chat_id=ADMIN_ID, animation=file_id, caption=user_message)
            elif media_type == "VOICE":
                await context.bot.send_voice(chat_id=ADMIN_ID, voice=file_id, caption=user_message)
            elif media_type == "DOCUMENT":
                await context.bot.send_document(chat_id=ADMIN_ID, document=file_id, caption=user_message)

            # ارسال تایید به کاربر
            await update.message.reply_text("Your message has been recorded. Please wait for a response.")
    except Exception as e:
        # ارسال پیام خطا به کاربر در صورت بروز مشکل
        await update.message.reply_text(LANGUAGES["fa"]["error"])
        # ارسال پیام خطا به ادمین
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Error occurred while handling media from user {user_id}: {e}")

# تابع برای مدیریت ثبت تیکت
async def create_ticket(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id

    # بررسی زبان کاربر
    language_code = user_languages.get(user_id, "fa")  # پیش‌فرض فارسی است

    # درخواست پیام برای ثبت تیکت
    await update.callback_query.message.edit_text(
        "لطفاً پیام خود را برای ثبت تیکت ارسال کنید.\n\nبعد از ارسال پیام، ادمین آن را بررسی خواهد کرد."
    )

    # ذخیره وضعیت کاربر به عنوان "در حال ثبت تیکت"
    user_messages[user_id] = "creating_ticket"  # نشان‌دهنده این است که کاربر در حال ثبت تیکت است

    # ارسال پیام تایید به کاربر
    await update.callback_query.answer()

# دریافت پیام از کاربر برای ثبت تیکت
async def user_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_message = update.message.text  # دریافت متن پیام کاربر

    # بررسی زبان کاربر
    language_code = user_languages.get(user_id, "fa")  # پیش‌فرض فارسی است

    if user_id in user_messages and user_messages[user_id] == "creating_ticket":
        # ارسال پیام تیکت به ادمین
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"تیکت جدید از کاربر {user_id} ({update.message.from_user.full_name}):\n\n{user_message}")
            # پس از ارسال تیکت، وضعیت کاربر را بازنشانی می‌کنیم
            user_messages[user_id] = "ticket_created"

            # ارسال تایید به کاربر
            await update.message.reply_text("تیکت شما ثبت شد و به ادمین ارسال گردید. لطفاً منتظر پاسخ باشید.")
        except Exception as e:
            # ارسال پیام خطا به کاربر در صورت بروز مشکل
            await update.message.reply_text(LANGUAGES[language_code]["error"])
            # ارسال پیام خطا به ادمین
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"خطا در ارسال تیکت از کاربر {user_id}: {e}")
    else:
        # در صورتی که کاربر خارج از حالت ثبت تیکت پیامی ارسال کند
        await update.message.reply_text(LANGUAGES[language_code]["start"])

# دستور /broadcast برای ارسال پیام همگانی به تمامی کاربران
async def broadcast_message(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:  # بررسی اینکه آیا فرستنده پیام ادمین است
        if len(context.args) == 0:
            await update.message.reply_text("Please provide the message to send.\nFormat: /broadcast <message>")
            return

        # پیام همگانی که باید ارسال شود
        broadcast_text = " ".join(context.args)

        # ارسال پیام به تمامی کاربران
        num_sent = 0
        errors = []
        for user_id in user_ids:
            try:
                await context.bot.send_message(chat_id=user_id, text=broadcast_text)
                num_sent += 1
            except Exception as e:
                errors.append(f"Failed to send message to {user_id}: {e}")

        # ارسال نتیجه به ادمین
        success_message = f"Message sent to {num_sent} users."
        if errors:
            error_message = "\n".join(errors)
            await update.message.reply_text(f"{success_message}\n\nErrors:\n{error_message}")
        else:
            await update.message.reply_text(success_message)

    else:
        await update.message.reply_text("You don't have permission to use this command.")

# راه‌اندازی ربات
def main():
    # راه‌اندازی اپلیکیشن با توکن ربات
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))  # اضافه کردن دستور /help
    application.add_handler(CommandHandler("message", admin_message))  # اضافه کردن دستور /message برای ادمین
    application.add_handler(CommandHandler("status", status))  # اضافه کردن دستور /status برای ادمین
    application.add_handler(CommandHandler("language_fa", change_language_fa))  # دستور تغییر زبان به فارسی
    application.add_handler(CommandHandler("language_en", change_language_en))  # دستور تغییر زبان به انگلیسی
    application.add_handler(CommandHandler("broadcast", broadcast_message))  # اضافه کردن دستور /broadcast برای ارسال پیام همگانی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message))
    application.add_handler(MessageHandler(filters.ALL, handle_media))  # اینجا برای همه انواع پیام‌ها
    application.add_handler(CallbackQueryHandler(create_ticket, pattern='^create_ticket$'))  # هندلر برای "ثبت تیکت"

    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()
