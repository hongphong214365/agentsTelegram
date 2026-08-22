import pytest
from pathlib import Path
from unittest.mock import patch
import log


def test_log_directory_exists():
    # Kiểm tra xem thư mục cha của LOG_FILE đã được tạo chưa
    from config import LOG_FILE
    assert LOG_FILE.parent.exists()


def test_get_last_logs_file_not_exist(tmp_path):
    # Mock LOG_FILE thành một file không tồn tại trong thư mục tạm
    fake_log_file = tmp_path / "non_existent.log"
    with patch("log.LOG_FILE", fake_log_file):
        result = log.get_last_logs()
        assert result == "Chưa có file log."


def test_get_last_logs_empty(tmp_path):
    # Mock LOG_FILE thành một file trống
    fake_log_file = tmp_path / "empty.log"
    fake_log_file.touch()
    with patch("log.LOG_FILE", fake_log_file):
        result = log.get_last_logs()
        assert result == "Log hiện tại đang trống."


def test_get_last_logs_with_content(tmp_path):
    # Mock LOG_FILE và ghi nội dung thử nghiệm
    fake_log_file = tmp_path / "test.log"
    lines = [f"Dòng log thứ {i}\n" for i in range(1, 31)]
    fake_log_file.write_text("".join(lines), encoding="utf-8")
    
    with patch("log.LOG_FILE", fake_log_file):
        # Đọc 20 dòng mặc định
        result = log.get_last_logs()
        expected = "".join(lines[-20:])
        assert result == expected

        # Đọc 5 dòng
        result_5 = log.get_last_logs(lines=5)
        expected_5 = "".join(lines[-5:])
        assert result_5 == expected_5


def test_get_last_logs_exception(tmp_path):
    # Giả lập lỗi khi đọc file (ví dụ truyền một Path là thư mục thay vì file)
    fake_log_file = tmp_path / "a_directory"
    fake_log_file.mkdir()
    
    with patch("log.LOG_FILE", fake_log_file):
        result = log.get_last_logs()
        assert "Đã có lỗi khi đọc log" in result
