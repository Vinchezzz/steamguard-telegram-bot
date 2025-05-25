import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from account_manager import AccountManager
from handlers import start, get_code_handler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # Account manager initializing
    account_manager = AccountManager('data/accounts.json')
    
    # Application building
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # 
    application.bot_data['account_manager'] = account_manager
    
    # Command define
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("code", get_code_handler))
    
    # Bot start
    application.run_polling()

if __name__ == '__main__':
    main()