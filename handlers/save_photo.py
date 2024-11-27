from telegram import Update, PhotoSize
from telegram.ext import MessageHandler, filters, ContextTypes
from utils.helpers import sanitize_filename
import os
import datetime

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in context.bot_data['ALLOWED_USERS']:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    photo: PhotoSize = update.message.photo[-1]
    file = await photo.get_file()
    file_name = f"{photo.file_unique_id}.jpg"
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    network_folder = context.user_data.get('network_folder', context.bot_data['NETWORK_FOLDER'])

    # Создаем папку с именем аккаунта пользователя
    user_folder_name = sanitize_filename(user_name)
    user_folder_path = os.path.join(network_folder, user_folder_name)
    os.makedirs(user_folder_path, exist_ok=True)

    # Создаем папку с датой и именем пользователя
    current_time = datetime.datetime.now().strftime('%d.%m.%Y_%H:00')
    folder_name = f"{current_time}-{user_name}"
    sanitized_folder_name = sanitize_filename(folder_name)
    folder_path = os.path.join(user_folder_path, sanitized_folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, file_name)
    await file.download_to_drive(file_path)

    folder_link = f"Ссылка на папку: file://{folder_path}\nПапка создана: {current_time}"
    await update.message.reply_text(folder_link)

handler = MessageHandler(filters.PHOTO, save_photo)