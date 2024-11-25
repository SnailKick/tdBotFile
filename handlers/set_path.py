from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Определите константы для состояний
SET_PATH, = range(1)

async def set_path(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.from_user.id not in context.bot_data['ALLOWED_USERS']:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return ConversationHandler.END

    await update.message.reply_text('Пожалуйста, отправьте новый путь для загрузки файлов.')
    return SET_PATH

async def save_path(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.from_user.id not in context.bot_data['ALLOWED_USERS']:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return ConversationHandler.END

    new_path = update.message.text
    if not os.path.isdir(new_path):
        await update.message.reply_text('Указанный путь не существует или не является директорией.')
        return SET_PATH

    context.user_data['network_folder'] = new_path
    await update.message.reply_text(f'Путь для загрузки файлов изменен на: {new_path}')
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('setpath', set_path)],
    states={
        SET_PATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_path)]
    },
    fallbacks=[]
)
