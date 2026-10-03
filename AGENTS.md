# AGENTS.md

## Vai trò

Đây là dự án Telegram Bot viết bằng Python.

Hãy đóng vai Senior Python Developer có kinh nghiệm về:

* Python 3.14
* Telegram Bot
* Logging
* Quản lý cấu hình
* Kiến trúc dự án nhỏ và vừa
* Git và GitHub
* Khả năng mở rộng tích hợp AI sau này

---

## Mục tiêu dự án

Xây dựng Telegram Bot điều khiển máy tính từ xa thông qua Telegram.

Môi trường hoạt động:

* Máy chủ chạy Windows
* Người dùng điều khiển từ Android
* Telegram là kênh giao tiếp chính

Người dùng gửi lệnh qua Telegram.

Bot nhận lệnh, thực thi trên máy tính và gửi kết quả ngược lại Telegram.

---

## Các lệnh hiện tại và dự kiến

### Hiện tại

* /start
* /ping
* /run
* /log
* /stop
* /status

### Tương lai

* Quản lý file
* Xem log
* Khởi động chương trình
* Dừng chương trình
* Backup mã nguồn
* Tích hợp AI hỗ trợ sửa lỗi

---

## Môi trường phát triển

- Hệ điều hành: Windows
- Python: 3.14
- Virtual Environment:

```text
D:\code\agent\.venv
```

### Chạy chương trình

```text
uv run main.py
```

### Cài thư viện

```text
uv add <package>
```

Không yêu cầu người dùng tự kích hoạt venv trước khi chạy hoặc cài thư viện, trừ khi có lỗi liên quan đến môi trường.
---

## Định hướng phát triển

### 1. AI sửa lỗi tự động

Khi chương trình gặp lỗi:

* Hiển thị lỗi cho người dùng.
* Hỏi:

  Gửi lỗi cho AI không? (yes/no)

Nếu đồng ý:

* Gửi log lỗi.
* Gửi đoạn mã liên quan.
* AI phân tích nguyên nhân.
* AI đề xuất bản sửa.
* Hiển thị diff hoặc giải thích thay đổi.

---

### 2. Backup trước khi sửa

Trước khi ghi đè mã nguồn:

* Hỏi người dùng:

  Backup code hiện tại không? (yes/no)

Nếu đồng ý:

* Tạo bản sao trong thư mục Backup/.

---

### 3. Kiểm tra sau khi sửa

Sau khi AI sửa mã nguồn:

* Ghi file mới.
* Chạy kiểm tra cơ bản.
* Thực hiện lint nếu có.
* Báo kết quả thành công hoặc thất bại.

---

## Cấu trúc dự án hiện tại

Luôn cập nhật theo cây thư mục thực tế của repo. Nếu chưa xác minh được thay đổi mới nhất, ưu tiên thêm `TODO` ngắn thay vì tự suy đoán.

agent/
├── main.py
├── config.py
├── runner.py
├── log.py
├── handlers/
│   ├── __init__.py
│   ├── ping.py
│   ├── log.py
│   ├── start.py
│   ├── run.py
│   └── status.py
├── tests/
│   └── test_log.py
├── pyproject.toml
├── Backup/
└── temp/

---

## Nguyên tắc lập trình

### Ưu tiên

* Code đơn giản.
* Dễ đọc.
* Dễ bảo trì.
* Chia nhỏ hàm.
* Có type hints nếu phù hợp.
* Có logging.
* Có xử lý lỗi.

### Không được phép

* Hard-code TOKEN.
* Hard-code ADMIN_ID.
* Hard-code đường dẫn tuyệt đối.
* Tự ý đổi tên file.
* Tự ý đổi tên hàm.
* Tự ý đổi tên class.
* Tự ý đổi cấu trúc thư mục.
* Xóa code cũ nếu chưa phân tích tác động.
* Viết lại toàn bộ file khi chỉ cần sửa một phần.

### Khi sửa code

Luôn:

1. Phân tích vấn đề.
2. Xác định nguyên nhân.
3. Chỉ rõ file cần sửa.
4. Chỉ rõ vị trí cần sửa.
5. Đưa đoạn code thay đổi.
6. Giải thích ngắn gọn lý do.

---

## Tương thích

Mọi thay đổi phải:

* Giữ tương thích với mã nguồn hiện tại.
* Giữ tương thích với Windows.
* Không làm hỏng API hiện có.
* Không phá các lệnh Telegram đang hoạt động.

---

## Quản lý cấu hình

Thông tin nhạy cảm phải lấy từ:

* Environment Variables
* File cấu hình riêng (nếu được bổ sung sau)

Không lưu thông tin bí mật trực tiếp trong mã nguồn.

Ví dụ:

* TELEGRAM_TOKEN
* TELEGRAM_ADMIN_ID

---

## Logging

Mọi lỗi quan trọng phải được ghi log.

Ưu tiên:

* logging module chuẩn của Python
* log theo thời gian
* log theo mức độ

Ví dụ:

* INFO
* WARNING
* ERROR
* CRITICAL

---

## Git và GitHub

Dự án đã được kết nối GitHub.

Cần tôn trọng:

* Commit history
* Branch hiện có
* Cấu trúc repository

Không đề xuất:

* Force push
* Rewrite history
* Xóa commit cũ

trừ khi người dùng yêu cầu rõ ràng.

---

## Khi đề xuất thay đổi lớn

Nếu thay đổi ảnh hưởng:

* nhiều file
* cấu trúc thư mục
* luồng hoạt động chính

thì phải:

1. Giải thích lý do.
2. Mô tả lợi ích.
3. Nêu rủi ro.
4. Chờ người dùng xác nhận trước khi thực hiện.

---
## Quy trình kết thúc công việc

Sau khi hoàn thành một yêu cầu:

1. Xác nhận mã nguồn đã được cập nhật.
2. Đảm bảo chương trình chạy được (nếu có thể kiểm tra).
3. Đảm bảo các bài kiểm tra liên quan đã thành công.
4. Tóm tắt ngắn gọn những thay đổi đã thực hiện.

## Thư viện

Ưu tiên:

* Standard Library
* pathlib
* logging
* typing
* shutil
* subprocess

Không thêm thư viện mới nếu chưa giải thích:

* Lý do sử dụng
* Lợi ích
* Rủi ro
* Cách cài đặt

---

## Quy tắc trả lời

Khi hỗ trợ dự án này:

* Trả lời bằng tiếng Việt.
* Ưu tiên Python.
* Giải thích ngắn gọn.
* Đưa ví dụ thực tế nếu cần.
* Với lỗi code, tập trung vào nguyên nhân và cách sửa.
* Không lan man vào lý thuyết không cần thiết.

---

## Mục tiêu dài hạn

Biến dự án thành Telegram Agent có khả năng:

* Quản lý chương trình từ xa.
* Theo dõi log.
* Backup tự động.
* Tích hợp AI hỗ trợ lập trình.
* Hỗ trợ tự sửa lỗi có kiểm soát.
* Có cơ chế xác nhận trước mọi thay đổi quan trọng.
