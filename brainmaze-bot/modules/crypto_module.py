from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests
from modules.language_selector import get_translation, get_user_language

async def show_crypto_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    disclaimer = translations['crypto_disclaimer']
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum')
        data = response.json()
        text = f"{disclaimer}\n\n{translations['crypto_prices']}\n"
        for coin in data:
            text += f"{coin['name']}: ${coin['current_price']}\n"
    except:
        text = translations['crypto_error']
    keyboard = [[InlineKeyboardButton(translations['refresh_crypto'], callback_data='crypto_analysis')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)