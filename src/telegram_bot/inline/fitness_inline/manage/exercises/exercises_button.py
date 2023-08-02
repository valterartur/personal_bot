from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def button(update: Update, context: CallbackContext, query) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Create", callback_data='create_category'),
            InlineKeyboardButton("Delete", callback_data='delete_category'),
            InlineKeyboardButton("Update", callback_data='update_category'),
            InlineKeyboardButton("Back", callback_data='manage_fitness'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)
    else:
        update.message.reply_text(text="Please select an option:", reply_markup=reply_markup)
    # return ConversationState.END
