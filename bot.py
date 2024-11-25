from telegram.ext import Application
from config import TOKEN, ALLOWED_USERS, ADMINS, REQUESTS, SET_PATH, NETWORK_FOLDER, logger, config, save_config
from handlers import start, request_access, admin_commands, set_path, get_path, save_file, save_photo, save_video

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Инициализация данных бота
    application.bot_data['ALLOWED_USERS'] = ALLOWED_USERS
    application.bot_data['ADMINS'] = ADMINS
    application.bot_data['REQUESTS'] = REQUESTS
    application.bot_data['SET_PATH'] = SET_PATH
    application.bot_data['NETWORK_FOLDER'] = NETWORK_FOLDER

    application.add_handler(start)
    application.add_handler(request_access)
    application.add_handler(admin_commands[0])  # approve_handler
    application.add_handler(admin_commands[1])  # reject_handler
    application.add_handler(set_path)
    application.add_handler(get_path)
    application.add_handler(save_file)
    application.add_handler(save_photo)
    application.add_handler(save_video)

    logger.info('Бот запущен')
    application.run_polling()

if __name__ == '__main__':
    main()