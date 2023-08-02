import os
import traceback
import requests
from telegram import Update, InputFile
from telegram.ext import CallbackContext, ConversationHandler

from src.api import gpt
from src.models import GPTConversation
from src.telegram_bot.common import conversation_utils


@conversation_utils.conversation_try_except
@gpt.validate_token
def handle(update: Update, context: CallbackContext):
    try:
        model_info = context.user_data.pop("model")
        model = gpt.get_model(context=context, model=model_info["model"], type=model_info["type"])
        images_number = context.user_data.pop("images_number")
        response = gpt.generate_image(context, prompt=update.message.text, number=images_number)
        conversation = gpt.start_conversation(context)
        for idx, data in enumerate(response.data):
            image_path = gpt.store_image(context, update, data["url"])
            gpt.audit_action(
                context=context,
                conversation=conversation,
                model=model,
                prompt=update.message.text,
                response=image_path,
                billing=model.cost,
            )
            with open(image_path, 'rb') as img:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=InputFile(img)
                )
        conversation = gpt.end_conversation(
            context=context,
            conversation=conversation,
            deactivate=True,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Total cost: {conversation.total_billing}$"
        )
    except:
        update.message.reply_text(f"Error: {traceback.format_exc()}")
    finally:
        return ConversationHandler.END
