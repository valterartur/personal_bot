from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.api import gpt


def handle(update: Update, context: CallbackContext):
    gpt.setup_token(context=context, token=update.message.text)
    update.message.reply_text(f"Token for user {update.effective_user.username} has been set")
    return ConversationHandler.END
