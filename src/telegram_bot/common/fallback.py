from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from typing import Callable


def fallback(update: Update, context: CallbackContext, button: Callable) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Operation canceled.')
    button(update, context)
    return ConversationHandler.END

