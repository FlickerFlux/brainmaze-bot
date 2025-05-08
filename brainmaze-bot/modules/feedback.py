from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
from modules.language_selector import get_translation, get_user_language

async def collect_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    if isinstance(update, Update) and update.message:
        feedback = update.message.text
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        users[str(user_id)]['feedback'] = users[str(user_id)].get('feedback', []) + [feedback]
        with open('data/users.json', 'w') as f:
            json.dump(users, f)
        await update.message.reply_text(translations['feedback_thanks'])
    else:
        keyboard = [[InlineKeyboardButton(translations['rate_bot'], callback_data='rate_bot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(translations['feedback_prompt'], reply_markup=reply_markup)

async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    await query.edit_message_text(translations['feedback_thanks'])