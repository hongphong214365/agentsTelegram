from types import SimpleNamespace

import pytest

from handlers import log as log_handler
from handlers import run as run_handler
from handlers import status as status_handler


class FakeBot:
    def __init__(self):
        self.handlers = {}
        self.replies = []

    def message_handler(self, commands):
        def register(handler):
            self.handlers[commands[0]] = handler
            return handler

        return register

    def reply_to(self, message, text, **kwargs):
        self.replies.append((message, text, kwargs))


@pytest.mark.parametrize(
    ("module", "register", "command"),
    [
        (run_handler, run_handler.register_run, "run"),
        (log_handler, log_handler.register_logs, "log"),
        (status_handler, status_handler.register_status, "status"),
    ],
)
def test_admin_chat_does_not_authorize_other_sender(
    monkeypatch, module, register, command
):
    admin_id = 123456789
    monkeypatch.setattr(module, "ADMIN_ID", admin_id)
    bot = FakeBot()
    register(bot)
    message = SimpleNamespace(
        chat=SimpleNamespace(id=admin_id),
        from_user=SimpleNamespace(id=987654321),
        text=f"/{command}",
    )

    bot.handlers[command](message)

    assert bot.replies == []
