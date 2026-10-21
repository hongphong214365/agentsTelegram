# AgentsTelegram: Telegram Agent điều khiển máy tính từ xa

Bot Telegram chạy trên máy tính của bạn, cho phép gửi lệnh từ Telegram và nhận kết quả ngay trên thiết bị đang sử dụng.

[English](README_EN.md)

## Tính năng

* Thực thi file Python từ xa bằng Telegram.
* Tùy chỉnh cấu hình như thời gian timeout, số dòng log và cấp độ log.
* Giới hạn các lệnh quản trị theo Telegram user ID đã cấu hình.
* Gửi kết quả thực thi hoặc thông báo lỗi về Telegram trên điện thoại, PC và các thiết bị khác.
* Ghi nhật ký hoạt động và hỗ trợ xem, lọc, đổi cấp độ hoặc dọn log.

## Yêu cầu

* Python 3.14.
* Telegram bot token.
* Kết nối Internet để bot liên lạc với Telegram.
* Telegram user ID của bạn để giới hạn quyền truy cập.

## Cài đặt

### Cách 1: Dùng uv (khuyên dùng)

```bash
# Tạo môi trường ảo và cài thư viện
uv venv
uv sync

# Chạy bot
uv run main.py
```

### Cách 2: Dùng pip

Tạo và kích hoạt môi trường ảo:

```bash
python -m venv .venv
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Cài thư viện và chạy bot:

```bash
pip install -r setup/requirements.txt
python main.py
```

## Cấu hình

### 1. Tạo bot và lấy token

Mở Telegram, trò chuyện với [@BotFather](https://t.me/BotFather), tạo bot mới bằng `/newbot` và làm theo hướng dẫn. Lưu token BotFather cung cấp ở nơi riêng tư.

### 2. Lấy Telegram user ID

Lấy **ID dạng số của tài khoản Telegram cá nhân** từ một bot tra cứu ID đáng tin cậy. Không dùng username, tên hiển thị hoặc ID của bot thay cho user ID của bạn.

### 3. Tạo hai biến môi trường

Ứng dụng chỉ đọc hai biến môi trường sau:

* `TELEGRAM_TOKEN`: token bot lấy từ BotFather.
* `TELEGRAM_ADMIN_ID`: Telegram user ID dạng số của bạn.

Thay các giá trị mẫu bên dưới bằng giá trị của bạn. Lệnh này chỉ đặt biến cho phiên terminal hiện tại.

**Windows (CMD):**

```cmd
set TELEGRAM_TOKEN=your_bot_token
set TELEGRAM_ADMIN_ID=123456789
```

**Windows (PowerShell):**

```powershell
$env:TELEGRAM_TOKEN = "your_bot_token"
$env:TELEGRAM_ADMIN_ID = "123456789"
```

**macOS:**

```bash
export TELEGRAM_TOKEN="your_bot_token"
export TELEGRAM_ADMIN_ID="123456789"
```

**Linux:**

```bash
export TELEGRAM_TOKEN="your_bot_token"
export TELEGRAM_ADMIN_ID="123456789"
```

Chạy bot trong chính terminal đã đặt biến môi trường. Muốn cấu hình lâu dài, hãy thêm biến vào thiết lập môi trường riêng của hệ điều hành; không ghi token vào mã nguồn hoặc commit lên Git.

### 4. Tùy chỉnh cấu hình khác (nếu cần)

Trong `config.py`, bạn có thể điều chỉnh `RUN_TIMEOUT` (mặc định 30 giây), `LOG_LINES` (20 dòng mặc định), `LOG_FILE` (mặc định `temp/agent.log`) và `LEVEL` (mặc định `INFO`). Hãy dừng bot trước khi sửa rồi khởi động lại để áp dụng.

## Sử dụng bot

### Chạy bot

Mở terminal tại thư mục dự án, đặt hai biến môi trường ở phần Cấu hình rồi chạy:

```bash
uv run main.py
```

Nếu cài bằng pip, kích hoạt môi trường ảo rồi chạy `python main.py`. Khi khởi động thành công, bot in:

```text
Telegram agent started successfully.
```

### Lệnh được hỗ trợ

* `/start` — Chào mừng và hiển thị hướng dẫn sử dụng.
* `/run tenfile.py` — Chạy file `.py` nằm trong thư mục dự án hiện tại; kết quả hoặc lỗi được gửi lại Telegram. Lệnh có thời gian chờ tối đa theo `RUN_TIMEOUT` và có khoảng nghỉ chống spam 15 giây giữa các lần chạy.
* `/log` — Xem 20 dòng log gần nhất (mặc định). Chỉ quản trị viên đã cấu hình mới dùng được.
* `/status` — Xem thư mục hiện tại, phiên bản Python, đường dẫn file log và timeout (**thử nghiệm**).
* `/ping` — Kiểm tra nhanh, bot trả lời `online`.

Các tùy chọn `/log` (ghép với `/log` trong một tin nhắn):

| Cú pháp | Tác dụng |
| --- | --- |
| `/log 50`, `/log -lines=50`, `/log --lines=50`, `/log -n=50` | Xem số dòng cuối chỉ định; số dòng tối thiểu là 1. |
| `/log -level=ERROR` hoặc `/log --level=ERROR` | Chỉ xem log theo cấp độ, ví dụ `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |
| `/log -time=11:09` hoặc `/log --time=11:09` | Lọc theo chuỗi thời gian xuất hiện trong dấu thời gian của log. |
| `/log -get-level`, `/log --get-level`, `/log -current-level`, `/log --current-level` | Xem cấp độ log hiện tại. |
| `/log -set-level=DEBUG` hoặc `/log --set-level=DEBUG` | Đổi cấp độ log khi bot đang chạy. |
| `/log -clean` hoặc `/log --clean` | Xóa nội dung file log. |

Các thao tác xem, lọc, đổi cấp độ và dọn log đều yêu cầu Telegram user ID quản trị đã cấu hình.

Lưu ý: `/ping` hiện trả lời mọi tài khoản Telegram; các lệnh còn lại chỉ xử lý yêu cầu từ ID đã cấu hình.

## Lưu ý bảo mật

> **CẢNH BÁO NGHIÊM TRỌNG: TELEGRAM TOKEN CÓ THỂ TOÀN QUYỀN ĐIỀU KHIỂN BOT CỦA BẠN.**
>
> **KHÔNG chia sẻ token dưới bất kỳ hình thức nào:** không push lên GitHub, không gửi cho bạn bè, không đăng ảnh chụp màn hình có token, không dán vào nơi công cộng và không gửi token trong cuộc trò chuyện. Ai có token có thể chiếm quyền điều khiển bot. Nếu token bị lộ, hãy thu hồi/tạo token mới ngay qua BotFather. Bạn tự chịu trách nhiệm bảo vệ token và hậu quả từ việc để lộ token.

* Không gửi token hoặc log chứa thông tin nhạy cảm cho người khác.
* Đặt `TELEGRAM_ADMIN_ID` đúng ID cá nhân; chỉ chia sẻ bot với người bạn tin cậy.
* `/run` thực thi mã Python trên máy đang chạy bot. Chỉ chạy bot trên máy bạn kiểm soát và chỉ gửi lệnh cho bot từ tài khoản đã cấu hình.
* Không chạy file `.py` không rõ nguồn gốc; mã độc có thể đọc, sửa hoặc xóa dữ liệu trong phạm vi quyền của tài khoản chạy bot.
* Cập nhật Python và các thư viện, đồng thời bảo vệ máy tính và tài khoản hệ điều hành bằng mật khẩu phù hợp.

## License

MIT License. Xem [LICENSE](LICENSE).
