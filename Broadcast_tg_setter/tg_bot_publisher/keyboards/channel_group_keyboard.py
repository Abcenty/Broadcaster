from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.general_keyboard import button_backward

from lexicon.lexicon_ru import LEXICON_RU

button_add_channel_group = KeyboardButton(text=LEXICON_RU['add_channel_group'])
button_show_channel_groups = KeyboardButton(text=LEXICON_RU['show_channel_groups'])
button_delete_channel_group = KeyboardButton(text=LEXICON_RU['delete_channel_group'])
button_show_channels_of_group = KeyboardButton(text=LEXICON_RU['show_groups_of_channel'])
button_update_group = KeyboardButton(text=LEXICON_RU['update_group'])

channel_group_buttons_builder = ReplyKeyboardBuilder()

channel_group_buttons_builder.row(button_add_channel_group,
                      button_show_channel_groups,
                      button_delete_channel_group,
                      button_show_channels_of_group,
                      button_backward,
                      button_update_group,
                      width=6)

channel_group_buttons: ReplyKeyboardMarkup = channel_group_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)