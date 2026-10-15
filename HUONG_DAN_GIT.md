# 📖 HƯỚNG DẪN ĐẨY CODE LÊN GITHUB & CƠ CHẾ TỰ ĐỘNG CẬP NHẬT GAME

Tài liệu này hướng dẫn chi tiết cách đưa dự án game lên GitHub và cách hệ thống tự động kiểm tra phiên bản mới để cập nhật mã nguồn trực tiếp từ Git.

---

## PHẦN 1: CÁC FILE KIỂM TRA PHIÊN BẢN ĐÃ CÓ TRONG DỰ ÁN

Trong thư mục gốc dự án đã có sẵn các file phục vụ hệ thống cập nhật:
1. [version.json]: Chứa thông tin số phiên bản hiện tại (`version: "1.1.0"`), ngày phát hành, changelog và đường dẫn repository.
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
git remote add origin https://github.com/<tên_tài_khoản_của_bạn>/game_test_3d.git

# 3. Chọn toàn bộ file trong dự án
git add .

# 4. Lưu lại bản commit đầu tiên
git commit -m "Phát hành phiên bản Little DaNang v1.1.0"

# 5. Đẩy code lên nhánh main
git push -u origin main
```

---

## PHẦN 4: CƠ CHẾ BẤM "CẬP NHẬT" TỰ ĐỘNG LẤY BẢN MỚI TỪ GIT

### 1. Khi bạn (nhà phát triển) ra mắt tính năng mới:
1. Mở file [version.json](file:///c:/vinhnq/game_test_3d/version.json):
   - Nâng số phiên bản: ví dụ `"version": "1.2.0"`, `"version_code": 120`.
   - Cập nhật nội dung các tính năng mới vào mục `"changelog"`.
2. Đẩy lên Git bằng cách chạy file [git_setup_and_push.bat](file:///c:/vinhnq/game_test_3d/git_setup_and_push.bat) (hoặc `git add .`, `git commit -m "v1.2.0"`, `git push origin main`).

### 2. Người chơi trong game:
1. Mở game lên -> Chọn **🚀 Cập nhật game**.
2. Nhấn nút **🔄 Kiểm Tra Cập Nhật**:
   - Game sẽ tự động kết nối và so khớp `version.json` trên Git hoặc kiểm tra commit mới nhất.
   - Nếu có bản cập nhật mới, nút **⬇️ Cập Nhật Ngay (Git Pull)** sẽ sáng lên.
3. Nhấn **⬇️ Cập Nhật Ngay (Git Pull)**:
   - Game tự động kéo mã nguồn và tài nguyên mới nhất về máy qua `git pull`.
   - Sau khi hoàn thành, màn hình hiện thông báo thành công và cung cấp nút **Khởi động lại game** để người chơi trải nghiệm ngay!
