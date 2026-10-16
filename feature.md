# TÀI LIỆU THIẾT KẾ DỰ ÁN: LITTLE DANANG - NÔNG TRẠI LÀNG QUÊ VIỆT NAM (2D PIXEL ART RPG)

## 1. Tổng quan dự án

* **Tên dự án**: Little DaNang (Nông trại Làng quê Việt)
* **Thể loại**: 2D Farming Simulator & Top-down RPG Life Sim
* **Phong cách đồ họa**: Pixel Art 16-bit cổ điển, góc nhìn Top-down (nhìn từ trên xuống theo tỉ lệ 2.5D / Y-sort).
* **Bối cảnh**: Làng quê nông thôn Việt Nam yên bình (Đà Nẵng / Duyên hải Nam Trung Bộ). Khung cảnh tái hiện chân thực với nhà ba gian mái ngói đỏ rêu phong, giàn hoa leo, lu nước chum gốm, rặng tre xanh, vườn chuối sai quả, dây phơi áo quần mộc mạc, chuồng gà - vịt - lợn và những luống đất cày thẳng tắp.
* **Mục tiêu**: Người chơi hóa thân thành người nông dân đội nón lá áo bà ba, quản lý nông trại, cuốc đất trồng trọt, tưới cây, chăm sóc vật nuôi (gà, vịt, heo), giao tiếp với người dân trong làng, nhận nhiệm vụ và từng bước mở rộng cơ ngơi.

---

## 2. Công nghệ & Kiến trúc kỹ thuật

* **Game Engine**: Godot Engine 4.x (4.7.2 LTS).
* **Ngôn ngữ**: GDScript.
* **Độ phân giải hiển thị (Viewport Base)**: 640x360 (Pixel-perfect scale lên 1280x720 hoặc Full HD 1920x1080 mà không bị nhòe pixel, sử dụng texture filter Nearest).
* **Kiến trúc Scene & Nodes**:
  - `Main`: Node quản lý vòng lặp thế giới, hệ thống ánh sáng ngày/đêm và HUD.
  - `World / FarmMap`: Quản lý các lớp TileMapLayer (Terrain, Paths, PlowedSoil, Obstacles) và YSort node cho cây cối, nhà cửa, nhân vật, động vật.
  - `Player`: `CharacterBody2D` với animation 4 hướng, hệ thống Raycast / Interaction Area để tương tác vật thể và dùng nông cụ.
  - `Animals`: Động vật AI đơn giản (lang thang trong chuồng, mổ thóc, kêu, đẻ trứng).
  - `Crops`: Quản lý trạng thái từng ô đất (đất hoang -> đất cuốc -> gieo hạt -> tưới nước -> nảy mầm -> thu hoạch).
  - `DayNightCycle`: Đồng hồ thời gian và CanvasModulate chỉnh màu sắc theo buổi (Sáng, Trưa, Chiều, Tối).
  - `UI / HUD`: Thanh thời gian đỉnh màn hình, thẻ địa danh "Little DaNang", túi đồ (Inventory bar / Grid), bảng hội thoại và thông báo.

---

## 3. Thiết kế bản đồ chi tiết (Dựa theo ảnh tham khảo)

Bản đồ nông trại được chia thành các khu vực chức năng rõ ràng:

### 3.1. Khu nhà ở truyền thống (Tây Bắc - Góc trên bên trái)
* **Ngôi nhà chính**: Kiến trúc nhà truyền thống Việt Nam: mái ngói đỏ âm dương phủ rêu phong, hiên nhà lát gạch, cột gỗ, cửa gỗ mộc mạc.
* **Tiểu cảnh xung quanh**:
  - Giàn hoa giấy / hoa leo hồng tươi nở rộ trên mái hiên.
  - Lu nước / chum sành hứng nước mưa đặc trưng nông thôn.
  - Giàn gỗ leo cây bên hông nhà, chổi rơm quét sân, các chậu cây cảnh/xương rồng trước thềm.
  - Sân gạch đỏ dẫn ra lối đi chính.

### 3.2. Khu chuồng trại chăn nuôi (Tây Nam - Góc dưới bên trái)
* **Chuồng gia súc / gia cầm**: Nhà chuồng gỗ mái ngói/tôn có cửa chuồng, kho thóc rơm.
* **Khuôn viên bãi quây**: Hàng rào cọc gỗ quây quanh bãi đất cát vàng.
* **Vật nuôi & Tiện ích**:
  - Đàn gà (gà trống mào đỏ, gà mái mổ thóc).
  - Đàn vịt trắng lang thang kiếm ăn.
  - Chú heo hồng ủn ỉn trong bãi.
  - Đống rơm vàng truyền thống (nguồn thức ăn và rơm lót chuồng).
  - Máng ăn, chậu nước cho vật nuôi.

