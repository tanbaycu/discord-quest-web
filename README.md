# Discord Quest Auto Completer - Web UI Edition

Ứng dụng web tự động hóa quy trình phát luồng giả lập và hoàn thành các thử thách nhiệm vụ (Discord Quests) một cách an toàn và tối ưu. Dự án được phát triển dựa trên việc cải tiến nhân xử lý cốt lõi của thanhdo1110, kết hợp giao diện quản trị 3D trực quan và hiện đại được thiết kế bởi tanbaycu.

---

## Kiến Trúc Hệ Thống và Công Nghệ Cốt Lõi

Ứng dụng được thiết kế theo mô hình Client-Server gọn nhẹ, phân tách rõ rệt giữa logic xử lý API Discord và giao diện điều khiển của người dùng.

### 1. Backend (Flask Engine)
*   **API Wrapper:** Gửi các truy vấn HTTPS mô phỏng Client Discord để tương tác trực tiếp với các endpoint của Discord (`/quests/@me`, `/quests/{id}/enroll`, `/quests/{id}/heartbeat`, v.v.).
*   **Static Asset Caching:** Tối ưu hóa bộ nhớ đệm phía trình duyệt bằng việc cấu hình tiêu đề phản hồi `Cache-Control` cho các tài nguyên tĩnh (`/static/*`), giảm thiểu độ trễ tải trang và tiết kiệm tài nguyên máy chủ.

### 2. Frontend (Tactile 3D & Glassmorphism)
*   **Skeuomorphic Design:** Áp dụng phong cách thiết kế nút nhấn vật lý 3D kết hợp hiệu ứng chiều sâu và đổ bóng rõ nét, mang lại trải nghiệm phản hồi xúc giác chân thực.
*   **GSAP Animation Engine:** Tích hợp GreenSock Animation Platform để xử lý các chuyển động mượt mà, tối ưu hóa hiệu năng render đồ họa của trình duyệt.
*   **Responsive Layout:** Giao diện được thiết kế tương thích hoàn toàn từ màn hình máy tính kích thước lớn đến các thiết bị di động màn hình hẹp.

### 3. Client-Side Optimization (Tối ưu hóa phía khách)
*   **Web Workers Threading:** Sử dụng luồng chạy nền riêng biệt của trình duyệt để duy trì kết nối heartbeat liên tục, ngăn ngừa hiện tượng đóng băng tiến trình (background throttling) khi người dùng ẩn tab hoặc chuyển ứng dụng khác.
*   **Wake Lock API Integration:** Yêu cầu trình duyệt giữ thiết bị không chuyển sang chế độ ngủ (sleep) hoặc tắt màn hình khi đang thực hiện tiến trình tự động treo.
*   **Console Repaint Cap:** Giới hạn hiển thị tối đa 100 dòng nhật ký log mới nhất tại giao diện điều khiển nhằm giảm tải số lượng phần tử DOM, hạn chế tối đa việc tiêu tốn RAM và tải xử lý của GPU trong thời gian dài.
*   **Preconnect CDNs:** Cấu hình preconnect đến các máy chủ phân phối nội dung (CDNs) của Google Fonts, TailwindCSS, và GSAP để rút ngắn thời gian phân giải DNS và tải tài nguyên ban đầu lên đến 30%.

---

## Các Tính Năng Nổi Bật

*   **Bảng Nhiệm Vụ Trực Quan (Visual Quest Board):** Tải và hiển thị toàn bộ danh sách các thử thách hiện có trên tài khoản Discord của người dùng đi kèm trạng thái cụ thể: ĐÃ XONG, ĐANG TREO, hoặc KHẢ DỤNG.
*   **Hiệu Ứng Skeleton Loading:** Áp dụng hiệu ứng bộ khung tải giả lập phát sáng trong thời gian kết nối và đồng bộ dữ liệu ban đầu.
*   **Thanh Tiến Trình Thời Gian Thực (Progress Bar):** Hiển thị thanh đo tiến độ hoàn thành dạng 3D gradient, cập nhật chỉ số phần trăm hoàn thành và thời gian đếm ngược chính xác theo từng giây.
*   **Hệ Thống Lấy Token Thông Minh:** Tích hợp Bookmarklet tương thích với cả PC và thiết bị di động, tự động hóa việc trích xuất khóa định danh Discord (Authorization Token) và sao chép trực tiếp vào bộ nhớ tạm bằng một cú click chuột.
*   **Tích Hợp Chatbot Telegram:** Liên kết trực tiếp với chatbot vệ tinh @ngocmaicute_bot để hỗ trợ người dùng treo nhiệm vụ trực tiếp trên đám mây 24/7 mà không cần bật máy tính hay điện thoại.

