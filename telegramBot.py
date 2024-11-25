import os
import datetime
import logging
import re
from telegram import Update, ReplyKeyboardMarkup, PhotoSize, Video
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Путь к сетевой папке по умолчанию
NETWORK_FOLDER = 'w:/Pomoika/сообщения тг бота/'

# Токен вашего бота
TOKEN = '7960500201:AAHvJswbgjeAuB2cOE5kCWAojNKsICwVqe0'

# Состояния для ConversationHandler
SET_PATH = 1

# Список разрешенных пользователей
ALLOWED_USERS = [1268380400, 1549629525]  # Замените на реальные ID пользователей

def sanitize_filename(filename):
    # Заменяем недопустимые символы на подчеркивание
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

async def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    reply_keyboard = [['/start', '/setpath', '/getpath']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Отправь мне файл, и я сохраню его в сетевую папку.', reply_markup=markup)

async def set_path(update: Update, context: CallbackContext) -> int:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return ConversationHandler.END

    await update.message.reply_text('Пожалуйста, отправьте новый путь для загрузки файлов.')
    return SET_PATH

async def save_path(update: Update, context: CallbackContext) -> int:
    new_path = update.message.text
    if not os.path.isdir(new_path):
        await update.message.reply_text('Указанный путь не существует или не является директорией.')
        return SET_PATH

    context.user_data['network_folder'] = new_path
    await update.message.reply_text(f'Путь для загрузки файлов изменен на: {new_path}')
    return ConversationHandler.END

async def get_path(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    network_folder = context.user_data.get('network_folder', NETWORK_FOLDER)
    await update.message.reply_text(f'Текущий путь для загрузки файлов: {network_folder}')

async def save_file(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    # Используем путь из контекста, если он есть, иначе используем путь по умолчанию
    network_folder = context.user_data.get('network_folder', NETWORK_FOLDER)

    # Создаем папку с названием Дата-время-от-кого
    current_time = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M')
    folder_name = f"{current_time}-{user_name}"
    sanitized_folder_name = sanitize_filename(folder_name)
    folder_path = os.path.join(network_folder, sanitized_folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Сохраняем файл в папку
    file_path = os.path.join(folder_path, file_name)
    await file.download_to_drive(file_path)

    # Возвращаем ссылку на папку с указанием времени создания
    folder_link = f"Ссылка на папку: file://{folder_path}\nПапка создана: {current_time}"
    await update.message.reply_text(folder_link)

async def save_photo(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    # Получаем наибольший размер фотографии
    photo: PhotoSize = update.message.photo[-1]
    file = await photo.get_file()
    file_name = f"{photo.file_unique_id}.jpg"
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    # Используем путь из контекста, если он есть, иначе используем путь по умолчанию
    network_folder = context.user_data.get('network_folder', NETWORK_FOLDER)

    # Создаем папку с названием Дата-время-от-кого
    current_time = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M')
    folder_name = f"{current_time}-{user_name}"
    sanitized_folder_name = sanitize_filename(folder_name)
    folder_path = os.path.join(network_folder, sanitized_folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Сохраняем фотографию в папку
    file_path = os.path.join(folder_path, file_name)
    await file.download_to_drive(file_path)

    # Возвращаем ссылку на папку с указанием времени создания
    folder_link = f"Ссылка на папку: file://{folder_path}\nПапка создана: {current_time}"
    await update.message.reply_text(folder_link)

async def save_video(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return

    video: Video = update.message.video
    file = await video.get_file()
    file_name = f"{video.file_unique_id}.mp4"
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    # Используем путь из контекста, если он есть, иначе используем путь по умолчанию
    network_folder = context.user_data.get('network_folder', NETWORK_FOLDER)

    # Создаем папку с названием Дата-время-от-кого
    current_time = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M')
    folder_name = f"{current_time}-{user_name}"
    sanitized_folder_name = sanitize_filename(folder_name)
    folder_path = os.path.join(network_folder, sanitized_folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Сохраняем видео в папку
    file_path = os.path.join(folder_path, file_name)
    await file.download_to_drive(file_path)

    # Возвращаем ссылку на папку с указанием времени создания
    folder_link = f"Ссылка на папку: file://{folder_path}\nПапка создана: {current_time}"
    await update.message.reply_text(folder_link)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setpath', set_path)],
        states={
            SET_PATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_path)]
        },
        fallbacks=[]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("getpath", get_path))
    application.add_handler(MessageHandler(filters.Document.ALL, save_file))
    application.add_handler(MessageHandler(filters.PHOTO, save_photo))
    application.add_handler(MessageHandler(filters.VIDEO, save_video))

    application.run_polling()

if __name__ == '__main__':
    main()