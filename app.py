import logging

from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

from src.common import Settings
from src.telegram_bot import cmd, inline, conversations
from src.telegram_bot.common import ConversationState
from src.telegram_bot.middleware import MiddlewareCommandHandler, MiddlewareCallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


def cancel(update: Update, context: CallbackContext) -> int:
    if update.message:
        update.message.reply_text('Operation canceled.')
    elif update.callback_query:
        update.callback_query.message.reply_text('Operation canceled.')
    inline.fitness_inline.button(update, context)
    return ConversationHandler.END


def setup_commands(updater: Updater):
    commands = []
    for func in dir(cmd):
        if func.endswith('_command'):
            logging.info(f'Adding command {func}')
            cmd_name = func.replace('_command', '')
            updater.dispatcher.add_handler(MiddlewareCommandHandler(cmd_name, getattr(cmd, func)))
            commands.append((cmd_name, getattr(cmd, func).__doc__))
    updater.bot.set_my_commands(commands)


def setup_conversation(updater: Updater):
    conv_handler = ConversationHandler(
        entry_points=[
            MiddlewareCommandHandler('fitness', cmd.fitness_command),
            CallbackQueryHandler(inline.fitness_inline.manage.categories.create_category.button, pattern='^create_category$')
        ],
        states={
            ConversationState.CREATE_CATEGORY: [
                MessageHandler(Filters.text & ~Filters.command, inline.fitness_inline.manage.categories.create_category.handle)
            ],
        },
        fallbacks=[
            MiddlewareCommandHandler('cancel', cancel),
            CallbackQueryHandler(inline.fitness_inline.manage.categories.create_category.fallback)
        ],
        per_user=True
    )
    updater.dispatcher.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[
            MiddlewareCommandHandler('fitness', cmd.fitness_command),
            CallbackQueryHandler(inline.fitness_inline.train.upload_data.category.button, pattern='^upload_data:.*$')
        ],
        states={
            ConversationState.UPLOAD_DATA: [
                MessageHandler(Filters.text & ~Filters.command, inline.fitness_inline.train.upload_data.category.handle)
            ],
        },
        fallbacks=[
            MiddlewareCommandHandler('cancel', cancel),
            CallbackQueryHandler(inline.fitness_inline.train.upload_data.category.fallback)
        ],
        per_user=True
    )
    updater.dispatcher.add_handler(conv_handler)

    for package in dir(conversations):
        if package.startswith('__'):
            continue
        package = getattr(conversations, package)
        for conversation in dir(package):
            if conversation.endswith('_conversation'):
                logging.info(f'Adding conversation {conversation}')
                updater.dispatcher.add_handler(getattr(package, conversation).conversation)


def setup_menus(updater: Updater):
    updater.dispatcher.add_handler(MiddlewareCallbackQueryHandler(inline.button))


def main() -> None:
    updater = Updater(Settings.TELEGRAM_TOKEN, use_context=True)
    setup_conversation(updater)
    setup_menus(updater)
    setup_commands(updater)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
