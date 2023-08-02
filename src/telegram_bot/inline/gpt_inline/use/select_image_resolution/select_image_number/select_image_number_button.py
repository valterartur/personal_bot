from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.api import gpt
from src.telegram_bot.common import ConversationState


def button(update: Update, context: CallbackContext) -> ConversationState:
    query = update.callback_query
    resolution = query.data.strip()
    context.user_data['model'] = {
        'model': "image",
        'type': resolution,
    }
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("Cancel", callback_data='gpt_command'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)
    return ConversationState.ACCEPT_IMAGE_DESCRIPTION
