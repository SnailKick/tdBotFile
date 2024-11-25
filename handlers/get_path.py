from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import NETWORK_FOLDER

async def get_path(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in context.bot_data['ALLOWED_USERS']:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    network_folder = context.user_data.get('network_folder', NETWORK_FOLDER)
    await update.message.reply_text(f'Текущий путь для загрузки файлов: {network_folder}')

handler = CommandHandler('getpath', get_path)