from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, CallbackContext
from src.models import User
from src.lib import db_session
from src.repository import Repository


class MiddlewareCommandHandler(CommandHandler):
    def __init__(self, command, callback, **kwargs):
        super().__init__(command, callback, **kwargs)

    def handle_update(self, update: Update, dispatcher, check_result: object, context: CallbackContext = None):
        with db_session() as session:
            user_repo = Repository(User, session)
            user = user_repo.get(name=update.effective_user.username)
            print(f'User: {user}')
            print(self.command)
            if not user and 'register' not in self.command:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Please register first. Use /register command")
                return
            elif not user.is_active and 'register' not in self.command:
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

            # Post-processing

    def check_permissions(self, orm_user: User):
        return True
