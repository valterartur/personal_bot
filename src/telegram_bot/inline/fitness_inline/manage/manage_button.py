from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def button(update: Update, context: CallbackContext, query) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Categories", callback_data='categories'),
            # InlineKeyboardButton("Exercises", callback_data='exercises'),
            InlineKeyboardButton("Back", callback_data='fitness'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)

