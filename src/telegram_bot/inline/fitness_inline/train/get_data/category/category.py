from telegram import Update
from telegram.ext import CallbackContext
from src.lib import db_session
from src.models import User, Category
from src.repository import Repository


def button(update: Update, context: CallbackContext, query) -> None:
    user = update.effective_user.username
    category_name = query.data.split(':')[1]
    with db_session() as session:
        repo = Repository(Category, session)
        category = repo.get(name=category_name)
        repo = Repository(User, session)
        user = repo.get(name=user)
        result_query = user.user_latest_performance(session, category_id=category.id)
        data = []
        for record in result_query.all():
            performance_data, exercise, category = record
            row = [
                exercise.display_name,
                str(performance_data.sets),
                '/'.join(performance_data.reps),
                '/'.join(performance_data.weight),
            ]
            data.append(', '.join(row))
        message = '\n'.join(data)
        if not message:
            message = 'No data found for this category. Make sure you have uploaded your training data.'
        else:
            query.message.reply_text(f'Data for "{category.display_name}" from last training on: {performance_data.timestamp}')
        query.message.reply_text(message)
