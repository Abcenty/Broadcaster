from enum import Enum

class MessageType(Enum):
    """Тип сообщения"""

    PHOTO = "PHOTO"
    """Изображение с подписью или без"""
    TEXT = "TEXT"
    """Текст"""
    VIDEO = "VIDEO"
    """Видео с подписью или без"""


def format_message(type: MessageType | str, text: str = "", file_path: str = None):
    return f"type<!&!>{type}<!#!>file_path<!&!>{file_path}<!#!>text<!&!>{text}"