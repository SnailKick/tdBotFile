import re
from telegram.ext import ContextTypes

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

async def notify_admins(context: ContextTypes.DEFAULT_TYPE, message: str):
    for admin_id in context.bot_data['ADMINS']:
        await context.bot.send_message(chat_id=admin_id, text=message)