from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    start_broadcast = State()        
    add_channel = State()         
 