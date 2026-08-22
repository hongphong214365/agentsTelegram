import logging
from config import LOG_FILE, LOG_LINES, LEVEL

logger = logging.getLogger(__name__)


# Hàm xử lí.
def get_last_logs(lines: int = LOG_LINES) -> str:
    try:
        if not LOG_FILE.exists():
            return "Chưa có file log."
        with LOG_FILE.open("r", encoding="utf-8", errors="ignore") as f:
            data = f.readlines()

        return "".join(data[-lines:]) or "Log hiện tại đang trống."
    except Exception as e:
        logger.exception("Lỗi khi đọc log")
        return f"Đã có lỗi khi đọc log: {e}"


# Đảm bảo thư mục chứa file log tồn tại trước khi ghi log
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
