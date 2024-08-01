from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.utills.message_former import format_message
from keyboards.general_keyboard import cancel_button, backward_button
from keyboards.broadcast_keyboard import broadcast_buttons, broadcast_type_buttons
from lexicon.lexicon_ru import LEXICON_RU
from services.queries.users.orm import UserGateway
from services.queries.groups.orm import ChannelGroupGateway
from fsm.fsm import FSMFillForm
from bot import get_bot
from set_broadcast import set_task
from services.s3.dependency import s3_client
from logger import logger

router = Router()

bot = get_bot()

# Этот хэндлер срабатывает на запрос перехода к управлению рассылками
@router.message(F.text == LEXICON_RU['broadcast_management'], StateFilter(default_state))
async def process_broadcast_management(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['broadcast_management_answer'], reply_markup=broadcast_type_buttons)
            await state.set_state(FSMFillForm.set_broadcast_type)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['broadcast_management_error'])
        logger.info('Error while starting broadcast management')
        
        
# Этот хэндлер срабатывает на запрос перехода к управлению рассылками
@router.message(F.text == LEXICON_RU['total_broadcast'], StateFilter(FSMFillForm.set_broadcast_type))
async def process_setting_broadcast_type_total(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['broadcast_total_answer'], reply_markup=broadcast_buttons)
            await state.set_data(data={'target': 'ALL'})
            await state.set_state(FSMFillForm.broadcast_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['setting_broadcast_type_error'])
        logger.info('Error while setting broadcast type total')
        
        
@router.message(F.text == LEXICON_RU['group_broadcast'], StateFilter(FSMFillForm.set_broadcast_type))
async def setting_broadcast_type_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['group_broadcast_answer'], reply_markup=backward_button)
            await state.set_state(FSMFillForm.set_group_for_broadcast)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['broadcast_management_error'])
        logger.info('Error while setting broadcast type group')
        
        
@router.message(F.text, StateFilter(FSMFillForm.set_group_for_broadcast))
async def process_setting_broadcast_type_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['process_group_broadcast_answer'], reply_markup=broadcast_buttons)
            try:
                group = ChannelGroupGateway.get(message.text).name
            except:
                raise
            await state.set_data(data={'target': group})
            await state.set_state(FSMFillForm.broadcast_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['broadcast_management_error'])
        logger.info('Error while setting broadcast type group')

# Этот хэндлер срабатывает на запрос создания рассылки
@router.message(F.text == LEXICON_RU['start_broadcast'], StateFilter(FSMFillForm.broadcast_management))
async def process_start_broadcast(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.start_broadcast)
            await message.answer(text=LEXICON_RU['start_broadcast_answer'], reply_markup=cancel_button)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['start_broadcast_error'])
        logger.info('Error while starting broadcast')
        
# Этот хэндлер срабатывает на отмену создания рассылки
@router.message(F.text == LEXICON_RU['cancel'], StateFilter(FSMFillForm.start_broadcast))
async def process_broadcast_cancel(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['canceled'],
            reply_markup=broadcast_buttons,
        )
        await state.set_state(FSMFillForm.broadcast_management)
    except:
        await message.answer(text=LEXICON_RU['broadcast_cancel_error'])
        logger.info('Error while canceling broadcast')
        
        
# Этот хэндлер срабатывает на ввод текстового сообщения для рассылки
@router.message(F.text, StateFilter(FSMFillForm.start_broadcast))
async def process_broadcast_text(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            data = await state.get_data()
            await set_task(format_message(type='text', text=message.text, target=data['target']))
            await message.answer(text=LEXICON_RU['broadcast_success'], reply_markup=broadcast_buttons)
            await state.set_state(FSMFillForm.broadcast_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['broadcast_error'])
        logger.info('Error while processing text broadcast')
        
# Этот хэндлер срабатывает на ввод изображения для рассылки с подписью или без
@router.message(F.photo, StateFilter(FSMFillForm.start_broadcast))
async def process_broadcast_photo(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            data = await state.get_data()
            file = await bot.get_file(message.photo[-1].file_id)
            file_path = file.file_path
            bfile = await bot.download_file(file_path)
            s3_client.upload_file(file_path=file_path, file=bfile)
            await set_task(format_message(type='photo', file_path=file_path.split("/")[-1],
                                        text=message.caption if message.caption is not None else "",
                                        target=data['target']))
            await message.answer(text=LEXICON_RU['broadcast_success'], reply_markup=broadcast_buttons)
            await state.set_state(FSMFillForm.broadcast_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['broadcast_error'])
        logger.info('Error while processing broadcast with photo')
        
        
# Этот хэндлер срабатывает на ввод изображения для рассылки с подписью или без
@router.message(F.video, StateFilter(FSMFillForm.start_broadcast))
async def process_broadcast_video(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            data = await state.get_data()
            file = await bot.get_file(message.video.file_id)
            file_path = file.file_path
            bfile = await bot.download_file(file_path)
            s3_client.upload_file(file_path=file_path, file=bfile)
            await set_task(format_message(type='video', file_path=file_path.split("/")[-1],
                                        text=message.caption if message.caption is not None else "",
                                        target=data['target']))
            await message.answer(text=LEXICON_RU['broadcast_success'], reply_markup=broadcast_buttons)
            await state.set_state(FSMFillForm.broadcast_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['broadcast_error'])
        logger.info('Error while processing broadcast with video')