from src.models.gpt import (
    GPTAudit,
    GPTToken,
    GPTModel,
    GPTConversation,
)
from src.repository._base import BaseRepository


class GPTTokenRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=GPTToken, session=session)


class GPTAuditRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=GPTAudit, session=session)


class GPTModelRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=GPTModel, session=session)


class GPTConversationRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=GPTConversation, session=session)

