LEXICON_RU: dict[str, str] = {
    '/start': '<b>Добро пожаловать в панель управления рассылкой!</b>\n'
              'Чтобы посмотреть справку, введите команду /help',
              
    '/access_denied': '<b>У вас нет доступа к панели управления!</b>\n'
                      'Введите команду /help',
                      
    '/help': 'Это бот для рассылок по телеграмм каналам\n'
             'Используйте команды клавиатуры (значок около кнопки в виде скрепки)\n'
             'Если бот говорит вам, что у вас нет доступа, то обратитесь'
             ' к администратору @kAzaKed.',
             
    'cancel': 'Отмена',
    
    'update_group_cancel': 'Назад',
    
    
    
    'broadcast_management': 'Управление рассылками',
    
    'channels_management': 'Управление каналами',
    
    'channel_groups_management': 'Управление группами каналов',
    
    'backward': 'Назад',
    
    
    
    'start_broadcast': 'Провести рассылку',
    
    'add_channel': 'Добавить канал',
    
    'add_channel_group': 'Создать группу каналов',
    
    'show_channels': 'Список каналов',
    
    'delete_channel': 'Удалить канал',
    
    'delete_channel_group': 'Удалить группу каналов',
    
    'show_channel_groups': 'Список групп каналов',
    
    'show_groups_of_channel': 'Список каналов группы',
    
    'update_group': 'Изменить группы каналов',
    
    'add_channels_for_group': 'Добавить каналы в группу',
    
    
    
    'broadcast_management_answer': 'Вы в панеле управления расслыками',
    
    'channels_management_answer': 'Вы в панеле управления каналами',
    
    'channel_groups_management_answer': 'Вы в панеле управления группами каналов',
    
    'start_broadcast_answer': 'Введите сообщение для рассылки:',
    
    'add_channel_answer': 'Введите имя канала, который хотите подключить:',
    
    'add_channel_group_answer': 'Введите имя группы каналов, который хотите подключить:',
    
    'show_channels_answer': 'Список подключенных каналов:',
    
    'delete_channel_answer': 'Введите имя канала, который хотите удалить.\n'
    'Обратите внимание, что бот удалит <b>ТОЛЬКО ОДИН</b> канал с введенным именем.'
    'Если вы хотите удалить больше одного дубликата, то повторите удаление столько раз'
    'сколько у вас дубликатов.',
    
    'delete_channel_group_answer': 'Введите имя группы каналов, которую хотите удалить.\n',
    
    'show_channel_groups_answer': 'Список созданных групп каналов:',
    
    'update_group_answer': 'Вы в панеле изменения групп каналов, выберите действие',
    
    'show_channels_of_group_answer': 'Введите имя группы каналов, список каналов которой хотите получить:',
    
    'add_channels_for_group_answer': 'Введите список каналов, который хотите добавить в группу через точку с '
    'запятой, без пробелов. Лучше добавлять одновременно не больше 10 каналов',
    
    
    
    'add_channel_success': 'Канал успешно добавлен!',
    
    'broadcast_success': 'Рассылка прошла успешно!',
    
    'delete_channel_success': 'Канал успешно удален',
    
    'add_channel_group_success': 'Группа каналов успешно создана!\n\n'
    'Теперь вы можете добавить в нее каналы для сегментации рассылки',
    
    'delete_channel_group_success': 'Группа каналов успешно удалена',
    
    
    
    'other_answer': 'Пожалуйста, введите корректное сообщение\n'
                    'Вы можете использовать кнопки интерфейса\n'
                    'Для этого нажмите на значок справа на строке ввода\n\n'
                    'Если считаете, что бот работает неисправно, то попробуйте'
                    'ввести вручную команду /start, если это не поможет - напишите'
                    ' администратору @kAzaKed',
                    
    'canceled': 'Вы отменили действие',
    
    'update_canceled': 'Вы отменили изменение группы каналов и вернулись в панель управления группами',
    
    'backwarded': 'Вы вернулись в главное меню',
    
    
    
    'start_bot_error': 'Ошибка при запуске бота, скорее всего у вас скрыт либо отсутствует алиас, '
    'необходимый для идентификации пользователя, добавьте его в профиле либо сообщите об ошибке @kAzaKed',
    
    'deleting_channel_error': 'Ошибка при удалении канала, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'deleting_channel_group_error': 'Ошибка при удалении группы каналов, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'show_channels_error': 'Ошибка при попытке получить список каналов, возможно вы пока не подключили ни одного канала'
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'show_channel_groups_error': 'Ошибка при попытке получить список групп каналов, возможно вы пока не создали ни одной группы'
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'show_channels_of_group_error': 'Ошибка при попытке получить список каналов группы, возможно вы неправильно ввели имя группы, '
    'или у введенной группы нет каналов, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'help_error': 'Ошибка при получении справочной инструкции, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'backward_error': 'Ошибка при возврате в главное меню, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'adding_channel_error': 'Ошибка при создании канала, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'adding_channel_group_error': 'Ошибка при создании группы каналов, возможно группа с таким именем уже существует в системе, '
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'cancel_channel_action_error': 'Ошибка при отмене действия с каналом, '
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'cancel_channel_group_action_error': 'Ошибка при отмене действия с группой каналов, '
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'channel_management_error': 'Ошибка при переходе в панель управления каналами, '
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'channel_group_management_error': 'Ошибка при переходе в панель управления группами каналов, '
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'broadcast_error': 'Ошибка при отправке сообщения для рассылки, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'broadcast_cancel_error': 'Ошибка при отмене рассылки, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'start_broadcast_error': 'Ошибка при начале работы с рассылкой, попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'broadcast_management_error': 'Ошибка при переходе в панель управления рассылками'
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'update_group_error': 'Ошибка при переходе в панель изменения групп каналов, '
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'cancel_group_update_error': 'Ошибка при возвращении в панель управления группами каналов, '
    'попробуйте еще раз либо сообщите об ошибке @kAzaKed',
    
    'add_channels_for_group_error': 'Ошибка при добавлении каналов в группу каналов, возможно вы ввели список каналов неправильно, '
    'попробуйте ввести еще раз список каналов через точку с запятой без пробелов. Лучше добавлять одновременно не больше 10 каналов'
}