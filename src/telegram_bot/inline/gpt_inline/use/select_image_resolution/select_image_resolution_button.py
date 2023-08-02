from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.telegram_bot.common import ConversationState


def button(update: Update, context: CallbackContext) -> ConversationState:
    keyboard = [
        [
            InlineKeyboardButton("256x256", callback_data='256x256'),
            InlineKeyboardButton("512x512", callback_data='512x512'),
        ],
        [
            InlineKeyboardButton("1024x1024", callback_data='1024x1024'),
            InlineKeyboardButton("Cancel", callback_data='gpt_command'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)
    return ConversationState.ACCEPT_NUMBER_OF_IMAGES
