import logging
import threading
from config import LOG_FILE, LOG_LINES, LEVEL

logger = logging.getLogger(__name__)

# Lock để đảm bảo thread-safe
_config_lock = threading.Lock()
_logging_initialized = False


def _ensure_logging_dir():
    """Đảm bảo thư mục log tồn tại."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def _setup_logging():
    """Cấu hình logging chỉ 1 lần, thread-safe."""
    global _logging_initialized
    with _config_lock:
        if _logging_initialized:
            return
        _ensure_logging_dir()
        logging.basicConfig(
            filename=str(LOG_FILE),
            level=LEVEL,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        _logging_initialized = True


def startup_log():
    """
    Hàm khởi tạo cho module Nhật Ký.
    Bọc tất cả cấu hình logging ban đầu và các hàm ghi nhật ký.
    Chỉ nên gọi 1 lần khi khởi động ứng dụng.
    """
    _setup_logging()
    logger.info("===== Khởi động module Nhật Ký =====")


# Hàm xử lý.
def get_last_logs(lines: int = LOG_LINES) -> str:
    try:
        if not LOG_FILE.exists():
            return "Chưa có file log."
        with LOG_FILE.open("r", encoding="utf-8", errors="ignore") as f:
            data = f.readlines()
        return "".join(data[-lines:]) or "Log hiện tại đang trống."
    except Exception as e:
        logger.exception("Error reading log")
        return f"There was an error reading log: {e}"


