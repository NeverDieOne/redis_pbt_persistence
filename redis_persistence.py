from typing import DefaultDict, Optional, Tuple
import json
from collections import defaultdict

from telegram.ext import BasePersistence
from telegram.ext.utils.types import UD, CD, BD, CDCData, ConversationDict
from redis import Redis


class RedisPersistence(BasePersistence):
    def __init__(self, host: str, port: int, db: int, *args, **kwargs) -> None:
        self.r_conn = Redis(host=host, port=port, db=0, decode_responses=True)
        super().__init__(*args, **kwargs)

    # Methods for db
    def get_redis_connection(self) -> Redis:
        return self.r_conn

    # Methods for bot data
    def get_bot_data(self) -> BD:
        r_conn = self.get_redis_connection()
        bot_data = r_conn.get('bot_data')
        if not bot_data:
            return {}
        return json.loads(bot_data)

    def update_bot_data(self, data: BD) -> None:
        r_conn = self.get_redis_connection()
        bot_data = r_conn.get('bot_data')
        if bot_data and json.loads(bot_data) == data:
            return
        r_conn.set('bot_data', json.dumps(data))
    
    # Methods for chat data
    def get_chat_data(self) -> DefaultDict[int, CD]:
        r_conn = self.get_redis_connection()
        chat_data = r_conn.get('chat_data')
        if chat_data is None:
            return defaultdict(dict)
        return json.loads(chat_data)
        

    def update_chat_data(self, chat_id: int, data: CD) -> None:
        r_conn = self.get_redis_connection()
        pass

    # Methods fot user data
    def get_user_data(self) -> DefaultDict[int, UD]:
        pass

    def update_user_data(self, user_id: int, data: UD) -> None:
        pass

    # Methods for callback data
    def get_callback_data(self) -> Optional[CDCData]:
        pass

    def update_callback_data(self, data: CDCData) -> None:
        pass

    # Methods for conversations
    def get_conversations(self, name: str) -> ConversationDict:
        pass

    def update_conversation(
        self,
        name: str,
        key: Tuple[int, ...],
        new_state: Optional[object]
    ) -> None:
        pass

    def flush(self) -> None:
        pass
