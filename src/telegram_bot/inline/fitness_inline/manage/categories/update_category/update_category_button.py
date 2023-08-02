from telegram import Update
from telegram.ext import CallbackContext


def button(update: Update, context: CallbackContext, query) -> None:
    query.message.reply_text("Not implemented yet")
    # with db_session() as session:
    #     repo = Repository(User, session)
    #     user = repo.get(name=update.effective_user.username)
    #     keyboard = [
    #         [
    #             InlineKeyboardButton(category.display_name, callback_data=f"edit_category:{category.name}")
    #             for category in user.categories
    #         ]
    #     ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # query.message.reply_markup(reply_markup)