### 3.3. Khu vườn ruộng canh tác (Khu Trung tâm & Đông)
* **Khu đất luống cày (Tilled Soil Grid)**:
  - Hệ thống các ô đất vuông vức theo luống để gieo trồng các loại cây (lúa, ngô, dưa, rau màu nhiệt đới).
  - Trạng thái đất: Đất khô (nâu nhạt) -> Đất đã tưới nước (nâu đậm bóng) -> Đất có cây phát triển theo từng giai đoạn.
* **Khu đất hoang chưa khai khẩn**: Đất lẫn cỏ dại và sỏi đá vụn cần dùng cuốc/xẻng để làm cỏ và cuốc luống.
* **Bảng chỉ dẫn (Farm Signpost)**: Đặt ở đầu luống ruộng để kiểm tra thông tin nông trại.

### 3.4. Hệ sinh thái cây cối & Lối đi (Phía Bắc & Ven bản đồ)
* **Rặng tre trúc xanh**: Khóm tre cao vút ở bờ rào phía Bắc.
* **Vườn chuối Việt**: Những bụi chuối xanh tốt, trổ buồng chuối non và bắp hoa chuối đỏ tím.
* **Cây ăn quả**: Cây ổi, xoài, cam trĩu quả viền quanh lối đi.
* **Dây phơi quần áo thôn quê**: Dây treo áo xanh, đỏ, trắng phơi dưới nắng ấm.
* **Hệ thống đường đi**: Đường đất sỏi mộc mạc chạy dọc giữa bản đồ, phân nhánh nối liền nhà chính, chuồng trại và vườn ruộng.

---

## 4. Cơ chế Gameplay cốt lõi (Core Mechanics)

### 4.1. Điều khiển nhân vật
* Di chuyển 4 hướng (WASD hoặc Phím mũi tên).
* Nhân vật: Nông dân mặc áo bà ba vàng, quần nâu, đội nón lá Việt Nam.
* Animation di chuyển (Idle / Walk 4 hướng).
* Tương tác phím `E` hoặc `Space` (hoặc click chuột):
  - Khi đứng trước ô đất: Dùng công cụ (cuốc đất, tưới nước, gieo hạt, thu hoạch).
  - Khi đứng trước vật nuôi: Cho ăn, vuốt ve, nhặt trứng.
  - Khi đứng trước NPC: Bắt đầu đối thoại.

### 4.2. Hệ thống nông cụ & Trồng trọt (Farming System)
* **Nông cụ cơ bản**:
  1. *Cuốc (Hoe)*: Khai hoang đất cỏ thành ô đất canh tác có luống.
  2. *Bình tưới (Watering Can)*: Tưới ẩm các ô đất đã gieo hạt.
  3. *Gói hạt giống (Seeds)*: Gieo các loại hạt rau thơm, lúa, dưa, ngô vào ô đất ướt.
  4. *Liềm / Kéo thu hoạch (Sickle)*: Thu hoạch hoa màu chín và cắt cỏ khô làm rơm.
* **Vòng đời cây trồng**:
  - Gieo hạt -> Mầm nhỏ -> Cây non -> Ra hoa/kết trái -> Thu hoạch -> Cho ra nông sản trong túi đồ.

### 4.3. Hệ thống chăm sóc vật nuôi (Animal Husbandry)
* Gà và vịt di chuyển tự do trong khu rào quây.
* Hàng ngày có thể rải thóc vào máng ăn hoặc cho ăn rơm.
* Sau khi được chăm sóc đầy đủ, gà mái sẽ đẻ trứng vào buổi sáng để người chơi nhặt.
* Động vật phát ra tiếng kêu dễ thương và có hiệu ứng bong bóng biểu cảm (trái tim ❤️ khi được cho ăn).

