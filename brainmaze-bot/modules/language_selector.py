from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("Urdu", callback_data='lang_ur')],
        [InlineKeyboardButton("Hindi", callback_data='lang_hi')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Apni zaban select karein:", reply_markup=reply_markup)

def get_translation(lang: str) -> dict:
    with open('assets/translations.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
    return translations.get(lang, translations['en'])