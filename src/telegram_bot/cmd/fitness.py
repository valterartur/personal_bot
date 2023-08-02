from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.models import User
from src.repository import Repository
from src.lib import db_session


def fitness_command(update: Update, context: CallbackContext) -> None:
    """Fitness manager."""

    keyboard = [
        [
            InlineKeyboardButton("Training", callback_data='train'),
            InlineKeyboardButton("Manage", callback_data='manage_fitness'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message or update.callback_query.message
    message.reply_text('Please choose:', reply_markup=reply_markup)
