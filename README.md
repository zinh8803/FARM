# Game Nông Trại 2D Pixel Art Việt Nam

Dự án game mô phỏng nông trại và đời sống làng quê Việt Nam được xây dựng trên **Godot Engine 4.x**, lấy cảm hứng từ phong cách đồ họa Stardew Valley kết hợp nét văn hóa truyền thống nông thôn Việt Nam.

---

## 🌾 Điểm nổi bật & Tính năng đã hoàn thành

1. **Đồ họa Pixel Art thuần Việt (Tái hiện chính xác hình ảnh mẫu)**:
   - **Nhà cổ truyền thống**: Mái ngói đỏ rêu phong, hiên nhà lát gạch đỏ, giàn hoa giấy / hoa leo nở rộ, lu nước sành, chổi rơm quét sân, cột gỗ và cửa liếp gắn bùa đỏ.
   - **Khu chuồng trại chăn nuôi**: Chuồng gỗ mái tôn, đống rơm vàng truyền thống, máng ăn.
   - **Vật nuôi sống động**: Đàn gà trống mào đỏ, gà mái đẻ trứng, đàn vịt trắng, chú heo hồng ủn ỉn có AI di chuyển tự nhiên và biểu cảm trái tim ❤️ khi được chăm sóc.
   - **Khu vườn ruộng (4 hàng x 8 cột)**: Luống đất cày xới, đất hoang có cỏ sỏi, cây bắp ngô trĩu hạt.
   - **Hệ sinh thái cảnh quan**: Rặng tre xanh, cây chuối sai buồng & bắp chuối tím, dây phơi quần áo thôn quê, cây ăn quả và biển chỉ dẫn nông trại.

2. **Nhân vật & Cơ chế điều khiển**:
   - Nhân vật nông dân đội nón lá Việt Nam, mặc áo bà ba vàng, quần nâu.
   - Di chuyển 4 hướng mượt mà (WASD hoặc phím mũi tên).
   - Hệ thống nông cụ 5 món trên thanh Hotbar (1: Cuốc, 2: Bình tưới, 3: Hạt giống, 4: Liềm, 5: Rơm/Thức ăn).
   - Tương tác phím `E` hoặc `Space` (hoặc click chuột): Cuốc đất, tưới nước, gieo hạt, thu hoạch bắp, nhặt trứng gà và trò chuyện với NPC.

3. **Hệ thống NPC & Chuỗi 3 nhiệm vụ nhập môn**:
   - NPC **Bác Ba (Trưởng thôn)** đứng đón chào tại ngã rẽ lối vào làng.
   - Hộp thoại hội thoại hiển thị tên người nói và lời thoại hướng dẫn.
   - Nhiệm vụ 1: Dùng cuốc xới tơi 4 ô đất luống.
   - Nhiệm vụ 2: Chăm sóc đàn gà và nhặt 2 quả trứng gà tươi.
   - Nhiệm vụ 3: Thu hoạch 2 bắp ngô đầu mùa giao cho Bác Ba.

4. **Hệ thống Đa Bản Đồ & Chuyển Cảnh Mượt Mà (Multi-Map Portals)**:
   - **🌾 Nông Trại Little DaNang (Farm Map)**: Bản đồ chính gồm nhà ngói đỏ, chuồng trại gia súc, lưới 32 ô ruộng trồng trọt, và bãi đỗ xe đạp, xe máy.
   - **🏡 Nhà Ba Gian Cổ Truyền (House Interior)**: Đi đến cửa nhà và nhấn `[E] Vào nhà` -> Bước vào không gian nhà cổ ấm cúng với bàn thờ gia tiên, sập gụ, chiếu cói và bộ bàn trà ấm tích; nhấn `[E] Ra ngoài sân` để trở lại nông trại.
   - **🏮 Chợ Quê & Làng Dân Cư (Village Market)**: Đi theo con đường đất về phía Nam -> Đến cổng làng đá rêu phong, dãy đèn lồng Hội An, sạp hàng chợ quê và gặp **NPC Cô Út** để bán nông sản và mua thêm hạt giống.
   - **🎋 Rừng Trúc & Suối Nước (Bamboo Forest)**: Đi theo con đường đất về phía Bắc -> Khám phá rặng trúc xanh mát, suối nước trong lành với cầu gỗ và bia di tích cổ kính.
   - **🌉 Đại Lộ & Cầu Sông Hàn Đà Nẵng (Danang Highway)**: Đi theo con đường đất về phía Đông nông trại -> Mở ra đại lộ ven biển dài 1400px với 4 làn xe nhựa mịn màng, ngắm nhìn biển xanh, hàng dừa, quán cà phê sữa đá vỉa hè, và cầu Rồng / sông Hàn biểu tượng!
   - Camera2D tự động bám theo bước chân nhân vật mượt mà với hiệu ứng chuyển màn hình (Fade transition) êm dịu, bảo toàn 100% tài nguyên, thời gian và phương tiện khi chuyển cảnh.

5. **Phương tiện di chuyển (Xe Đạp & Xe Máy Super Cub)**:
   - **🚲 Xe đạp phượng hoàng**: Tốc độ 185 px/s, có giỏ mây, bấm chuông `[H]` kêu "Kính coong!".
   - **🏍️ Xe máy Super Cub 50**: Tốc độ 285 px/s, đèn pha sáng, yếm trắng cổ điển, bấm còi `[H]` kêu "Bíp bíp!", xả khói bô khi tăng tốc.
   - Đến gần xe bấm `[E]` để lên xe, bấm `[E]` lần nữa để xuống xe bất kỳ lúc nào.

6. **Hệ thống Ngắm Ruộng Chuẩn Xác (Precision Farming Targeting)**:
   - Khi đứng trước các ô đất, hệ thống tự động xác định chính xác ô ruộng theo hướng nhân vật nhìn (hoặc theo con trỏ chuột) và hiển thị khung ngắm viền vàng.
   - Không còn tình trạng đứng lệch mà thao tác nhầm vào ô đất sau lưng hoặc bên hông.

---

## 🎮 Hướng dẫn điều khiển

| Phím | Hành động |
|---|---|
| `W`, `A`, `S`, `D` hoặc Phím mũi tên | Di chuyển nhân vật / Lái xe |
| `1`, `2`, `3`, `4`, `5` | Chọn nhanh nông cụ (Cuốc, Bình tưới, Hạt giống, Liềm, Thức ăn) |
| `E` hoặc `Space` | Tương tác / Lên xe / Xuống xe / Nói chuyện NPC / Dùng công cụ |
| `Chuột trái` | Click trực tiếp vào ô đất cần cuốc, tưới, gieo hạt, thu hoạch |
| `H` hoặc `F` | Bấm còi xe máy ("Bíp bíp") / Bấm chuông xe đạp ("Kính coong") |

---

## 🚀 Cách chạy Game

1. **Cách 1 (Nhanh nhất)**:
   - Click đúp vào file `run_game.bat` trong thư mục dự án.
2. **Cách 2 (Mở bằng Godot Editor)**:
   - Khởi động Godot 4.x.
   - Bấm **Import** -> Chọn file `project.godot` trong thư mục `game_test_3d`.
   - Nhấn **F5** để khởi chạy game.
