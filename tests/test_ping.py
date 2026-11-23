from types import SimpleNamespace

from handlers import ping as ping_handler


class FakeBot:
    def __init__(self):
        self.handler = None
        self.replies = []

    def message_handler(self, commands):
        def register(handler):
            self.handler = handler
            return handler

        return register

    def reply_to(self, message, text):
        self.replies.append((message, text))


def _register_ping():
    bot = FakeBot()
    ping_handler.register_ping(bot)
    return bot, bot.handler


def test_ping_rejects_non_admin_sender_in_admin_chat(monkeypatch):
    monkeypatch.setattr(ping_handler, "ADMIN_ID", 123456789)
    monkeypatch.setattr(ping_handler, "_last_ping", None)
    bot, handler = _register_ping()
    message = SimpleNamespace(
        chat=SimpleNamespace(id=123456789),
        from_user=SimpleNamespace(id=987654321),
    )

    handler(message)

    assert bot.replies == []


def test_ping_throttles_admin_replies(monkeypatch):
    monkeypatch.setattr(ping_handler, "ADMIN_ID", 123456789)
    monkeypatch.setattr(ping_handler, "_last_ping", None)
    now = [100.0]
    monkeypatch.setattr(
        ping_handler, "time", SimpleNamespace(monotonic=lambda: now[0])
    )
    bot, handler = _register_ping()
    message = SimpleNamespace(
        chat=SimpleNamespace(id=-100123456789),
        from_user=SimpleNamespace(id=123456789),
    )

    handler(message)
    now[0] = 100.5
    handler(message)
    now[0] = 101.0
    handler(message)

    assert [reply for _, reply in bot.replies] == ["online", "online"]
