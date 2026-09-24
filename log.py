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
def set_log_level(level: str | int) -> str:
    """
    Điều chỉnh cấp độ ghi log trong runtime.
    Chấp nhận tên level (DEBUG, INFO, WARNING, ERROR, CRITICAL) hoặc int.
    """
    _setup_logging()
    if isinstance(level, str):
        level_str = level.strip().upper()
        numeric_level = getattr(logging, level_str, None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Cấp độ log không hợp lệ: '{level}'")
    elif isinstance(level, int):
        numeric_level = level
        level_str = logging.getLevelName(level)
    else:
        raise ValueError(f"Kiểu dữ liệu cấp độ log không hợp lệ: {type(level)}")

    with _config_lock:
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)
        for handler in root_logger.handlers:
            handler.setLevel(numeric_level)
        logger.setLevel(numeric_level)

    logger.info(f"Log level changed to {level_str}")
    return level_str


def get_current_log_level() -> str:
    """Trả về tên cấp độ log hiện tại."""
    level = logging.getLogger().getEffectiveLevel()
    return logging.getLevelName(level)


def clean_log_file() -> tuple[bool, str]:
    """
    Xóa toàn bộ nội dung file log và ghi lại sự kiện dọn log.
    """
    _setup_logging()
    with _config_lock:
        try:
            _ensure_logging_dir()
            with LOG_FILE.open("w", encoding="utf-8") as f:
                f.truncate(0)
            logger.info("Log file cleaned.")
            return True, "File log đã được dọn dẹp thành công."
        except Exception as e:
            logger.exception("Error cleaning log file")
            return False, f"Đã có lỗi khi dọn dẹp file log: {e}"


def get_last_logs(
    lines: int = LOG_LINES,
    level: str | None = None,
    time_filter: str | None = None,
) -> str:
    """
    Đọc các dòng log cuối cùng, hỗ trợ lọc theo cấp độ (level) và mốc thời gian (time_filter).
    """
    try:
        if not LOG_FILE.exists():
            return "Chưa có file log."
        with LOG_FILE.open("r", encoding="utf-8", errors="ignore") as f:
            data = f.readlines()

        # Lọc theo level nếu có
        if level:
            level_tag = f"| {level.strip().upper()} |"
            data = [line for line in data if level_tag in line]

        # Lọc theo time_filter nếu có (ví dụ '11:09')
        if time_filter:
            tf = time_filter.strip()
            data = [
                line for line in data
                if tf in (line.split("|")[0] if "|" in line else line)
            ]

        return "".join(data[-lines:]) or "Log hiện tại đang trống."
    except Exception as e:
        logger.exception("Error reading log")
        return f"Đã có lỗi khi đọc log: {e}"


