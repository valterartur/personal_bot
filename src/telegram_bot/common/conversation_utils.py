import os
from functools import partial
from glob import glob
from importlib import import_module

from telegram.ext import MessageHandler, Filters, ConversationHandler

from src.telegram_bot import inline, cmd
from src.telegram_bot.common import ConversationState, fallback
from src.telegram_bot.middleware import MiddlewareCommandHandler, MiddlewareCallbackQueryHandler


class DynamicConversation:
    def __init__(self, file: str):
        self.file = file
        self.__button_module = self.get_conversation_module()

    @property
    def conversation_body(self, **kwargs):
        return {
            'entry_points': [
                MiddlewareCommandHandler(self.command, getattr(cmd, f"{self.command}_command")),
                MiddlewareCallbackQueryHandler(self.button, pattern=self.pattern)
            ],
            'states': {
                getattr(ConversationState, self.pattern.upper()): [
                    MessageHandler(Filters.text & ~Filters.command, self.handle)
                ],
            },
            'fallbacks': [
                MiddlewareCallbackQueryHandler(partial(fallback, button=self.previous_button))
            ],
            'per_user': True,
            **kwargs
        }

    @property
    def pattern(self) -> str:
        return self.get_pattern()

    @property
    def command(self) -> str:
        return self.get_command()

    @property
    def button(self):
        return self.__button_module.button

    @property
    def handle(self):
        return self.__button_module.handle

    @property
    def previous_button(self):
        return self.get_previous_button(self.__button_module)

    def get_pattern(self) -> str:
        return self.file.replace('_conversation.py', '').split('/')[-1]

    def get_command(self) -> str:
        return os.path.dirname(self.file).split('/')[-1]

    def get_conversation_module(self):
        module_inline = getattr(inline, f"{self.get_command()}_inline")
        inline_path = module_inline.__path__[0]
        button_path = glob(f"{inline_path}/**/{self.pattern}_button.py", recursive=True)
        if len(button_path) != 1:
            raise Exception(
                f"Expected to find exactly one button {self.get_pattern()} for command {self.get_command()}, found {len(button_path)}"
            )
        button_path = os.path.dirname(button_path[0])
        button_path = button_path.replace(inline_path, '').strip('/')
        for sub_module in button_path.split('/'):
            module_inline = getattr(module_inline, sub_module)
        return module_inline

    def get_previous_button(self, module):
        previous_module_name = '.'.join(module.__name__.split('.')[:-1])
        previous_module = import_module(previous_module_name)
        return previous_module.button


def conversation_try_except(func):
    def wrapper(update, context, *args, **kwargs):
        try:
            return func(update, context, *args, **kwargs)
        except Exception as e:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Error: {e}"
            )
            return ConversationHandler.END
    return wrapper
