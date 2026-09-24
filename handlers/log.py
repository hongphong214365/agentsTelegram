from html import escape
import telebot
from config import ADMIN_ID, LOG_LINES
from log import (
    logger,
    get_last_logs,
    clean_log_file,
    set_log_level,
    get_current_log_level,
)


def parse_log_args(parts: list[str]) -> dict:
    """
    Phân tích các tham số truyền vào lệnh /log.
    Hỗ trợ cả tiền tố '-' và '--'.
    """
    options: dict = {
        "clean": False,
        "level": None,
        "time": None,
        "set_level": None,
        "lines": LOG_LINES,
    }

    for part in parts:
        cleaned = part.strip()
        lower = cleaned.lower()
        if lower in ("-clean", "--clean"):
            options["clean"] = True
        elif lower.startswith(("-set-level=", "--set-level=")):
            options["set_level"] = cleaned.split("=", 1)[1].strip()
        elif lower.startswith(("-level=", "--level=")):
            options["level"] = cleaned.split("=", 1)[1].strip()
        elif lower.startswith(("-time=", "--time=")):
            options["time"] = cleaned.split("=", 1)[1].strip()
        elif lower.startswith(("-lines=", "--lines=", "-n=")):
            try:
                options["lines"] = max(1, int(cleaned.split("=", 1)[1].strip()))
            except ValueError:
                pass

    return options


def register_logs(bot: telebot.TeleBot):
    @bot.message_handler(commands=["log"])
    def show_log(message):
        if message.chat.id != ADMIN_ID:
            return

        parts = message.text.split()[1:]
        opts = parse_log_args(parts)

        logger.info(f"User {message.chat.id} executed /log with command: '{message.text}'")

        # Xử lý cờ dọn dẹp file log
        if opts["clean"]:
            success, msg = clean_log_file()
            bot.reply_to(message, msg)
            return

        # Xử lý cờ thay đổi cấp độ log runtime
        if opts["set_level"]:
            try:
                new_lvl = set_log_level(opts["set_level"])
                bot.reply_to(
                    message,
                    f"Cấp độ log đã được cập nhật thành: <b>{new_lvl}</b>",
                    parse_mode="HTML",
                )
            except ValueError as e:
                bot.reply_to(message, f"Lỗi: {e}")
            return

        # Lấy log và lọc theo tiêu chí
        logs = get_last_logs(
            lines=opts["lines"],
            level=opts["level"],
            time_filter=opts["time"],
        )

        # Giới hạn kích thước tin nhắn Telegram để tránh lỗi quá dài
        if len(logs) > 3800:
            logs = "..." + logs[-3800:]

        bot.reply_to(message, f"<pre>{escape(logs)}</pre>", parse_mode="HTML")
