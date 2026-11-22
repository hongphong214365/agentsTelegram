import pytest

import main


def test_network_error_redacts_token_from_logs_and_output(monkeypatch, caplog, capsys):
    token = "123456:secret-token"
    monkeypatch.setattr(main, "TOKEN", token)
    monkeypatch.setattr(main, "startup_log", lambda: None)
    monkeypatch.setattr(main, "validate_environment", lambda: (True, []))

    class FailedBot:
        def __init__(self, bot_token):
            assert bot_token == token

        def get_me(self):
            raise RuntimeError(f"request failed for /bot{token}/getMe")

    monkeypatch.setattr(main.telebot, "TeleBot", FailedBot)

    with caplog.at_level("CRITICAL"):
        with pytest.raises(SystemExit):
            main.main()

    output = capsys.readouterr().out
    assert token not in caplog.text
    assert token not in output
    assert "[REDACTED]" in caplog.text
    assert "[REDACTED]" in output
