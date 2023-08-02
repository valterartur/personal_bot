from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.telegram_bot.inline import fitness_inline


def fallback(update: Update, context: CallbackContext) -> int:
    if update.message:
        update.message.reply_text('Operation canceled.')
    elif update.callback_query:
        update.callback_query.message.reply_text('Operation canceled.')
    fitness_inline.button(update, context)
    return ConversationHandler.END

