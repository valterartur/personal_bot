from telegram import Update
from telegram.ext import CallbackContext

from src.telegram_bot.common import ConversationState



def button(update: Update, context: CallbackContext) -> ConversationState:
    query = update.callback_query
    category_name = query.data.split(':')[1]
    context.user_data['category_name'] = category_name
    query.message.reply_text(
        "Please send the data to upload. The data should be in the following format:\n"
        "Exercise name, sets, reps, weight separated with a comma\n"
        "If you have multiple sets, reps or weights, separate them with a slash (/).\n"
        "Example:\n"
        "Bench press, 3, 10/10/10, 50/50/50\n"
        "Squat, 3, 10/10/10, 50/50/50\n"
    )
    return ConversationState.UPLOAD_DATA
