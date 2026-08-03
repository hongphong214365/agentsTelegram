import telebot
from config import ADMIN_ID


def register_start(bot: telebot.TeleBot):
    # Lệnh start: Chào mừng và hướng dẫn sử dụng.
    @bot.message_handler(commands=["start"])
    def start(message):
        if message.chat.id != ADMIN_ID:
            return
        bot.reply_to(
            message,
            "Chào mừng! Đây là Agent Bot điều khiển máy tính từ xa.\n\n"
            "Các lệnh hỗ trợ:\n"
            "/ping - Kiểm tra nhanh kết nối\n"
            "/run <tên_file.py> - Thực thi một file Python\n"
            "/start - Hiển thị hướng dẫn này\n"
            "/log - Xem 20 dòng log gần nhất\n"
            "/status - Xem trạng thái chi tiết của bot (thử nghiệm)",
        )
