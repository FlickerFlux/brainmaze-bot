from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
from modules.language_selector import get_translation, get_user_language

async def start_mystery_adventure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    riddles = [
        {"question": translations['riddle_1'], "answer": 0, "options": [translations['riddle_1_opt1'], translations['riddle_1_opt2']]},
    ]
    context.user_data['current_riddle'] = random.choice(riddles)
    riddle = context.user_data['current_riddle']
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"riddle_{i}") for i, opt in enumerate(riddle['options'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        f"{translations['mystery_start']}\n\n{riddle['question']}", reply_markup=reply_markup
    )

async def handle_riddle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    riddle = context.user_data.get('current_riddle')
    selected = int(query.data.split('_')[1])
    if selected == riddle['answer']:
        text = translations['riddle_correct']
    else:
        text = translations['riddle_wrong']
    keyboard = [[InlineKeyboardButton(translations['next_riddle'], callback_data='mystery_adventure')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)