from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.telegram_bot.inline.fitness_inline.manage.categories import button as categories_button
from src.telegram_bot.common import ConversationState

from src.models import User, Category
from src.repository import Repository
from src.lib import db_session


def handle(update: Update, context: CallbackContext):
    category_name = update.message.text
    with db_session() as session:
        user_repo = Repository(User, session)
        user = user_repo.get(name=update.effective_user.username)
        category_repo = Repository(Category, session)
        if category_repo.get(name=category_name, user_id=user.id):
            update.message.reply_text(f"Category {category_name} already exists")
            return ConversationState.END
        category_repo.store_from_name(name=category_name, user_id=user.id)
        update.message.reply_text(f'Created category "{category_name}"')
        categories_button(update, context, query=update.callback_query)

    return ConversationHandler.END
