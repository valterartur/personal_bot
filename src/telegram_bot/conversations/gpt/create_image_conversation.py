from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler

from src.telegram_bot.middleware import (
    MiddlewareCommandHandler, MiddlewareCallbackQueryHandler, MiddlewareMessageHandler
)
from src.telegram_bot.common import ConversationState, fallback
from src.telegram_bot.common import DynamicConversation
from functools import partial
from src.telegram_bot import cmd
from src.telegram_bot.inline import gpt_inline


conversation = ConversationHandler(
    entry_points=[
        MiddlewareCommandHandler("gpt_command", cmd.gpt_command),
        MiddlewareCallbackQueryHandler(
            gpt_inline.use.select_image_resolution.button, pattern="select_image_resolution"
        )
    ],
    states={
        ConversationState.ACCEPT_NUMBER_OF_IMAGES: [
            MiddlewareCallbackQueryHandler(gpt_inline.use.select_image_resolution.select_image_number.button),
        ],
        ConversationState.ACCEPT_IMAGE_DESCRIPTION: [
            MiddlewareCallbackQueryHandler(gpt_inline.use.select_image_resolution.select_image_number.create_image.button),
        ],
        ConversationState.CREATE_IMAGE: [
            MiddlewareMessageHandler(Filters.text, gpt_inline.use.select_image_resolution.select_image_number.create_image.handle),
        ],
    },
    fallbacks=[
        MiddlewareCallbackQueryHandler(partial(fallback, button=gpt_inline.use))
    ],
    per_user=True,
)


