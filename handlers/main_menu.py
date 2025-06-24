# handlers/main_menu.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import MainKeyboard

class MainMenuHandler:
    def __init__(self):
        pass
    
    async def handle_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت منوی اصلی"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "main_menu":
            keyboard = MainKeyboard.get_main_menu()
            await query.edit_message_text(
                "📋 منوی اصلی:",
                reply_markup=keyboard
            )
        elif query.data == "main_back":
            keyboard = MainKeyboard.get_main_menu()
            await query.edit_message_text(
                "🏠 بازگشت به منوی اصلی:",
                reply_markup=keyboard
            )
