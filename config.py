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
ADMIN_ID: int | None = None
if ADMIN_ID_RAW:
    try:
        ADMIN_ID = int(ADMIN_ID_RAW)
    except ValueError:
        ADMIN_ID = None


def validate_environment() -> tuple[bool, list[str]]:
    """
    Kiểm tra các biến môi trường cần thiết cho ứng dụng.
    Trả về (is_ok, danh_sách_lỗi).
    """
    errors: list[str] = []
    if not TOKEN:
        errors.append("TELEGRAM_TOKEN is missing in environment variables.")
    elif ":" not in TOKEN:
        errors.append("TELEGRAM_TOKEN format is invalid (expected '<bot_id>:<token>').")

    if not ADMIN_ID_RAW:
        errors.append("TELEGRAM_ADMIN_ID is missing in environment variables.")
    else:
        try:
            int(ADMIN_ID_RAW)
        except ValueError:
            errors.append(
                f"TELEGRAM_ADMIN_ID must be an integer, got '{ADMIN_ID_RAW}'."
            )

    return len(errors) == 0, errors
