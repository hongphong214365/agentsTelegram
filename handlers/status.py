import telebot
from config import ADMIN_ID, RUN_TIMEOUT, LOG_FILE
import platform
from pathlib import Path


def register_status(bot: telebot.TeleBot):
    # Hàm lấy thông tin và tạo câu trả lời.
    def get_info() -> str:
        cwd = Path.cwd()
        python_version = platform.python_version()
        return (
            "Agent Status\n\n"
            f"Thư mục hiện tại: {cwd}\n"
            f"Phiên bản python: {python_version}\n"
            f"Thời gian timeout của file là: {RUN_TIMEOUT} giây\n"
            f"Đường dẫn tới file log: {LOG_FILE}"
        )

    # Hàm kiểm tra trạng thái chi tiết của bot.
    @bot.message_handler(commands=["status"])
    def status(message):
        if message.chat.id != ADMIN_ID:
            return
        bot.reply_to(message, get_info())
