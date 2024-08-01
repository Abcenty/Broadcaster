Приложение для рассылок сообщений на основе телеграмм ботов

Реализовано с помощью aiogram, SQLAlchemy, PostreSQL, RabbitMQ, S3

Полезно для рассылки сообщений в большое количество телеграмм каналов разом

______________________________________________________________________________
План разработки:
+Поменять все id на uuid вместо int

+Служебные сообщения добавить в исключения

-Если добавить в группу один канал несколько раз, то он там продублируется, также и с
дубликатами в общем списке каналов

-Сделать раздел Помощь в главном меню с кратким описанием функционала и с инструкцией по началу
использования приложения

-Сделать разделение каналов по пользователям (реализовать через группы и подгруппы каналов,
предусмотреть защиту от доступа других пользователей к группе, к которой не было передано доступа)

+Сделать возможность формировать, изменять(добавлять и удалять каналы из группы)
группы каналов со своим названием, закрепленных за пользователем и удалять их


-Сделать рассылку в несколько введенных каналов

-Сделать рассылку по группе каналов

+Обработать ошибку при получении каналов при их отсутствии

-Доработать механизм извлечения сообщения из брокера

-Доработать асинхрооность (многие функции работают в синхронном режиме для быстроты выдачи мвп, надо
будет переработать)

-Добавить видео, аудио, документ, файл типы в рассылку

-Добавить галерею медиафайлов

-Добавить в обработку ошибок хендлеров установку исходного состояния

*-Сделать возможность передать группу каналов другому пользователю бота, введя название
группы и имя пользователя

*-Добавить более детализированные исключения


