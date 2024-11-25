from telegram import Update, Video
from telegram.ext import MessageHandler, filters, ContextTypes
from utils.helpers import sanitize_filename
import os
import datetime

async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in context.bot_data['ALLOWED_USERS']:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    video: Video = update.message.video
    file = await video.get_file()
    file_name = f"{video.file_unique_id}.mp4"
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    network_folder = context.user_data.get('network_folder', context.bot_data['NETWORK_FOLDER'])

    current_time = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M')
    folder_name = f"{current_time}-{user_name}"
    sanitized_folder_name = sanitize_filename(folder_name)
    folder_path = os.path.join(network_folder, sanitized_folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, file_name)
    await file.download_to_drive(file_path)

    folder_link = f"Ссылка на папку: file://{folder_path}\nПапка создана: {current_time}"
    await update.message.reply_text(folder_link)

handler = MessageHandler(filters.VIDEO, save_video)