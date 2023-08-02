from os import path as opath


class Constants:
    PERFORMANCE_DATA_TABLE = 'performance_data_fact'
    CATEGORIES_TABLE = 'category_dim'
    USERS_TABLE = 'user_dim'
    TELEGRAM_USERS_TABLE = 'telegram_user_dim'
    EXCERSISES_TABLE = 'exercise_dim'
    PERMISSIONS_TABLE = 'permissions'
    USER_PERMISSIONS_TABLE = 'user_permissions'
    GPT_AUDIT_TABLE = 'gpt_audit_dim'
    GPT_TOKEN_TABLE = 'gpt_token_dim'
    GPT_CONVERSATION_TABLE = 'gpt_conversation_fact'
    GPT_MODEL_TABLE = 'gpt_model_dim'

    BASE_DIR = opath.dirname(opath.dirname(opath.dirname(opath.abspath(__file__))))
    DATA_DIR = opath.join(BASE_DIR, 'data')
    MEDIA_PATH: str = f"{DATA_DIR}/media/images/{{user}}/{{file}}"
    DATA_FILE_PATH =  f"{DATA_DIR}/fitness/{{date}}_{{username}}_{{category}}.csv"
    PROCESSED_FILE_PATH = f"{DATA_DIR}/fitness/processed/{{date}}_{{username}}_{{category}}.csv"
    DB_PATH: str = f"{BASE_DIR}/db/app.db"
    DATABASE_URL: str = f'sqlite:///{DB_PATH}'
