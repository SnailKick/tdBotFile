from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils import notify_admins

async def request_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    if user_id in context.bot_data['ALLOWED_USERS']:
        await update.message.reply_text('У вас уже есть доступ к этому боту.')
        return

    if user_id in context.bot_data['REQUESTS']:
        await update.message.reply_text('Ваш запрос уже отправлен и ожидает рассмотрения.')
        return

    context.bot_data['REQUESTS'][user_id] = user_name
    await update.message.reply_text('Ваш запрос на доступ отправлен. Ожидайте одобрения администратором.')
    await notify_admins(context, f'Получен новый запрос на доступ от пользователя {user_name} (ID: {user_id}). Используйте /approve {user_id}, чтобы одобрить или /reject {user_id}, чтобы отклонить.')

handler = CommandHandler('request', request_access)