### 4.4. Hệ thống chu kỳ Ngày/Đêm & Lịch thời gian
* **Thanh HUD thời gian (Top Bar)**:
  - Hiển thị chính xác như ảnh: `☀️ 11:40 - Thứ ba, 13/10 - Buổi trưa`.
  - Tốc độ thời gian game: 1 phút đời thực = 1 giờ trong game (hoặc tùy chỉnh).
  - Các buổi: Sáng sớm (06:00 - 10:00), Buổi trưa (10:00 - 14:00), Buổi chiều (14:00 - 18:00), Buổi tối (18:00 - 06:00).
  - Ánh sáng môi trường thay đổi mượt mà qua Shader / CanvasModulate (nắng vàng rực rỡ buổi trưa, ánh cam hoàng hôn lúc chiều tà, sắc lam tím huyền ảo ban đêm với đèn lồng phát sáng).
* **Thẻ địa danh (Bottom Right)**:
  - Hiển thị: `🌴 Little DaNang` với phong cách bảng gỗ/thẻ bo góc cổ điển.

---

## 5. Hệ thống NPC, Hội thoại & Nhiệm vụ

### 5.1. Các NPC mẫu
1. **Bác Ba (Trưởng thôn / Người dẫn đường)**:
   - Thường đứng gần cổng ngõ đón chào và hướng dẫn những bước đầu tiên về việc quản lý nông trại và làm quen hàng xóm.
2. **Cô Út (Chủ tiệm tạp hóa / Hạt giống chợ quê)**:
   - Cung cấp hạt giống rau, củ nhiệt đới, công cụ nâng cấp và thu mua nông sản tươi sống.
3. **Chú Năm (Người nuôi gia súc / Thợ mộc)**:
   - Hướng dẫn cách chăm sóc đàn gà vịt, đống rơm và cung cấp vật liệu sửa chữa nâng cấp chuồng trại.

### 5.2. Chuỗi nhiệm vụ nhập môn (Tutorial Quests)
* **Nhiệm vụ 1: "Khai hoang lập nghiệp"**:
  - Mục tiêu: Dùng cuốc xới tơi 4 ô đất luống và tưới nước cho đất.
  - Thưởng: 10 hạt giống rau thơm Đà Nẵng + 50 Tiền xu (Đồng).
* **Nhiệm vụ 2: "Tiếng gà ban mai"**:
  - Mục tiêu: Đi xuống chuồng góc Tây Nam, cho gà ăn thóc và nhặt 2 quả trứng gà đầu tiên.
  - Thưởng: 1 Bó rơm vàng + Mở khóa công thức ốp la trứng.
* **Nhiệm vụ 3: "Chuyến hàng chợ phiên"**:
  - Mục tiêu: Thu hoạch luống rau đầu tiên và giao cho Bác Ba trưởng thôn.
  - Thưởng: Nâng cấp bình tưới nước dung tích lớn hơn + Mở khóa khu vực đường làng mới.

---

## 6. Giao diện người dùng (Pixel Art UI / UX)

* **Thanh trạng thái thời gian trên cùng**:
  - Khung bo góc nền kem/kraft, viền nâu cổ điển, icon thời tiết động.
* **Thanh Hotbar nông cụ (Dưới cùng)**:
  - Các ô phím tắt 1 - 5 chọn nhanh Cuốc, Bình tưới, Hạt giống, Liềm, Thức ăn.
* **Bảng túi đồ (Inventory Modal - Phím I)**:
  - Lưới ô đồ hiển thị số lượng vật phẩm, nông sản, tiền tệ.
* **Hộp thoại hội thoại (Dialogue Box - Phím Space/E)**:
  - Khung thoại pixel art có chân dung NPC (Portrait), hiển thị từng chữ typewriter mượt mà.
* **Thông báo nổi (Toast Notification)**:
  - Hiển thị "+1 Trứng gà", "+1 Bắp ngô" với âm thanh vui tươi.

---

## 7. Lộ trình triển khai dự án (Implementation Roadmap)

### Giai đoạn 1: Khởi tạo Project Godot & Cấu trúc mã nguồn
- Thiết lập project Godot 4.7 (`project.godot`), cài đặt độ phân giải pixel-perfect, viewport scaling.
- Xây dựng hệ thống input: WASD, phím công cụ (1-5), tương tác (E / Space / Left Click).
- Tạo nhân vật người chơi với sprite nón lá + áo bà ba và script di chuyển CharacterBody2D.

### Giai đoạn 2: Dựng bản đồ "Little DaNang" bằng Sprite & TileMap
- Tạo các asset pixel art chuẩn mực cho:
  - Ngôi nhà mái ngói đỏ Việt Nam, giàn hoa leo, lu nước, giàn mướp/dây leo.
  - Khu chuồng trại gỗ, đống rơm, máng thức ăn.
  - Ô đất cày (tilled soil), đất khô, đất ướt, đất cỏ hoang.
  - Bụi tre, hàng chuối, dây phơi áo quần, cây xanh và đường đất.
