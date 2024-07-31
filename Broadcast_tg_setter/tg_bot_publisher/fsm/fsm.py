from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    channel_group_management = State()
    broadcast_management = State()
    start_broadcast = State()    
    channels_management = State()    
    add_channel = State()
    add_channel_group = State()
    delete_channel = State()    
    delete_channel_group = State()
    show_channels_of_group = State()
    update_group_waiting_name = State() 
    update_group = State()    
    process_change_group_name = State()
    process_add_group_channels = State()
    process_delete_group_channels = State()
 