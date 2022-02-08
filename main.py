import requests
import settings
import datetime
from telegram.ext import Updater, CallbackContext, CommandHandler, Dispatcher, \
    CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.update import Update
from googletrans import Translator

translater = Translator()

updater = Updater(token=settings.API_TOKEN)
dispatcher: Dispatcher = updater.dispatcher

CITY_STATE = 0

keyboard = [
    [InlineKeyboardButton("Toshkent", callback_data="toshkent"),
     InlineKeyboardButton("Andijon", callback_data="andijon")],
    [InlineKeyboardButton("Buxoro", callback_data="buxoro"), InlineKeyboardButton("Xorazm", callback_data="khiva")],
    [InlineKeyboardButton("Surxondaryo", callback_data="shakhrisabz"),
     InlineKeyboardButton("Navoiy", callback_data="navoiy")],
    [InlineKeyboardButton("Samarqand", callback_data="samarqand"),
     InlineKeyboardButton("Qashqadaryo", callback_data="qashqadaryo")],
    [InlineKeyboardButton("Qoraqalpog'iston", callback_data="qoraqalpoq"),
     InlineKeyboardButton("Jizzax", callback_data="jizzax")],
    [InlineKeyboardButton("Farg'ona", callback_data="farg'ona"),
     InlineKeyboardButton("Namangan", callback_data="namangan")]
]

back = [
    [InlineKeyboardButton("⬅️Ortga", callback_data="back")]
]

boshlash = [
    [InlineKeyboardButton("✅ Boshlash", callback_data="start")]
]


def start(update: Update, context: CallbackContext):
    update.message.reply_text(f"Assalomu alaykum, {update.message.from_user.first_name}\n \nBotni ishga tushirish uchun"
                              f' "✅ Boshlash" tugmasini bosing',
                              reply_markup=InlineKeyboardMarkup(boshlash))


def back_(query):
    query.answer()
    query.edit_message_text("Kerakli shaharni tanlang 👇", reply_markup=InlineKeyboardMarkup(keyboard))


def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data != "back" and query.data != "start":
        try:
            City = query.data
            url = f'http://api.openweathermap.org/data/2.5/weather?q={City}&appid={settings.API_KEY}&units=metric'
            res = requests.get(url)
            data = res.json()
            city = translater.translate(data['name'], 'uz').text
            quyosh_chiqishi = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            quyosh_botishi = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            kun_davomiyligi = datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
                              datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            ob_havo = data['weather'][0]['main']
            if ob_havo in settings.code_smiles_uz:
                wd = settings.code_smiles_uz[ob_havo]
            else:
                wd = f"{ob_havo}"
            query.edit_message_text(
                f"🌇<b>Shahar:</b> \t{city}\n☂<b>Joriy ob-havo:</b> \t{temp} ℃ \t{wd}\n💨<b>Shamol tezligi:</b> \t{wind_speed} m/s\n🌔<B>Quyosh chiqishi:</b> \t{quyosh_chiqishi}\n🌘<b>Quyosh botishi:</b> {quyosh_botishi}\n🌍<b>Kun davomiyligi:</b> \t{kun_davomiyligi}\n<u>Kuningiz xayrli o`tsin</u>",
                parse_mode="HTML", reply_markup=InlineKeyboardMarkup(back)
            )
        except Exception as e:
            print(e)
    elif query.data == "back":
        back_(query)
    elif query.data == "start":
        query.answer()
        query.edit_message_text("Quyidagi shaharlardan birini tanlang 👇",
                                reply_markup=InlineKeyboardMarkup(keyboard))
    return CITY_STATE


def all_(update: Update, context: CallbackContext):
    update.message.reply_text("Noma'lum buyruq!")


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CITY_STATE: [
            dispatcher.add_handler(CallbackQueryHandler(callback_handler))
        ]
    },
    fallbacks=[CommandHandler('start', start)]
)

dispatcher.add_handler(conv_handler)

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
