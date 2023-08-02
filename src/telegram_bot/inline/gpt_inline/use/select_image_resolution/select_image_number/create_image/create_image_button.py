from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.telegram_bot.common import ConversationState
from src.api import gpt


@gpt.validate_token
def button(update: Update, context: CallbackContext) -> ConversationState or int:
    query = update.callback_query
    image_number = query.data
    context.user_data['images_number'] = int(image_number)

    query.message.reply_text(text="Send description of image to generate here.")
    return ConversationState.CREATE_IMAGE
