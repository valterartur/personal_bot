from enum import Enum, auto


class ConversationState(Enum):
    END = -1
    CREATE_CATEGORY = auto()
    UPLOAD_DATA = auto()
    SETUP_TOKEN = auto()

    # image generation
    ACCEPT_NUMBER_OF_IMAGES = auto()
    ACCEPT_IMAGE_DESCRIPTION = auto()
    CREATE_IMAGE = auto()
