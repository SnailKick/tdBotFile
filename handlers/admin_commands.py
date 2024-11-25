from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import config, save_config

async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in config['ADMINS']:
        await update.message.reply_text('Извините, у вас нет доступа к этой команде.')
        return

    if len(context.args) == 0:
        await update.message.reply_text('Использование: /approve <user_id>')
        return

    user_id = int(context.args[0])
    if user_id not in config['REQUESTS']:
        await update.message.reply_text('Запрос от этого пользователя не найден.')
        return

    config['ALLOWED_USERS'].append(user_id)
    user_name = config['REQUESTS'][user_id]
    del config['REQUESTS'][user_id]
    await update.message.reply_text(f'Доступ пользователю {user_name} (ID: {user_id}) одобрен.')
    await context.bot.send_message(chat_id=user_id, text='Ваш запрос на доступ к боту одобрен.')

    # Сохраняем обновленную конфигурацию
    save_config(config)

async def reject_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in config['ADMINS']:
        await update.message.reply_text('Извините, у вас нет доступа к этой команде.')
        return

    if len(context.args) == 0:
        await update.message.reply_text('Использование: /reject <user_id>')
        return

    user_id = int(context.args[0])
    if user_id not in config['REQUESTS']:
        await update.message.reply_text('Запрос от этого пользователя не найден.')
        return

    user_name = config['REQUESTS'][user_id]
    del config['REQUESTS'][user_id]
    await update.message.reply_text(f'Запрос от пользователя {user_name} (ID: {user_id}) отклонен.')
    await context.bot.send_message(chat_id=user_id, text='Ваш запрос на доступ к боту отклонен.')

    # Сохраняем обновленную конфигурацию
    save_config(config)

approve_handler = CommandHandler('approve', approve_request)
reject_handler = CommandHandler('reject', reject_request)