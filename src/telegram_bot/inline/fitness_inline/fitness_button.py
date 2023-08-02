from telegram import Update
from telegram.ext import CallbackContext

from src.telegram_bot.inline.fitness_inline import train, manage


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'fitness':
        from src.telegram_bot.cmd import fitness_command
        fitness_command(update, context)
    elif query.data == 'train':
        train.button(update, context, query)
    elif query.data == 'manage_fitness':
        manage.button(update, context, query)
    elif query.data == 'categories':
        manage.categories.button(update, context, query)
    elif query.data == 'create_category':
        manage.categories.create_category.button(update, context)
    elif query.data == 'delete_category':
        manage.categories.delete_category.button(update, context, query)
    elif query.data.startswith('delete_category:'):
        manage.categories.delete_category.handle(update, context, query)
        manage.categories.delete_category.button(update, context, query)
    elif query.data == 'update_category':
        manage.categories.update_category.button(update, context, query)
        manage.categories.button(update, context, query)
    elif query.data == 'upload_data':
        train.upload_data.button(update, context)
    elif query.data.startswith('upload_data:'):
        train.upload_data.category.button(update, context)
    elif query.data == 'get_data':
        train.get_data.button(update, context, query)
    elif query.data.startswith('get_data:'):
        train.get_data.category.button(update, context, query)
