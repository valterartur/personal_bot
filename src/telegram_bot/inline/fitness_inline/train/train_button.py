from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def button(update: Update, context: CallbackContext, query) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Upload Data", callback_data='upload_data'),
            InlineKeyboardButton("Get Data", callback_data='get_data'),
            InlineKeyboardButton("Back", callback_data='fitness'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)
