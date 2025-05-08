from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
import random
from modules.language_selector import get_translation, get_user_language

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    
    # Load quizzes
    with open('data/quizzes.json', 'r') as f:
        quizzes = json.load(f)
    
    # Select a random quiz
    quiz = random.choice(quizzes)
    context.user_data['current_quiz'] = quiz
    
    # Create buttons for options
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{i}") for i, opt in enumerate(quiz['options'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send quiz question
    await update.callback_query.edit_message_text(
        f"{translations['quiz']}\n\n{quiz['question']}", reply_markup=reply_markup
    )

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    quiz = context.user_data.get('current_quiz')
    selected = int(query.data.split('_')[1])
    
    # Check if answer is correct
    if selected == quiz['correct']:
        # Update user score
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        if str(user_id) not in users:
            users[str(user_id)] = {'language': lang, 'quiz_scores': {}, 'game_progress': {}, 'module_usage': []}
        users[str(user_id)]['quiz_scores'][quiz['question']] = users[str(user_id)]['quiz_scores'].get(quiz['question'], 0) + 1
        with open('data/users.json', 'w') as f:
            json.dump(users, f)
        text = translations['correct_answer']
    else:
        text = f"{translations['wrong_answer']}\n{translations['correct']}: {quiz['options'][quiz['correct']]}"
    
    # Add button for next quiz
    keyboard = [[InlineKeyboardButton(translations['next_quiz'], callback_data='study_skills')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)