import os
import time
from html import escape
from runner import run_python
from config import ADMIN_ID, FILE_EXTENSION
from log import logger
import telebot

last_run = 0


def file_exists_exact(filename):
    files = os.listdir(".")
    return filename in files


def register_run(bot: telebot.TeleBot):
    # Lệnh run: Chạy file python, hàm cốt lõi của bot.
    @bot.message_handler(commands=["run"])
    def run_file(message):
        # Kiểm tra ID người dùng
        if message.chat.id != ADMIN_ID:
            return
        # Chống spam
        global last_run
        if time.time() - last_run < 15:
            return
        last_run = time.time()

        try:
            parts = message.text.split()
            # Phòng lỗi truy cập phần tử hợp lệ trước khi lấy giữ liệu.
            if len(parts) < 2:
                bot.reply_to(
                    message, "Cách sử dụng: ten-file.py. Vui lòng nhập đúng cú pháp"
                )
                return
            file_name = parts[1]
            # Kiểm tra đuôi file .py
            if not file_name.endswith(FILE_EXTENSION):
                logger.warning(
                    f"Execution request by user {message.chat.id} rejected: invalid extension for '{file_name}'"
                )
                bot.reply_to(
                    message, "File không hợp lệ, chỉ file .py mới được phép chạy"
                )
                return

            # Kiểm tra file tồn tại.
            if not file_exists_exact(file_name):
                logger.warning(
                    f"Execution request by user {message.chat.id} failed: file '{file_name}' not found."
                )
                bot.reply_to(
                    message,
                    "Không tìm thấy file. Hãy kiểm tra lại tên file và chữ hoa/chữ thường.",
                )
                return

            logger.info(f"User {message.chat.id} triggered run command for '{file_name}'")
            out, err = run_python(file_name)

            if err:
                bot.reply_to(
                    message, f"<pre>{escape(err[-3000:])}</pre>", parse_mode="HTML"
                )

            else:
                bot.reply_to(
                    message, f"<pre>{escape(out[-3000:])}</pre>", parse_mode="HTML"
                )
        except Exception as e:
            logger.exception("Unexpected error")
            bot.reply_to(message, str(e))