- Áp dụng hệ thống Y-sort để nhân vật có thể đi trước/sau công trình và cây cối tự nhiên.
- Thiết lập Collision Polygon2D ngăn xuyên tường, xuyên rào.

### Giai đoạn 3: Hiện thực hóa cơ chế Nông trại & Động vật
- Hệ thống ô đất tương tác: Click hoặc phím hành động để cuốc đất, tưới nước, gieo hạt.
- Tạo các NPC động vật: Gà con, gà trống mào đỏ, vịt trắng, heo con đi lại ngẫu nhiên trong chuồng.
- Nhặt vật phẩm (trứng, nông sản) vào túi đồ.

### Giai đoạn 4: Hệ thống Thời gian Ngày/Đêm & UI Hoàn chỉnh
- Tạo HUD đồng hồ thời gian y hệt ảnh: `☀️ 11:40 - Thứ ba, 13/10 - Buổi trưa`.
- Tạo nhãn địa danh `🌴 Little DaNang` góc dưới bên phải.
- Hiệu ứng ánh sáng ngày/đêm chuyển màu mượt mà.
- Bảng túi đồ và thông báo nhặt đồ.

### Giai đoạn 5: NPC, Hội thoại & Nhiệm vụ
- Thêm NPC Bác Ba trưởng thôn đứng bên đường.
- Hệ thống hội thoại hiển thị tên, nội dung và giao 3 nhiệm vụ mẫu.
- Kiểm thử và đóng gói hoàn thiện.

---

## 8. Kế hoạch Bản cập nhật 1.4: Tùy biến Nông thôn & Trải nghiệm Âm vang

### 1. Tùy biến Personalization & Xây dựng (Customization & Building)
- **Tùy biến Trang phục (Cosmetics):**
  - Thay đổi trang phục nhân vật linh hoạt: Áo bà ba truyền thống (các gam màu đặc trưng: vàng mỡ gà, xanh lá sen, nâu đất), áo dài truyền thống du xuân, nón lá chóp nhọn, khăn rằn Nam Bộ quàng cổ.
- **Trang trí Nhà cửa & Nông trại (Furniture & Decorating):**
  - **Nội thất bên trong nhà ba gian:** Bộ bàn ghế cẩm thạch xưa, sập/phản gỗ lim, bàn thờ gia tiên trang nghiêm, tivi đen trắng cổ điển, quạt trần cánh đồng xưa.
  - **Ngoại thất khuôn viên:** Đặt thêm bù nhìn rơm xua đuổi chim ăn hạt, chậu cúc vàng rực rỡ đón Tết, hàng rào tre đan lát bao quanh bờ ao, giàn bầu/mướp trĩu quả ngay lối vào cổng ngõ.

### 2. Nâng cấp Kỹ thuật & Trải nghiệm (Godot Engine)
- **Hệ thống Lưu dữ liệu toàn diện (Save/Load System):**
  - Cơ chế tự động lưu game khi nhân vật lên giường đi ngủ (kết thúc một ngày làm việc nông trại).
  - Dữ liệu lưu trữ định dạng JSON/Resource bao gồm: trạng thái độ ẩm và sinh trưởng từng ô đất, thời gian trong game, toàn bộ vật phẩm trong túi đồ, trang phục đang mặc và vị trí của các NPC.
- **Thiết kế Âm thanh & Nhạc nền (Sound & Audio Design):**
  - **Ambient Sound (Âm thanh môi trường chân thực):**
    - Tiếng gà trống gáy vang ban mai đánh thức ngày mới.
    - Tiếng ve sầu râm ran trưa hè rực nắng.
    - Tiếng dế mèn, ếch nhái rên rỉ râm ran trong đêm thanh vắng.
    - Tiếng sóng biển vỗ rì rào dọc tuyến đường ven biển và đảo ngọc.
  - **BGM (Nhạc nền bản sắc):**
    - Nhạc Acoustic êm dịu kết hợp bộ nhạc cụ dân tộc truyền thống (Đàn bầu tha thiết, Sáo trúc véo von, Đàn tranh thánh thót).
    - Phối khí cùng phong cách điệu điệu hiện đại chillhop/lo-fi nhẹ nhàng, thư giãn cho người chơi khi làm nông.

