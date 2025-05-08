from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import json
import os
from modules.language_selector import select_language, get_translation
from modules.business import show_business_ideas, show_business_plan
from modules.study_skills import start_quiz
from modules.fun_maze import start_maze_game
from modules.mystery_adventure import start_mystery_adventure
from modules.crypto_module import show_crypto_analysis
from modules.feedback import collect_feedback
from config import API_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    if str(user_id) not in users:
        await select_language(update, context)
    else:
        await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    keyboard = [
        [InlineKeyboardButton(translations['business_ideas'], callback_data='business_ideas')],
        [InlineKeyboardButton(translations['business_plans'], callback_data='business_plans')],
        [InlineKeyboardButton(translations['study_skills'], callback_data='study_skills')],
        [InlineKeyboardButton(translations['fun_maze'], callback_data='fun_maze')],
        [InlineKeyboardButton(translations['mystery_adventure'], callback_data='mystery_adventure')],
        [InlineKeyboardButton(translations['surprise_me'], callback_data='surprise_me')],
        [InlineKeyboardButton(translations['crypto_analysis'], callback_data='crypto_analysis')],
        [InlineKeyboardButton(translations['feedback'], callback_data='feedback')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(translations['welcome_message'], reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'business_ideas':
        await show_business_ideas(query, context)
    elif data == 'business_plans':
        await show_business_plan(query, context)
    elif data == 'study_skills':
        await start_quiz(query, context)
    elif data == 'fun_maze':
        await start_maze_game(query, context)
    elif data == 'mystery_adventure':
        await start_mystery_adventure(query, context)
    elif data == 'crypto_analysis':
        await show_crypto_analysis(query, context)
    elif data == 'feedback':
        await collect_feedback(query, context)
    elif data == 'surprise_me':
        import random
        options = ['business_ideas', 'study_skills', 'fun_maze', 'mystery_adventure', 'crypto_analysis']
        await button_handler(Update(update.update_id, callback_query=query._replace(data=random.choice(options))), context)
    elif data.startswith('lang_'):
        lang = data.split('_')[1]
        user_id = query.from_user.id
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        users[str(user_id)] = {'language': lang, 'quiz_scores': {}, 'game_progress': {}, 'module_usage': []}
        with open('data/users.json', 'w') as f:
            json.dump(users, f)
        await show_main_menu(query, context)

def get_user_language(user_id):
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    return users.get(str(user_id), {}).get('language', 'en')

def main():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_feedback))
    print("Bot shuru ho gaya!")
    application.run_polling()

if __name__ == '__main__':
    main()