from pydantic_settings import BaseSettings
from cryptography.fernet import Fernet


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str = ''
    GOOGLE_CREDENTIALS: str = ''
    CURRENT_WORKSHEET_PREFIX: str = 'current_'
    SPREADSHEET_ID: str = ''
    FERNET_KEY: str = Fernet.generate_key()


Settings = Settings()
