from telegram import Update
from telegram.ext import CallbackContext
from . import fitness_inline
from . import gpt_inline


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    fitness_inline.button(update, context)
    gpt_inline.button(update, context)

