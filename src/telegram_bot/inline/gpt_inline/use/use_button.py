from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def button(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("GPT 3.5", callback_data='gpt'),
            InlineKeyboardButton("GPT 4", callback_data='gpt4'),
        ],
        [
            InlineKeyboardButton("Image", callback_data='select_image_resolution'),
            InlineKeyboardButton("Audio", callback_data='whisper'),
        ],
        [
            InlineKeyboardButton("Back", callback_data='gpt_command'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text="Please select an option:", reply_markup=reply_markup)