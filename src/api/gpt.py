import os
from contextlib import contextmanager
from datetime import datetime
from typing import Callable

import requests
from sqlalchemy import desc
from telegram.ext import ConversationHandler

from src.common import Constants
from src.lib import OpenAI, BotUtils
from src.models import GPTToken, GPTAudit, GPTConversation, GPTModel
from src.repository import Repository


def validate_token(func) -> Callable:
    def wrapper(update, context, *args, **kwargs):
        user = context.user_data['orm_user']
        if not user.gpt_token:
            context.bot.send_message(
                chat_id=user.telegram_user.chat_id,
                text='You have to set your GPT token first.',
            )
            return ConversationHandler.END
        return func(update, context, *args, **kwargs)
    return wrapper


def setup_token(context, token: str) -> GPTToken:
    token_repo = Repository(GPTToken, context.user_data['session'])
    user = context.user_data['orm_user']
    orm_token = token_repo.get(user_id=user.id)
    data = {
        'user_id': user.id,
        'token': token,
    }
    token_repo.update(orm_token, **data) if orm_token else token_repo.save(**data)
    orm_token = token_repo.get(user_id=user.id)
    return orm_token


def generate_image(context, prompt: str, number: int) -> str:
    user = context.user_data['orm_user']
    openai = OpenAI(user.gpt_token.token)
    return openai.generate_image(prompt=prompt, n=number, size='1024x1024')


def audit_action(
        context,
        conversation: GPTConversation,
        model: GPTModel,
        prompt: str,
        response: str,
        billing: float,
) -> None:
    audit_repo = Repository(GPTAudit, context.user_data['session'])
    if not conversation.messages:
        previous = None
    else:
        previous = audit_repo.get(
            sort=desc(GPTAudit.timestamp),
            conversation_id=conversation.id,
        )
    audit_repo.save(**{
        "model": model,
        "conversation": conversation,
        "prompt": prompt,
        "response": response,
        "billing": billing,
        "previous": previous,
    })


def start_conversation(
    context,
):
    conversation_repo = Repository(GPTConversation, context.user_data['session'])
    conversation_repo.save(**{
        "user_id": context.user_data['orm_user'].id,
        "token_id": context.user_data['orm_user'].gpt_token.id,
    })
    orm_conversation = conversation_repo.get(
        sort=desc(GPTConversation.start),
        user_id=context.user_data['orm_user'].id,
        token_id=context.user_data['orm_user'].gpt_token.id,
    )

    return orm_conversation


def end_conversation(
    context,
    conversation: GPTConversation,
    deactivate: bool = False,
):
    conversation_repo = Repository(GPTConversation, context.user_data['session'])
    billing = sum(message.billing for message in conversation.messages)
    conversation_repo.update(conversation, **{
        "end": datetime.utcnow(),
        "total_billing": billing,
        "active": not deactivate,
    })
    return conversation_repo.get(id=conversation.id)


def store_image(context, update, url: str):
    user = context.user_data['orm_user']
    bot_utils = BotUtils(update, context)
    image_content = requests.get(url).content
    image_path = Constants.MEDIA_PATH.format(
        user=user.name, file=bot_utils.get_message_time(format='%Y_%m_%d_%H_%M_%S') + '.jpg'
    )
    image_dir = os.path.dirname(image_path)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    with open(image_path, "wb") as f:
        f.write(image_content)
    return image_path


def get_model(context, model: str, type: str, input_type: str = None) -> GPTModel:
    model_repo = Repository(GPTModel, context.user_data['session'])
    orm_model = model_repo.get(model=model, model_type=type, input_type=input_type)
    if not orm_model:
        raise Exception(f"Model {model} not found.")
    return orm_model


