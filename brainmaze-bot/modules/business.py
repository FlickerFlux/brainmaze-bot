from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
import random
from modules.language_selector import get_translation, get_user_language

async def show_business_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    with open('data/business_ideas.json', 'r') as f:
        ideas = json.load(f)
    idea = random.choice(ideas)
    text = f"{translations['business_idea']}\n\n{idea['title']}\n{idea['description']}\n\nCategory: {idea['category']}"
    keyboard = [[InlineKeyboardButton(translations['another_idea'], callback_data='business_ideas')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

async def show_business_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    lang = get_user_language(user_id)
    translations = get_translation(lang)
    steps = [
        translations['market_research'],
        translations['investment_breakdown'],
        translations['revenue_model'],
        translations['marketing_strategy'],
        translations['tools_needed'],
    ]
    current_step = context.user_data.get('plan_step', 0)
    text = f"{translations['business_plan']}\n\nStep {current_step + 1}: {steps[current_step]}"
    keyboard = []
    if current_step > 0:
        keyboard.append([InlineKeyboardButton(translations['previous'], callback_data='plan_prev')])
    if current_step < len(steps) - 1:
        keyboard.append([InlineKeyboardButton(translations['next'], callback_data='plan_next')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    if 'plan_prev' in update.callback_query.data and current_step > 0:
        context.user_data['plan_step'] = current_step - 1
    elif 'plan_next' in update.callback_query.data and current_step < len(steps) - 1:
        context.user_data['plan_step'] = current_step + 1