from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext
from src.models import User
from src.lib import db_session
from src.repository import Repository




class MiddlewareCallbackQueryHandler(CallbackQueryHandler):
    def __init__(self, callback, **kwargs):
        super().__init__(callback, **kwargs)

    def handle_update(self, update: Update, dispatcher, check_result: object, context: CallbackContext = None):
        with db_session() as session:
            user_repo = Repository(User, session)
            user = user_repo.get(name=update.effective_user.username)
            if not user:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Please register first. Use /register command")
                return
            elif not user.is_active:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Your account is not active. Please contact admin.")
                return

            context.user_data['orm_user'] = user
            context.user_data['session'] = session

            return super().handle_update(
                update=update,
                dispatcher=dispatcher,
                check_result=check_result,
                context=context,
            )
