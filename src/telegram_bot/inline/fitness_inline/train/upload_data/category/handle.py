from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from src.lib import db_session
from src.models import User
from src.repository import Repository
from src.lib.bot_utils import BotUtils
from src.lib.file_parser import FileParser
from src.lib.evaluation import handle_df


def handle(update: Update, context: CallbackContext) -> int:
    try:
        bot = BotUtils(update, context)
        category_name = context.user_data.pop('category_name')
        user = update.effective_user.username
        with db_session() as session:
            repo = Repository(User, session)
            user = repo.get(name=user)
            path = bot.save_data_to_file(category=category_name, text=update.message.text)
            df = FileParser.parse(file_path=path, bot=bot)
            df['category'] = category_name
            handle_df(df=df, user=user, session=session)
        bot.move_data_file_to_processed(category=category_name)
        update.message.reply_text('Data was processed')
    except Exception as e:
        update.message.reply_text(f'Error: {e}')
    finally:
        return ConversationHandler.END
