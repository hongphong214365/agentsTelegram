# agentsTelegram

Bot Telegram đơn giản để chạy các tệp Python từ xa và nhận kết quả đầu ra hoặc thông báo lỗi.

[English](README_EN.md)

## Tính năng

* Chạy các tệp Python từ xa thông qua Telegram.
* Nhận kết quả đầu ra trực tiếp trên Telegram.
* Thông báo lỗi khi thực thi thất bại.
* Giới hạn quyền truy cập bằng Admin ID.

## Yêu cầu hệ thống

* Python 3.10 trở lên
* Telegram Bot Token

## Cài đặt

### Cách 1: Sử dụng uv (Khuyên dùng)

```bash
# Tạo môi trường ảo và cài đặt thư viện
uv venv
uv sync

# Chạy bot
uv run main.py
```

### Cách 2: Sử dụng pip

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate
# Kích hoạt (Linux/macOS)
source .venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy bot
python main.py
```

## Cấu hình

Thiết lập các biến môi trường sau:

* `TELEGRAM_TOKEN`: Bot token từ @BotFather.
* `TELEGRAM_ADMIN_ID`: ID Telegram của bạn.

## Các lệnh

* `/start` - Hiển thị hướng dẫn.
* `/ping` - Kiểm tra trạng thái bot.
* `/run <file.py>` - Chạy file Python (Chỉ dành cho Admin).
* `/log` - Xem 20 dòng log cuối (Chỉ dành cho Admin).
* `/status` - Xem trạng thái bot.

## Lưu ý bảo mật

* Không bao giờ chia sẻ hoặc commit `TELEGRAM_TOKEN`.
* Luôn sử dụng biến môi trường cho thông tin nhạy cảm.

## Giấy phép

MIT License
