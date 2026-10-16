# 📖 HƯỚNG DẪN ĐẨY CODE LÊN GITHUB & CƠ CHẾ TỰ ĐỘNG CẬP NHẬT GAME

Tài liệu này hướng dẫn chi tiết cách đưa dự án game lên GitHub và cách hệ thống tự động kiểm tra phiên bản mới để cập nhật mã nguồn trực tiếp từ Git.

---

## PHẦN 1: CÁC FILE KIỂM TRA PHIÊN BẢN ĐÃ CÓ TRONG DỰ ÁN

Trong thư mục gốc dự án đã có sẵn các file phục vụ hệ thống cập nhật:
1. [version.json]: Chứa thông tin số phiên bản hiện tại (`version: "1.3.0"`), ngày phát hành, changelog và đường dẫn repository.
2. [update_game.bat]: Kịch bản tự động chạy lệnh `git pull` để tải mã nguồn mới nhất từ GitHub về máy.
3. [git_setup_and_push.bat]: Công cụ 1-click tự động khởi tạo Git, thêm remote và đẩy toàn bộ code lên GitHub.
4. [.gitignore]: Đã cấu hình loại trừ bộ nhớ tạm `.godot/`, log, bản build nặng để Git luôn nhẹ và sạch sẽ.

---

## PHẦN 2: HƯỚNG DẪN TẠO KHO LƯU TRỮ TRÊN GITHUB (1 PHÚT)

1. Truy cập vào **[https://github.com/new](https://github.com/new)** (Đăng nhập tài khoản GitHub của bạn).
2. Điền thông tin tạo kho mới:
   - **Repository name**: `game_test_3d` (hoặc tên tùy thích).
   - Chọn **Public** (hoặc **Private** tùy bạn).
   - ⚠️ **LƯU Ý QUAN TRỌNG**: **KHÔNG** tích chọn ô *"Add a README file"*, *"Add .gitignore"*, hay *"Choose a license"*, vì dự án ở máy bạn đã có sẵn các file này rồi!
3. Nhấn nút xanh **Create repository**.
4. GitHub sẽ hiện ra một trang chứa đường dẫn kho, có dạng:
   ```text
   https://github.com/<tên_tài_khoản_của_bạn>/game_test_3d.git
   ```
   👉 Hãy copy lại đường dẫn này.

---

## PHẦN 3: ĐẨY CODE LÊN GITHUB (CHỌN 1 TRONG 2 CÁCH)

### Cách A: Dùng file tự động (Khuyên dùng - Nhanh nhất)
1. Trong thư mục dự án, bạn nhấp đúp chạy file **[git_setup_and_push.bat](file:///c:/vinhnq/game_test_3d/git_setup_and_push.bat)**.
2. File sẽ hỏi bạn dán link GitHub Repository vừa copy ở Bước 2 vào.
3. Nhập ghi chú commit (hoặc bấm Enter để dùng mặc định).
4. Chương trình sẽ tự động `git add`, `git commit` và `git push` toàn bộ code lên nhánh `main` của GitHub!
*(Nếu máy chưa đăng nhập GitHub, một cửa sổ đăng nhập sẽ hiện lên để bạn xác thực).*

---

### Cách B: Dùng dòng lệnh Git thủ công (Dành cho ai muốn gõ lệnh)
Mở cửa sổ Command Prompt (hoặc PowerShell / Git Bash) tại thư mục dự án `game_test_3d` và gõ lần lượt các lệnh sau:

```bash
# 1. Khởi tạo Git nếu chưa có
git init
git branch -M main

# 2. Thêm liên kết với GitHub Repository của bạn
# (Thay đường dẫn bên dưới bằng link repo của bạn)
git remote add origin https://github.com/zinh8803/FARM.git

# 3. Chọn toàn bộ file trong dự án
git add .

# 4. Lưu lại bản commit đầu tiên
git commit -m "Phát hành phiên bản Little DaNang v1.3.0"

# 5. Đẩy code lên nhánh main
git push -u origin main
```

---

## PHẦN 4: CẬP NHẬT BẢN GAME ĐÃ EXPORT QUA GITHUB RELEASES

### 1. Phát hành phiên bản mới:
1. Trong `version.json`, tăng `version` (ví dụ `1.3.1`) và cập nhật `changelog`.
2. Commit và push mã nguồn lên nhánh `main` trước khi phát hành.
3. Cài GitHub CLI (`gh`) trên máy xuất bản và đăng nhập một lần bằng `gh auth login`.
4. Chạy `export_game.bat`, chọn `Y` ở câu hỏi tạo GitHub Release. Script export `LittleDaNang.exe`, PCK nền, các patch PCK, SHA-256 và `update_manifest.json` lên release có tag `v` + version.
5. Bản chuyển tiếp đầu tiên có các patch PCK đầy đủ để người đang ở 1.1.2, 1.3, 1.3.1, 1.4 hoặc 1.4.1 nhảy thẳng tới phiên bản mới; các bản kế tiếp dùng patch nối chuỗi.

### 2. Người chơi cập nhật:
1. Chỉ cần tải và chạy `LittleDaNang.exe`; không cần cài Git, clone repository hay có thư mục `.git`.
2. Các bản cũ cập nhật một lần lên executable mới. Sau đó, nút **🚀 Cập nhật game** đọc `update_manifest.json`, tải các PCK theo chuỗi phiên bản, xác minh SHA-256 và khởi động lại để nạp patch.

Mỗi release cần có `LittleDaNang.exe`, `update_manifest.json`, PCK nền và các PCK được manifest tham chiếu. Game cần kết nối Internet; PCK được lưu trong thư mục dữ liệu người dùng. Nếu GitHub báo tag đã tồn tại, tăng version trước khi xuất bản phiên bản kế tiếp.
