import subprocess
import os
import time
import logging
from config import RUN_TIMEOUT

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
    start_time = time.time()
    start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    logger.info(f"Started executing file '{file_name}' at {start_time_str}")

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
        duration = time.time() - start_time
        
        # Ghi log kết quả
        if stderr:
            logger.error(
                f"Execution of '{file_name}' finished with errors in {duration:.2f}s: {stderr[:200]}"
            )
        else:
            logger.info(
                f"Execution of '{file_name}' completed successfully in {duration:.2f}s"
            )
        
        return stdout, stderr
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        logger.warning(
            f"Execution of '{file_name}' timed out after {duration:.2f}s (limit: {RUN_TIMEOUT}s)"
        )
        process.kill()
        return "", "Timeout: Chạy quá thời gian cho phép"
    except OSError as e:
        logger.error(f"OSError executing '{file_name}': {e}")
        return "", "Lỗi: File không tìm thấy hoặc không chạy được"
    except Exception as e:
        logger.exception(f"Unexpected error executing '{file_name}'")
        return "", f"Lỗi: {str(e)}"
