# Redis Persistence for python-telegram-bot

Позволяет хранить chat_data, bot_data, user_data, conversations в Redis.

## Как подключить

```python
import os

from telegram.ext import Updater

from redis_persistence import RedisPersistence


def main():
    persistence = RedisPersistence(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        db=int(os.getenv('REDIS_DB_NUMBER')),
        password=os.getenv('REDIS_PASSWORD')  # опциональный аргумент
    )

    updater = Updater(os.getenv('TG_BOT_TOKEN'), persistence=persistence)
```

## Как использовать

### Замечания
1. Когда вы используете bot_data, chat_data, user_data, данные автоматически сохраняются в Redis.
2. При перезагрузке бота данные будут автоматически подгружены из редис.


### Пример
```python
from telegram import Update
from telegram.ext import CallbackContext


def some_handler(update: Update, context: CallbackContext) -> None:
    context.bot_data['foo'] = 'bar'  # Данные будут загружены в БД

def one_more_handler(update: Update, context: CallbackContext) -> None:
    print(context.bot_data['foo'])  # Данные будут подгружены из БД
```

## ConversationHandler

При использовании ConversationHandler стейты пользователей 
будут хранится в БД под ключом, который указан в аргументе
`name` у `ConversationHandler`.

```python
from telegram.ext import ConversationHandler

conv_handler = ConversationHandler(
    entry_points=[...],
    states={
        'some_state': ...
    },
    fallbacks=[...],
    name='my_conversation',
    persistent=True
)
```

## Если хочется самостоятельно записать что-то в БД.

```python
from telegram import Update
from telegram.ext import CallbackContext


def some_handler(update: Update, context: CallbackContext) -> None:
    redis_conn = context.dispatcher.persistence.get_redis_connection()
    redis_conn.set('foo', 'bar')
    print(redis_conn.get('foo'))  # bar
```