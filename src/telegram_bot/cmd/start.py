from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import os
from importlib import import_module
from src.models import User
from src.repository import Repository
from src.lib import db_session


def start_command(update: Update, context: CallbackContext) -> None:
    """Press to display interactive menu."""
    cmd_path = os.path.dirname(os.path.abspath(__file__))
    data = []
    for file in os.listdir(cmd_path):
        if file == '__init__.py' or not file.endswith('.py'):
            continue
        module_name = file.replace(".py", "")
        module = import_module(f'src.telegram_bot.cmd.{module_name}')
        metadata = {
            'name': module_name,
            'description': getattr(module, f'{module_name}_command').__doc__,
        }
        data.append(metadata)
    msg = '\n'.join([f'/{m["name"]} - {m["description"]}' for m in data])

    message = update.message or update.callback_query.message
    message.reply_text(msg)
