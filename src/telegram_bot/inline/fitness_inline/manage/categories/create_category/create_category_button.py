from telegram import Update
from telegram.ext import CallbackContext

from src.telegram_bot.common import ConversationState



def button(update: Update, context: CallbackContext) -> ConversationState:
    query = update.callback_query
    query.message.reply_text(text="Please send category name")
    return ConversationState.CREATE_CATEGORY

