from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.general_keyboard import cancel_button, backward_button
from keyboards.channel_group_keyboard import channel_group_buttons
from keyboards.update_channel_group_keyboard import update_group_buttons
from lexicon.lexicon_ru import LEXICON_RU
from services.queries.users.orm import UserGateway
from fsm.fsm import FSMFillForm
from services.queries.groups.orm import ChannelGroupGateway
from bot import get_bot
from logger import logger


router = Router()

bot = get_bot()


# Этот хэндлер срабатывает на запрос изменения группы
@router.message(F.text == LEXICON_RU['update_group'], StateFilter(FSMFillForm.channel_group_management))
async def update_group_waiting_name(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['update_group_waiting_name'], reply_markup=backward_button)
            await state.set_state(FSMFillForm.update_group_waiting_name)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['update_group_error'])
        logger.info('Error while starting update channel group')
        
        
# Этот хэндлер срабатывает на выход из панели изменения группы каналов
@router.message(F.text == LEXICON_RU['update_group_cancel'], StateFilter(FSMFillForm.update_group,
                                                                         FSMFillForm.update_group_waiting_name))
async def update_group_cancel(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['update_canceled'],
            reply_markup=channel_group_buttons,
        )
        await state.set_state(FSMFillForm.channel_group_management)
    except:
        await message.answer(text=LEXICON_RU['cancel_group_update_error'])
        logger.info('Error while canceling updating of channel group')

  
# Этот хэндлер срабатывает на ввод имени группы для изменения
@router.message(F.text, StateFilter(FSMFillForm.update_group_waiting_name))
async def update_group_set_name(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            name = message.text
            if ChannelGroupGateway.get(name) is None:
                raise    
            await state.set_data(data={'name': name})
            await message.answer(text=LEXICON_RU['update_group_set_name_answer'], reply_markup=update_group_buttons)
            await state.set_state(FSMFillForm.update_group)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['update_setting_name_error'])
        logger.info('Error while setting name to update channel group')
        
        
# Этот хэндлер срабатывает на отмену изменения группы каналов
@router.message(F.text == LEXICON_RU['cancel'], StateFilter(FSMFillForm.process_delete_group_channels,
                                                            FSMFillForm.process_add_group_channels,
                                                            FSMFillForm.process_change_group_name))
async def cancel_process_group_updating(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['update_canceled'],
            reply_markup=update_group_buttons,
        )
        await state.set_state(FSMFillForm.update_group)
    except:
        await message.answer(text=LEXICON_RU['cancel_group_update_error'])
        logger.info('Error while canceling updating process of channel group') 
        
        
# Этот хэндлер срабатывает на запрос добавления каналов в группу
@router.message(F.text == LEXICON_RU['add_channels_for_group'], StateFilter(FSMFillForm.update_group))
async def update_group_add_channels(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['add_channels_for_group_answer'], reply_markup=cancel_button)
            await state.set_state(FSMFillForm.process_add_group_channels)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['add_channels_for_group_error'])
        logger.info('Error while adding channels to group')
        
        
# Этот хэндлер срабатывает на ввод каналов для добавления в группу
@router.message(F.text, StateFilter(FSMFillForm.process_add_group_channels))
async def process_add_group_channels(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            data = await state.get_data()
            name = data['name']
            channels = message.text.split(';')
            ChannelGroupGateway.update(name=name, channels=channels, update_type='add_channels')
            await message.answer(text=LEXICON_RU['add_channels_for_group_success'], reply_markup=update_group_buttons)
            await state.set_state(FSMFillForm.update_group)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['add_channels_for_group_error'])
        logger.info('Error while process adding channels for group')
        
        
# Этот хэндлер срабатывает на запрос удаления каналов из группы
@router.message(F.text == LEXICON_RU['delete_channels_from_group'], StateFilter(FSMFillForm.update_group))
async def update_group_delete_channels(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['delete_channels_from_group_answer'], reply_markup=cancel_button)
            await state.set_state(FSMFillForm.process_delete_group_channels)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['delete_channels_from_group_error'])
        logger.info('Error while deleting channels from group')
        
        
# Этот хэндлер срабатывает на ввод каналов для удаления из группы
@router.message(F.text, StateFilter(FSMFillForm.process_delete_group_channels))
async def process_delete_group_channels(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            data = await state.get_data()
            name = data['name']
            channels = message.text.split(';')
            ChannelGroupGateway.update(name=name, channels=channels, update_type='delete_channels')
            await message.answer(text=LEXICON_RU['delete_channels_from_group_success'], reply_markup=update_group_buttons)
            await state.set_state(FSMFillForm.update_group)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['delete_channels_from_group_error'])
        logger.info('Error while process deleting channels from group')
        
        
# Этот хэндлер срабатывает на запрос изменения имени группы каналов
@router.message(F.text == LEXICON_RU['change_group_name'], StateFilter(FSMFillForm.update_group))
async def update_group_change_name(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['change_group_name_answer'], reply_markup=cancel_button)
            await state.set_state(FSMFillForm.process_change_group_name)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['change_group_name_error'])
        logger.info('Error while changing group name')
        
        
# Этот хэндлер срабатывает на ввод нового названия группы
@router.message(F.text, StateFilter(FSMFillForm.process_change_group_name))
async def process_change_name(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            data = await state.get_data()
            name = data['name']
            ChannelGroupGateway.update(name=name, new_name=message.text, update_type='change_name')
            await message.answer(text=LEXICON_RU['change_group_name_success'], reply_markup=update_group_buttons)
            await state.set_state(FSMFillForm.update_group)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['change_group_name_error'])
        logger.info('Error while process changing group name')
        
        
