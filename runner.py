import subprocess
import os
import logging
from config import RUN_TIMEOUT
import log  # Import log module để basicConfig được setup

# Lấy logger của module này
logger = logging.getLogger(__name__)


def run_python(file_name):
    """
    Chạy file Python và capture output.
    
    Sử dụng subprocess.Popen thay vì subprocess.run:
    - Non-blocking: có thể kiểm soát process
    - Tương tác real-time: chuẩn bị cho streaming output
    - Ghi log đầy đủ: timeout, error tracking
    
    Args:
        file_name: Đường dẫn file Python cần chạy
        
    Returns:
        tuple: (stdout, stderr)
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    try:
        process = subprocess.Popen(
            ["python", file_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            errors="replace",
        )
        stdout, stderr = process.communicate(timeout=RUN_TIMEOUT)
        
        # Ghi log nếu có lỗi
        if stderr:
            logger.error(f"Lỗi khi chạy {file_name}: {stderr[:200]}")
        
        return stdout, stderr
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout khi chạy {file_name} (>30 giây)")
        process.kill()
        return "", "Timeout: Chạy quá thời gian cho phép"
    except OSError as e:
        logger.error(f"OSError khi chạy {file_name}: {e}")
        return "", "Lỗi: File không tìm thấy hoặc không chạy được"
    except Exception as e:
        logger.exception(f"Lỗi chạy {file_name}")
        return "", f"Lỗi: {str(e)}"
