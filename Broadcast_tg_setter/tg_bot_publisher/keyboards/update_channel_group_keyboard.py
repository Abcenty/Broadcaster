from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.general_keyboard import button_backward

from lexicon.lexicon_ru import LEXICON_RU


button_add_channels = KeyboardButton(text=LEXICON_RU['add_channels_for_group'])
button_delete_channels = KeyboardButton(text=LEXICON_RU['delete_channels_from_group'])
button_change_group_name = KeyboardButton(text=LEXICON_RU['change_group_name'])

update_group_buttons_builder = ReplyKeyboardBuilder()

update_group_buttons_builder.row(button_add_channels,
                      button_delete_channels,
                      button_change_group_name,
                      button_backward,
                      width=6)

update_group_buttons: ReplyKeyboardMarkup = update_group_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)