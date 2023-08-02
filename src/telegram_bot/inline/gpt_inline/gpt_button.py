from telegram import Update
from telegram.ext import CallbackContext
from src.telegram_bot.cmd import gpt_command
from . import manage
from . import use


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'gpt_command':
        gpt_command(update, context)
    elif query.data == 'use_gpt':
        use.button(update, context)
    elif query.data == 'gpt':
        query.message.reply_text('Not implemented yet')
    elif query.data == 'gpt4':
        query.message.reply_text('Not implemented yet')
    elif query.data == 'select_image_resolution':
        use.select_image_resolution.button(update, context)
    elif query.data == 'whisper':
        query.message.reply_text('Not implemented yet')
    elif query.data == 'manage_gpt':
        manage.button(update, context)

