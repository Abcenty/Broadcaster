from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    broadcast_management = State()
    start_broadcast = State()    
    channels_management = State()    
    add_channel = State()
    delete_channel = State()         
 