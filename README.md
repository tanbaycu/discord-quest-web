# Discord Quest Auto - Web UI Edition

Dự án tự động hóa quá trình nhận phần thưởng Discord Quest thông qua giao diện Web. 

## Giới Thiệu
Đây là phiên bản Web UI được nâng cấp từ công cụ CLI gốc. Với bản cập nhật này, người dùng không cần cài đặt thêm phần mềm, chỉ cần thao tác trực tiếp trên trình duyệt để treo và nhận thưởng.

### Các Tính Năng Nổi Bật:
- **Giao diện hiện đại:** Được tối ưu hóa UI/UX với GSAP và các hiệu ứng mượt mà.
- **Không yêu cầu cài đặt:** Hoạt động hoàn toàn trên trình duyệt, có thể triển khai lên server cá nhân.
- **Tiện ích lấy Token nhanh:** Hỗ trợ lấy Token bằng thao tác kéo thả (Bookmarklet) hoặc copy mã trên cả PC và Mobile.
- **Độ tin cậy cao:** Tích hợp Web Worker và Wake Lock API giúp chống "ngủ đông" tab và chống tắt màn hình khi treo trên điện thoại.
- **Bảo mật:** Token chỉ được xử lý cục bộ, không lưu trữ trên máy chủ.

---

## Hướng Dẫn Sử Dụng
1. Truy cập vào trang web (hoặc localhost nếu tự host).
2. Tới phần **Hướng dẫn lấy Token** và làm theo các bước trên PC hoặc Mobile.
3. Dán Token vào ô nhập và nhấn **Bắt Đầu**.
4. Treo máy và chờ hệ thống hoàn thành tự động.

---

## Dành Cho Developer
Dự án được xây dựng dựa trên Python (Flask) và Vanilla JS.

### Cài đặt và Khởi chạy
```bash
# 1. Clone repository
git clone https://github.com/tanbaycu/discord-quest-web.git
cd discord-quest-web

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Chạy server
python app.py
```
Sau đó truy cập `http://localhost:5000`.

---

## Bản Quyền & Tác Giả
- **Original CLI Core:** [thanhdo1110](https://github.com/thanhdo1110/Discord-Quest-Auto-Completer)
- **Web UI & UX Remaster:** [tanbaycu](https://github.com/tanbaycu)

*Lưu ý: Dự án mã nguồn mở, không sử dụng cho mục đích thương mại.*
