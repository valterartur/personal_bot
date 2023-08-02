from telegram import Update
from telegram.ext import CallbackContext

from src.models import User, Category
from src.repository import Repository
from src.lib import db_session


def handle(update: Update, context: CallbackContext, query) -> None:
    category_name = query.data.split(':')[1]
    with db_session() as session:
        repo = Repository(User, session)
        user = repo.get(name=update.effective_user.username)
        repo = Repository(Category, session)
        repo.delete(name=category_name.lower().replace(' ', '_'), user_id=user.id)
    query.message.reply_text(text=f"Deleted category {category_name}")
