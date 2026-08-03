import os
import sys
from pathlib import Path
import logging

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID_RAW = os.getenv("TELEGRAM_ADMIN_ID")
# Đường dẫn đến tập tin log
LOG_FILE = Path("temp/agent.log")
# Số dòng log
LOG_LINES = 20
# Cấp độ ghi log.
LEVEL = logging.INFO
# Giới hạn thời gian chạy.
RUN_TIMEOUT = 30
# Đuôi file.
FILE_EXTENSION = ".py"
if not TOKEN:
    sys.exit("Lỗi: Chưa cấu hình biến môi trường 'TELEGRAM_TOKEN'.")

if not ADMIN_ID_RAW:
    sys.exit("Lỗi: Chưa cấu hình biến môi trường 'TELEGRAM_ADMIN_ID'.")

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError:
    sys.exit(
        f"Lỗi: 'TELEGRAM_ADMIN_ID' phải là một số nguyên, nhận được: '{ADMIN_ID_RAW}'."
    )
