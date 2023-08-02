from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.lib import db_session
from src.models import User
from src.repository import Repository


def button(update: Update, context: CallbackContext, query) -> None:
    with db_session() as session:
        repo = Repository(User, session)
        user = repo.get(name=update.effective_user.username)
        keyboard = [
            [
                InlineKeyboardButton(category.display_name, callback_data=f"get_data:{category.name}")
                for category in user.categories
            ] + [
                InlineKeyboardButton("Back", callback_data=f"train"),
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)
