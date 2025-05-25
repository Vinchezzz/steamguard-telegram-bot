from telegram import Update
from telegram.ext import ContextTypes
from config import ALLOWED_USERS
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in ALLOWED_USERS:
        logger.warning(f"Access denied for {chat_id}")
        return
    
    await update.message.reply_text(
        "Welcome! Use /code <account_id> to receive code"
    )

async def get_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in ALLOWED_USERS:
        return
    
    if not context.args:
        await update.message.reply_text("Enter account login")
        return
    
    account_id = context.args[0]
    try:
        code = context.bot_data['account_manager'].get_code(account_id)
        await update.message.reply_text(f"Code for {account_id}: {code}")
    except ValueError as e:
        logger.error(e)
        await update.message.reply_text(str(e))