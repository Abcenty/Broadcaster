from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.general_keyboard import cancel_button
from keyboards.channel_group_keyboard import channel_group_buttons
from lexicon.lexicon_ru import LEXICON_RU
from services.queries.users.orm import UserGateway
from fsm.fsm import FSMFillForm
from services.queries.groups.orm import ChannelGroupGateway
from bot import get_bot
from logger import logger


router = Router()

bot = get_bot()

# Этот хэндлер срабатывает на запрос перехода к управлению группами каналов
@router.message(F.text == LEXICON_RU['channel_groups_management'], StateFilter(default_state))
async def process_channel_group_management(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.channel_group_management)
            await message.answer(text=LEXICON_RU['channel_groups_management_answer'], reply_markup=channel_group_buttons)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['channel_group_management_error'])
        logger.info('Error while starting channel group management')
        
        
# Этот хэндлер срабатывает на запрос добавления группы каналов
@router.message(F.text == LEXICON_RU['add_channel_group'], StateFilter(FSMFillForm.channel_group_management))
async def add_channel_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.add_channel_group)
            await message.answer(text=LEXICON_RU['add_channel_group_answer'], reply_markup=cancel_button)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['adding_channel_group_error'])
        logger.info('Error while adding channel group')
        
        
# Этот хэндлер срабатывает на ввод группы каналов для удаления
@router.message(F.text == LEXICON_RU['delete_channel_group'], StateFilter(FSMFillForm.channel_group_management))
async def delete_channel_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.delete_channel_group)
            await message.answer(text=LEXICON_RU['delete_channel_group_answer'], reply_markup=cancel_button)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['deleting_channel_group_error'])
        logger.info('Error while deleting channel group')
  
        
# Этот хэндлер срабатывает на отмену действия с группой каналов
@router.message(F.text == LEXICON_RU['cancel'], StateFilter(FSMFillForm.delete_channel_group,
                                                            FSMFillForm.add_channel_group,
                                                            FSMFillForm.show_channels_of_group,
                                                            ))
async def process_channel_group_cancel(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['canceled'],
            reply_markup=channel_group_buttons,
        )
        await state.set_state(FSMFillForm.channel_group_management)
    except:
        await message.answer(text=LEXICON_RU['cancel_channel_group_action_error'])
        logger.info('Error while canceling action with channel group')
        
        
# Этот хэндлер срабатывает на ввод группы каналов для создания
@router.message(F.text, StateFilter(FSMFillForm.add_channel_group))
async def process_add_channel_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            if message.text == LEXICON_RU['backward']:
                await message.answer(text=LEXICON_RU['backwarded'], reply_markup=channel_group_buttons)
            else:
                ChannelGroupGateway.create(ChannelGroupGateway, message.text)
                await message.answer(text=LEXICON_RU['add_channel_group_success'], reply_markup=channel_group_buttons)
            await state.set_state(FSMFillForm.channel_group_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['adding_channel_group_error'])
        logger.info('Error while adding channel group')
        
        
# Этот хэндлер срабатывает на ввод группы каналов для удаления
@router.message(F.text, StateFilter(FSMFillForm.delete_channel_group))
async def process_delete_channel_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            if message.text == LEXICON_RU['backward']:
                await message.answer(text=LEXICON_RU['backwarded'], reply_markup=channel_group_buttons)
            else:
                ChannelGroupGateway.delete(message.text)
                await message.answer(text=LEXICON_RU['delete_channel_group_success'], reply_markup=channel_group_buttons)
            await state.set_state(FSMFillForm.channel_group_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['deleting_channel_group_error'])
        logger.info('Error while deleting channel group')
        
        
# Этот хэндлер срабатывает на запрос списка групп каналов
@router.message(F.text == LEXICON_RU['show_channel_groups'], StateFilter(FSMFillForm.channel_group_management))
async def process_show_channel_groups(message: Message):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['show_channel_groups_answer'], reply_markup=channel_group_buttons)
            channel_groups = [channel_group.name for channel_group in ChannelGroupGateway.get_list()]
            text = ", ".join (channel_groups).replace(", ", "\n")
            await message.answer(text=text, reply_markup=channel_group_buttons)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['show_channel_groups_error'])
        logger.info('Error while showing list of channel groups')
        
        
# Этот хэндлер срабатывает на запрос списка каналов группы
@router.message(F.text == LEXICON_RU['show_groups_of_channel'], StateFilter(FSMFillForm.channel_group_management))
async def show_channels_of_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.show_channels_of_group)
            await message.answer(text=LEXICON_RU['show_channels_of_group_answer'], reply_markup=cancel_button)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['show_channels_of_group_error'])
        logger.info('Error while showing groups of channel')
        
# Этот хэндлер обрабатывает запрос списка каналов группы   
@router.message(F.text, StateFilter(FSMFillForm.show_channels_of_group))
async def process_show_channels_of_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            if message.text == LEXICON_RU['backward']:
                await message.answer(text=LEXICON_RU['backwarded'], reply_markup=channel_group_buttons)
            else:
                channels = [channel.name for channel in ChannelGroupGateway.get(message.text).channels]
                text = ", ".join(channels).replace(", ", "\n")
                await message.answer(text=f"{LEXICON_RU['show_channels_of_group_success']}\n{text}",
                                        reply_markup=channel_group_buttons)
            await state.set_state(FSMFillForm.channel_group_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['show_channels_of_group_error'])
        logger.info('Error while showing channels of group')
