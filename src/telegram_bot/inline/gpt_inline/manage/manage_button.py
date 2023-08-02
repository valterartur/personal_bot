from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def button(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Setup Token", callback_data='setup_token'),
            InlineKeyboardButton("Back", callback_data='gpt_command'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)

