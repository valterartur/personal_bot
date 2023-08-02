from telegram.ext import ConversationHandler

from src.telegram_bot.common import DynamicConversation


conversation = ConversationHandler(**DynamicConversation(__file__).conversation_body)


