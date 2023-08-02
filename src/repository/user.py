from src.models.user import User, TelegramUser
from src.repository._base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=User, session=session)


class TelegramUserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=User, session=session)
