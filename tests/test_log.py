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


def test_set_and_get_log_level():
    # Kiểm tra thiết lập và lấy cấp độ log hợp lệ
    old_level = log.get_current_log_level()
    try:
        new_level = log.set_log_level("DEBUG")
        assert new_level == "DEBUG"
        assert log.get_current_log_level() == "DEBUG"

        new_level_info = log.set_log_level("info")
        assert new_level_info == "INFO"
        assert log.get_current_log_level() == "INFO"
    finally:
        log.set_log_level(old_level)


def test_set_log_level_invalid():
    # Kiểm tra lỗi khi truyền cấp độ không hợp lệ
    with pytest.raises(ValueError):
        log.set_log_level("INVALID_LEVEL")


def test_clean_log_file(tmp_path):
    # Kiểm tra tính năng xóa trắng file log
    fake_log_file = tmp_path / "test_clean.log"
    fake_log_file.write_text("Dòng log cũ 1\nDòng log cũ 2\n", encoding="utf-8")

    with patch("log.LOG_FILE", fake_log_file):
        success, msg = log.clean_log_file()
        assert success is True
        assert "thành công" in msg
        # File được xóa sạch nội dung cũ (hoặc chỉ chứa log của lần clean)
        content = fake_log_file.read_text(encoding="utf-8")
        assert "Dòng log cũ 1" not in content


def test_get_last_logs_filtered(tmp_path):
    # Kiểm tra lọc log theo level và time
    fake_log_file = tmp_path / "filter_test.log"
    log_content = (
        "2026-09-24 10:00:00 | INFO | Initializing\n"
        "2026-09-24 11:09:15 | ERROR | Something went wrong\n"
        "2026-09-24 11:09:45 | INFO | User requested /run\n"
        "2026-09-24 12:00:00 | WARNING | Disk low\n"
    )
    fake_log_file.write_text(log_content, encoding="utf-8")

    with patch("log.LOG_FILE", fake_log_file):
        # Lọc theo level ERROR
        error_logs = log.get_last_logs(level="ERROR")
        assert "ERROR | Something went wrong" in error_logs
        assert "Initializing" not in error_logs

        # Lọc theo time 11:09
        time_logs = log.get_last_logs(time_filter="11:09")
        assert "11:09:15" in time_logs
        assert "11:09:45" in time_logs
        assert "10:00:00" not in time_logs

        # Lọc kết hợp cả level và time
        combined = log.get_last_logs(level="INFO", time_filter="11:09")
        assert "User requested /run" in combined
        assert "Something went wrong" not in combined


def test_parse_log_args():
    from handlers.log import parse_log_args

    # Test không cờ
    opts = parse_log_args([])
    assert opts["clean"] is False
    assert opts["level"] is None
    assert opts["time"] is None
    assert opts["set_level"] is None

    # Test -clean và --clean
    assert parse_log_args(["-clean"])["clean"] is True
    assert parse_log_args(["--clean"])["clean"] is True

    # Test --level=info -time=11:09
    opts = parse_log_args(["--level=info", "-time=11:09", "-n=50"])
    assert opts["level"] == "info"
    assert opts["time"] == "11:09"
    assert opts["lines"] == 50

    # Test --set-level=debug
    opts = parse_log_args(["--set-level=debug"])
    assert opts["set_level"] == "debug"


def test_validate_environment():
    import config

    # Test trường hợp hợp lệ
    with patch.object(config, "TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"), \
         patch.object(config, "ADMIN_ID_RAW", "987654321"):
        is_ok, errors = config.validate_environment()
        assert is_ok is True
        assert len(errors) == 0

    # Test thiếu TOKEN
    with patch.object(config, "TOKEN", None), \
         patch.object(config, "ADMIN_ID_RAW", "987654321"):
        is_ok, errors = config.validate_environment()
        assert is_ok is False
        assert any("TELEGRAM_TOKEN is missing" in e for e in errors)

    # Test sai định dạng TOKEN
    with patch.object(config, "TOKEN", "invalidtokenwithoutcolon"), \
         patch.object(config, "ADMIN_ID_RAW", "987654321"):
        is_ok, errors = config.validate_environment()
        assert is_ok is False
        assert any("TELEGRAM_TOKEN format is invalid" in e for e in errors)

    # Test thiếu ADMIN_ID_RAW
    with patch.object(config, "TOKEN", "123:ABC"), \
         patch.object(config, "ADMIN_ID_RAW", None):
        is_ok, errors = config.validate_environment()
        assert is_ok is False
        assert any("TELEGRAM_ADMIN_ID is missing" in e for e in errors)

    # Test ADMIN_ID_RAW không phải số nguyên
    with patch.object(config, "TOKEN", "123:ABC"), \
         patch.object(config, "ADMIN_ID_RAW", "not_a_number"):
        is_ok, errors = config.validate_environment()
        assert is_ok is False
        assert any("must be an integer" in e for e in errors)
