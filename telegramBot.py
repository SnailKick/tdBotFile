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

# Список администраторов
ADMINS = [1268380400]  # Замените на реальные ID администраторов

# Список запросов на доступ
REQUESTS = {}

def sanitize_filename(filename):
    # Заменяем недопустимые символы на подчеркивание
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

async def notify_admins(context: CallbackContext, message: str):
    for admin_id in ADMINS:
        await context.bot.send_message(chat_id=admin_id, text=message)

async def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту. Используйте /request для отправки запроса.')
        return

    reply_keyboard = [['/start', '/setpath', '/getpath']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Отправь мне файл, и я сохраню его в сетевую папку.', reply_markup=markup)

async def request_access(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    if user_id in ALLOWED_USERS:
        await update.message.reply_text('У вас уже есть доступ к этому боту.')
        return

    if user_id in REQUESTS:
        await update.message.reply_text('Ваш запрос уже отправлен и ожидает рассмотрения.')
        return

    REQUESTS[user_id] = user_name
    await update.message.reply_text('Ваш запрос на доступ отправлен. Ожидайте одобрения администратором.')
    await notify_admins(context, f'Получен новый запрос на доступ от пользователя {user_name} (ID: {user_id}). Используйте /approve {user_id}, чтобы одобрить или /reject {user_id}, чтобы отклонить.')

async def approve_request(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ADMINS:
        await update.message.reply_text('Извините, у вас нет доступа к этой команде.')
        return

    if len(context.args) == 0:
        await update.message.reply_text('Использование: /approve <user_id>')
        return

    user_id = int(context.args[0])
    if user_id not in REQUESTS:
        await update.message.reply_text('Запрос от этого пользователя не найден.')
        return

    ALLOWED_USERS.append(user_id)
    user_name = REQUESTS[user_id]
    del REQUESTS[user_id]
    await update.message.reply_text(f'Доступ пользователю {user_name} (ID: {user_id}) одобрен.')
    await context.bot.send_message(chat_id=user_id, text='Ваш запрос на доступ к боту одобрен.')
    logger.info(f'Доступ пользователю {user_name} (ID: {user_id}) одобрен. ALLOWED_USERS: {ALLOWED_USERS}')

async def reject_request(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ADMINS:
        await update.message.reply_text('Извините, у вас нет доступа к этой команде.')
        return

    if len(context.args) == 0:
        await update.message.reply_text('Использование: /reject <user_id>')
        return

    user_id = int(context.args[0])
    if user_id not in REQUESTS:
        await update.message.reply_text('Запрос от этого пользователя не найден.')
        return

    user_name = REQUESTS[user_id]
    del REQUESTS[user_id]
    await update.message.reply_text(f'Запрос от пользователя {user_name} (ID: {user_id}) отклонен.')
    await context.bot.send_message(chat_id=user_id, text='Ваш запрос на доступ к боту отклонен.')
    logger.info(f'Запрос от пользователя {user_name} (ID: {user_id}) отклонен.')

async def set_path(update: Update, context: CallbackContext) -> int:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return ConversationHandler.END

    await update.message.reply_text('Пожалуйста, отправьте новый путь для загрузки файлов.')
    return SET_PATH

async def save_path(update: Update, context: CallbackContext) -> int:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text('Извините, у вас нет доступа к этому боту.')
        return SET_PATH

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
    application.add_handler(CommandHandler("request", request_access))
    application.add_handler(CommandHandler("approve", approve_request))
    application.add_handler(CommandHandler("reject", reject_request))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("getpath", get_path))
    application.add_handler(MessageHandler(filters.Document.ALL, save_file))
    application.add_handler(MessageHandler(filters.PHOTO, save_photo))
    application.add_handler(MessageHandler(filters.VIDEO, save_video))

    application.run_polling()

if __name__ == '__main__':
    main()