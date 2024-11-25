from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in context.bot_data['ALLOWED_USERS']:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту. Используйте /request для отправки запроса.')
        return

    reply_keyboard = [['/start', '/setpath', '/getpath']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Отправь мне файл, и я сохраню его в сетевую папку.', reply_markup=markup)

handler = CommandHandler('start', start)