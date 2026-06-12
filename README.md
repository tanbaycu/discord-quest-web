<div align="center">
  <img src="https://raw.githubusercontent.com/tanbaycu/discord-quest-web/main/static/logo.png" alt="Discord Quest Web Logo" width="150" />
  <h1>🚀 Discord Quest Auto <br/> <span style="color: #00e676;">Web UI Edition V2.0</span></h1>
  
  <p align="center">
    <b>🏆 Giải pháp tối thượng để farm phần thưởng Discord Quest hoàn toàn tự động!</b>
  </p>
  
  <p align="center">
    <img src="https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge&logo=discord" alt="Status">
    <img src="https://img.shields.io/badge/Security-100%25_Safe-blue.svg?style=for-the-badge" alt="Security">
    <img src="https://img.shields.io/badge/UI-Remastered-purple.svg?style=for-the-badge" alt="UI">
    <img src="https://img.shields.io/badge/License-Non_Commercial-red.svg?style=for-the-badge" alt="License">
  </p>
</div>

---

## 🔥 Đột Phá Công Nghệ (Why Choose This?)

Tạm biệt những ngày tháng tải game hàng chục GB, lụi cụi mở game treo máy tốn điện, hay căng mắt nhìn những dòng code khô khan trên cửa sổ đen sì (CLI). Bản **Web UI Remastered** mang đến trải nghiệm Đỉnh Cao (Peak Experience):

- 🎨 **Giao Diện Siêu Việt (Glassmorphism):** Trải nghiệm thị giác đỉnh cao với dark mode huyền bí, hiệu ứng bóng kính sang trọng và animation mượt mà (Lenis Scroll).
- ⚡ **Zero Setup & Cloud-Based:** Không cài thêm bất cứ phần mềm hay game nào. Chạy trực tiếp trên trình duyệt, có thể host lên server để tự farm 24/7.
- 🔰 **Bookmarklet Tiên Tiến (1-Click Token):** Không cần F12, không cần Developer Console. Lấy Token Discord chỉ với 1 cú kéo thả Dấu Trang (Bookmark) hoặc 1 nút bấm trên điện thoại.
- 🎮 **Bảng Điều Khiển Console Sinh Động:** Terminal log ngay trên nền web với Progress Bar (thanh tiến trình) và các thông báo "chuẩn game thủ" tấu hài cực mạnh.
- 🔒 **Bảo Mật Tối Đa:** Token của bạn **chỉ tồn tại trên RAM trình duyệt của bạn**. Mã nguồn mở cam kết 100% không lưu trữ, không gửi Token về bất kỳ máy chủ nào khác ngoài Discord.

---

## 🚀 Hướng Dẫn Khởi Động Nhanh (Quick Start)

### 1. Trải Nghiệm & Lấy Token (Dành cho Người Dùng)
1. Truy cập vào trang web của chúng tôi (hoặc localhost nếu bạn tự host).
2. Tới phần **Hướng dẫn lấy Token** -> Chọn phương pháp cực dễ:
   - **🖥️ PC:** Nắm kéo nút xanh lên thanh Bookmark (Dấu trang) -> Qua tab Discord bấm 1 phát lấy token luôn!
   - **📱 Mobile:** Copy đoạn mã -> Qua tab Discord -> Gõ `javascript:` vào thanh địa chỉ rồi dán mã vào là xong!
3. Dán Token vào Web và nhấn **🚀 START QUEST**. Xong! Ngồi rung đùi húp quà.

### 2. Triển Khai (Dành cho Admin / Developer)
Dự án được tối ưu siêu nhẹ bằng Python (Flask) để dễ dàng deploy lên bất kỳ đâu:
```bash
# 1. Clone repository
git clone https://github.com/tanbaycu/discord-quest-web.git
cd discord-quest-web

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Chạy server
python app.py
```
> 👉 *Truy cập `http://localhost:5000` và tận hưởng! Phù hợp deploy lên Render, Railway, VPS, Heroku...*

---

## 🛠️ Công Nghệ Lõi (Tech Stack)

- **Backend:** Python 3, Flask, Requests (Siêu nhẹ, tốc độ phản hồi tính bằng ms)
- **Frontend:** HTML5, TailwindCSS (JIT), Vanilla JS, Lenis Scroll (60fps Animation)
- **Tối Ưu:** Responsive 100% Mobile First, SEO Meta Tags đầy đủ.

---

## 📝 Bản Quyền & Lời Cảm Ơn (Credits)

Dự án này là sự kết tinh từ đam mê mã nguồn mở:
- 👑 **Original CLI Core:** [@thanhdo1110](https://github.com/thanhdo1110/Discord-Quest-Auto-Completer) - Tác giả của bộ khung logic gửi gói tin siêu việt. Đừng quên cho bác ấy 1 sao nhé!
- 🎨 **Web UI & UX Remaster:** [@tanbaycu](https://github.com/tanbaycu) - Đập đi xây lại toàn bộ giao diện, đưa trải nghiệm người dùng lên tầm cao mới với các trick lấy token cực kỳ tiện dụng.

<div align="center">
  <br>
  <b>Made with 💚 and ☕ by TanBayCu</b>
  <br>
  <i>⚠️ Lưu ý: Tuyệt đối không sử dụng dự án này cho mục đích thương mại.</i>
</div>
