import threading
import time

import telebot
from config import ADMIN_ID

_MIN_PING_INTERVAL = 1.0
_last_ping: float | None = None
_ping_lock = threading.Lock()


def register_ping(bot: telebot.TeleBot):
    @bot.message_handler(commands=["ping"])
    def ping(message):
        if message.from_user is None or message.from_user.id != ADMIN_ID:
            return

        global _last_ping
        now = time.monotonic()
        with _ping_lock:
            if _last_ping is not None and now - _last_ping < _MIN_PING_INTERVAL:
                return
            _last_ping = now

        bot.reply_to(message, "online")
