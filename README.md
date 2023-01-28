# Бот для студии
____
## Немного о боте
### Студия - это компания, которая оказывает услуги по разработке чего либо, например телеграмм ботов. Клиент (заказчик) пишет куратору о своем желании заказать бота. Куратор уточняет ТЗ, бюджет. После куратор (он же владелец студии) пишет в чат с кодерами, передавая ТЗ и бюджет заказчику (добавляя свою наценку, например +30$ к бюджету заказчика). Кодер, который будет готов выполнить заказ - говорит куратору о своем жалнии. Владелец студии заходит в бота, создает комнату, назначая кодера исполнителем. Бот дает куратору код комнаты, который нужно передать заказчику. Клиент вводит код в боте и попадает в комнату. Все сообщения исполнителя/заказчика отправляются друг другу, таким образом они могут спокойно общаться друг с другом, не зная с кем конкретно они общаются. Все сообщения в комнате логируются, поэтому попытка обмена контактами / информацией о цене / скама будут очевидны для куратора
___
## Установка и  настройка бота
### Для установки бота - необходимо перейти на [официальный сайт питона](https://www.python.org/downloads/) и скачать инсталятор последней версии. При установке очень важно нажать на галочку ADD TO PATCH, ведь без нее установка библиотек будет некорректно работать <p>
### Теперь настроим самого бота. Его нужно создать в телеграм боте  @BotFather. Открываем файл config.py через любой редактор кода (или даже блокнот) и ранее полученный токен (в ботфазере) вставляем в поле TOKEN. Дальше в списке admin вставляем айди всех админов, через запятую (если админ айди - пишем только его айди, без запятых). Айди получается в боте @userinfobot. Далее создаем в телеге канал, который будет использоваться для логов. Добавляем в канал бота @myidbot и пишем в канале /getgroupid. Бот выдаст айди канала, который мы должны указать в поле logs. Кстати так же в этом канале должен быть ваш бот (которого вы создавали ранее в ботфазере), а так же у него должны быть админ.права. Последний этап в настройке конфига - создание правил. Их нужно придумать и разместить на каком-то интернет.ресурсе, например я выбрал телеграф (еще могу посоветовать телетайп). Ссылку на эти правила укажите в поле customerRules
___
## Запуск бота
### Для запуска бота нужно просто запустить файл start.bat. Этот файл сам установит нужные боту библиотеки
