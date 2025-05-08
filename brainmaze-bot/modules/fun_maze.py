from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modules.language_selector import get_translation, get_user_language

async def start_maze_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    context.user_data['maze_step'] = 0
    steps = [
        {"text": translations['maze_start'], "options": [translations['left'], translations['right']]},
        {"text": translations['maze_trap'], "options": [translations['retry']]},
        {"text": translations['maze_treasure'], "options": [translations['restart']]},
    ]
    current_step = steps[0]
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"maze_{i}") for i, opt in enumerate(current_step['options'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(current_step['text'], reply_markup=reply_markup)

async def handle_maze_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    choice = int(query.data.split('_')[1])
    steps = [
        {"text": translations['maze_start'], "options": [translations['left'], translations['right']]},
        {"text": translations['maze_trap'], "options": [translations['retry']]},
        {"text": translations['maze_treasure'], "options": [translations['restart']]},
    ]
    if context.user_data['maze_step'] == 0:
        context.user_data['maze_step'] = 2 if choice == 1 else 1
    else:
        context.user_data['maze_step'] = 0
    current_step = steps[context.user_data['maze_step']]
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"maze_{i}") for i, opt in enumerate(current_step['options'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(current_step['text'], reply_markup=reply_markup)