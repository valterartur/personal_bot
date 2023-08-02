from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.models import User
from src.repository import Repository
from src.lib import db_session


def gpt_command(update: Update, context: CallbackContext) -> None:
    """Mobile chat GPT."""
    keyboard = [
        [
            InlineKeyboardButton("Use GPT", callback_data='use_gpt'),
            InlineKeyboardButton("Manage", callback_data='manage_gpt'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message or update.callback_query.message
    message.reply_text('Please choose:', reply_markup=reply_markup)
