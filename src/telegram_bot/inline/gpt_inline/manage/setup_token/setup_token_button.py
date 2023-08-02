from telegram import Update
from telegram.ext import CallbackContext

from src.telegram_bot.common import ConversationState



def button(update: Update, context: CallbackContext) -> ConversationState:
    query = update.callback_query
    query.message.reply_text(text="Send OpenAi token here. It will be stored in encrypted form so no-one can read it.")
    return ConversationState.SETUP_TOKEN

