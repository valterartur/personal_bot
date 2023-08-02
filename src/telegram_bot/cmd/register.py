from telegram import Update
from telegram.ext import CallbackContext
from src.models import User
from src.repository import Repository
from src.lib import db_session


def register_command(update: Update, context: CallbackContext) -> None:
    """Register user for personalization."""
    try:
        with db_session() as session:
            user = update.message.from_user
            username = user.username

            repo = Repository(User, session)
            orm_user = repo.get(name=username)
            if orm_user and orm_user.is_active is True:
                update.message.reply_text(f"User {username} is already registered!")
                return
            elif orm_user and orm_user.is_active is False:
                update.message.reply_text(f"User {username} already registered, but not active. Please contact admin.")
                return

            last_name = f' {user.last_name}' if user.last_name else ''
            display_name = f'{user.first_name}{last_name}'
            repo.save(name=username, display_name=display_name)

        reply = f"User {display_name} successfully was place in queue for approve. Please contact admin."
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")