---

## Hướng Dẫn Cài Đặt và Khởi Chạy

### Yêu Cầu Hệ Thống
*   Môi trường chạy: Python 3.8 trở lên.
*   Trình duyệt web hỗ trợ tiêu chuẩn HTML5.

### Các Bước Triển Khai
1.  Tải mã nguồn dự án:
    ```bash
    git clone https://github.com/tanbaycu/discord-quest-web.git
    cd discord-quest-web
    ```
2.  Cài đặt các gói thư viện phụ thuộc:
    ```bash
    pip install -r requirements.txt
    ```
3.  Khởi động máy chủ phát triển nội bộ:
    ```bash
    python app.py
    ```
4.  Truy cập ứng dụng:
    Mở trình duyệt bất kỳ và truy cập đường dẫn: `http://localhost:5000`

---

## Hướng Dẫn Sử Dụng Chi Tiết

### Bước 1: Trích Xuất Khóa Định Danh (Discord Token)
*   **Phương thức thủ công (PC):** Đăng nhập Discord trên trình duyệt -> Nhấn phím `F12` mở Developer Tools -> Tab `Network` -> Nhập `/api/` vào bộ lọc -> Chọn một request bất kỳ -> Tìm và sao chép chuỗi mã ký tự tại trường `Authorization` trong Request Headers.
*   **Phương thức tự động (Bookmarklet - PC/Mobile):** 
    1.  Nhấp vào nút **Copy Mã Điện Thoại** tại giao diện hướng dẫn để lưu mã chạy tự động.
    2.  Truy cập trang Discord Web và đăng nhập.
    3.  Tại thanh địa chỉ của trang Discord Web, bạn tự gõ đúng từ khóa `javascript:` sau đó dán toàn bộ đoạn mã đã copy và nhấn phím Enter (hoặc nút Đi trên điện thoại).
    4.  Hệ thống sẽ hiển thị một thông báo 3D nảy lò xo xác nhận token đã được sao chép thành công.

### Bước 2: Kích Hoạt Tiến Trình Tự Động
1.  Quay trở lại giao diện web ứng dụng, dán đoạn Token vào ô nhập liệu.
2.  Nhấn nút **BẮT ĐẦU** màu xanh để hệ thống bắt đầu quét và treo Quest tự động.
3.  Để dừng lại bất kỳ lúc nào, bạn chỉ cần nhấn nút **DỪNG LẠI** màu đỏ.

---

## Tuyên Bố Bảo Mật & Bản Quyền

*   **Cam kết bảo mật:** Ứng dụng xử lý Token của người dùng hoàn toàn cục bộ tại phía Client và thực hiện các kết nối API HTTPS trực tiếp đến các endpoint của Discord hoặc thông qua máy chủ cục bộ tự chạy của người dùng. Hệ thống **tuyệt đối không thu thập, lưu trữ, hay gửi tiếp** thông tin Token của bạn về bất kỳ máy chủ bên thứ ba nào.
*   **Phân phối bản quyền:**
    *   Phát triển logic nhân xử lý gốc: [thanhdo1110](https://github.com/thanhdo1110)
    *   Thiết kế kiến trúc Web UI & UX: [tanbaycu](https://github.com/tanbaycu)
    *   *Dự án được phân phối mã nguồn mở phi thương mại dưới giấy phép MIT.*
