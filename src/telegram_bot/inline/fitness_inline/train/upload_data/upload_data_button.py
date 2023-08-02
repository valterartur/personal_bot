from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.lib import db_session
from src.models import User
from src.repository import Repository


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    with db_session() as session:
        repo = Repository(User, session)
        user = repo.get(name=update.effective_user.username)

        keyboard = [
            [
                InlineKeyboardButton(category.display_name, callback_data=f"upload_data:{category.name}")
                for category in user.categories
            ] + [
                InlineKeyboardButton("Back", callback_data=f"train"),
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text(text="Please select a category:", reply_markup=reply_markup)

