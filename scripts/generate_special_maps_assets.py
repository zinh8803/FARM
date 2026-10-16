"""
Script vẽ texture chi tiết độ phân giải cao pixel-art cho 3 map:
1. casino_props.png (256x256):
   - Bàn Roulette tròn sang trọng có số và bánh xoay kim loại vàng
   - Bàn Blackjack / Bài tây hình móng ngựa xanh lá đậm có viền bọc da đệm
   - Bàn Poker nỉ nhung đỏ viền gỗ gụ, chip cược, bài tây xòe
   - Máy đánh bạc Slot Machine neon phát sáng 777
   - Bàn Bi-da nỉ xanh lá 6 lỗ bọc da, bóng bi-da & gậy cơ
   - Cột đèn chùm pha lê Casino vàng kim lấp lánh
   - Quầy Bar cocktail ly rượu cao cấp

2. school_props.png (256x256):
   - Bàn học sinh đôi bằng gỗ tự nhiên có ngăn kéo cặp sách
   - Ghế tựa học sinh
   - Bàn giáo viên gỗ sang trọng có chồng giáo án, cốc bút
   - Bảng đen phấn trắng có chữ viết tiếng Việt nắn nót & hình vẽ hoa điểm 10
   - Tủ sách thư viện / Tủ trưng bày cúp cờ thi đua
   - Trống trường học truyền thống bọc da sơn đỏ có giá đỡ gỗ
   - Bản đồ Việt Nam treo tường có quần đảo Hoàng Sa & Trường Sa
   - Cây bàng / Cây phượng vĩ trong chậu trường học

3. racecourse_props.png (256x256):
   - Khán đài khán giả có mái che vòm bạt trắng sang trọng & các hàng ghế ngồi xem đua
   - Cổng xuất phát & Đích đến (Starting Gate / Finish Banner) cờ ca-rô thể thao
   - Hàng rào gỗ trắng đường đua uốn lượn phong cách hoàng gia Anh
   - Tháp quan sát trọng tài và cúp vàng chiến thắng
   - Đài phun nước trung tâm bãi cỏ trường đua
   - Bảng điện tử LED tỉ lệ cược & số thứ tự ngựa đua
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_casino_props():
    W, H = 256, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Bàn Blackjack / Bài Tây hình bán nguyệt móng ngựa (80 x 54 at 0, 0)
    bx, by = 4, 4
    # Viền đệm bọc da màu nâu cánh gián
    draw.chord([bx, by, bx + 76, by + 50], 0, 180, fill=(70, 35, 18, 255), outline=(140, 85, 45, 255), width=2)
    # Mặt nỉ xanh ngọc emerald
    draw.chord([bx + 6, by + 4, bx + 70, by + 46], 0, 180, fill=(15, 95, 60, 255))
    # Đường viền cược màu vàng gold hình vòng cung
    draw.arc([bx + 14, by + 12, bx + 62, by + 42], 0, 180, fill=(235, 195, 75, 255), width=1)
    # Vị trí các tụ đặt cược (5 ô tròn vàng)
    for px, py in [(bx + 16, by + 32), (bx + 26, by + 38), (bx + 38, by + 40), (bx + 50, by + 38), (bx + 60, by + 32)]:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(240, 210, 80, 255), outline=(160, 120, 30, 255))
    # Các quân bài tây xòe trước mặt dealer
    draw.rectangle([bx + 34, by + 18, bx + 42, by + 28], fill=(250, 250, 250, 255), outline=(180, 20, 20, 255))
    draw.rectangle([bx + 37, by + 18, bx + 45, by + 28], fill=(250, 250, 250, 255), outline=(20, 20, 20, 255))

    # 2. Bàn Poker nỉ nhung đỏ viền gỗ oval (88 x 54 at 86, 0)
    px, py = 88, 4
    # Viền gỗ gụ cao cấp
    draw.ellipse([px, py, px + 84, py + 48], fill=(55, 25, 15, 255), outline=(120, 65, 30, 255), width=3)
    # Mặt nỉ đỏ ruby
    draw.ellipse([px + 8, py + 6, px + 76, py + 42], fill=(145, 20, 35, 255))
    draw.ellipse([px + 14, py + 10, px + 70, py + 38], outline=(225, 185, 70, 255), width=1)
    # Cọc chip poker (xanh, đỏ, đen, vàng) ở giữa bàn
    draw.ellipse([px + 36, py + 20, px + 42, py + 24], fill=(40, 100, 210, 255))
    draw.ellipse([px + 44, py + 22, px + 50, py + 26], fill=(220, 40, 40, 255))
    draw.ellipse([px + 40, py + 24, px + 46, py + 28], fill=(240, 200, 50, 255))

    # 3. Bàn Bi-da chuyên nghiệp nỉ xanh lá 6 lỗ có bi & cơ (80 x 48 at 176, 0)
    lx, ly = 176, 6
    # Thành bàn gỗ bóng
    draw.rectangle([lx, ly, lx + 76, ly + 44], fill=(60, 32, 16, 255), outline=(110, 65, 30, 255), width=2)
    # Mặt nỉ xanh chuẩn thi đấu
    draw.rectangle([lx + 6, ly + 6, lx + 70, ly + 38], fill=(20, 110, 75, 255))
    # 6 lỗ góc và giữa màu đen
    for hx, hy in [(lx+6, ly+6), (lx+38, ly+6), (lx+70, ly+6), (lx+6, ly+38), (lx+38, ly+38), (lx+70, ly+38)]:
        draw.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(15, 15, 20, 255))
    # Bi cái trắng và tam giác bi màu
    draw.ellipse([lx + 20, ly + 20, lx + 24, ly + 24], fill=(255, 255, 255, 255))
    draw.ellipse([lx + 52, ly + 18, lx + 56, ly + 22], fill=(220, 40, 40, 255))
    draw.ellipse([lx + 56, ly + 16, lx + 60, ly + 20], fill=(240, 210, 40, 255))
    draw.ellipse([lx + 56, ly + 22, lx + 60, ly + 26], fill=(30, 70, 180, 255))
    # Gậy cơ bi-da đặt cạnh bàn
    draw.line([lx + 10, ly + 41, lx + 66, ly + 41], fill=(215, 175, 110, 255), width=2)

    # 4. Máy Đánh Bạc Neon Hoàng Gia 777 (Slot Machine - 40 x 64 at 0, 60)
    sx, sy = 6, 60
    # Thùng máy sơn mài tím đen viền LED vàng
    draw.rectangle([sx, sy + 4, sx + 34, sy + 60], fill=(35, 15, 45, 255), outline=(255, 215, 60, 255), width=2)
    # Bảng biển hiệu 777 JACKPOT phát sáng rực rỡ
    draw.rectangle([sx + 3, sy + 6, sx + 31, sy + 18], fill=(200, 20, 50, 255))
    draw.text((sx + 5, sy + 7), "7 7 7", fill=(255, 245, 120, 255))
    # Màn hình 3 cuộn quay Slot
    draw.rectangle([sx + 4, sy + 22, sx + 30, sy + 40], fill=(240, 245, 250, 255), outline=(40, 20, 60, 255))
    draw.line([sx + 13, sy + 22, sx + 13, sy + 40], fill=(160, 170, 185, 255), width=1)
    draw.line([sx + 21, sy + 22, sx + 21, sy + 40], fill=(160, 170, 185, 255), width=1)
    # Biểu tượng chuông, quả đào, số 7 trên cuộn
    draw.ellipse([sx + 6, sy + 28, sx + 11, sy + 34], fill=(220, 30, 30, 255))
    draw.ellipse([sx + 14, sy + 27, sx + 19, sy + 33], fill=(245, 190, 40, 255))
    draw.ellipse([sx + 23, sy + 28, sx + 28, sy + 34], fill=(50, 180, 70, 255))
    # Cần gạt bên hông máy (Pull Lever)
    draw.line([sx + 34, sy + 36, sx + 38, sy + 26], fill=(190, 195, 200, 255), width=2)
    draw.ellipse([sx + 36, sy + 22, sx + 41, sy + 27], fill=(230, 30, 40, 255))
    # Khay hứng xu bên dưới
    draw.rectangle([sx + 6, sy + 48, sx + 28, sy + 56], fill=(70, 75, 85, 255), outline=(220, 200, 80, 255))

    # 5. Đèn chùm pha lê Casino lung linh (Crystal Chandelier - 44 x 44 at 52, 60)
    dx, dy = 52, 60
    # Dây xích treo mạ vàng
    draw.line([dx + 22, dy + 2, dx + 22, dy + 12], fill=(220, 180, 60, 255), width=2)
    # Tầng pha lê 1 (lớn)
    draw.ellipse([dx + 6, dy + 12, dx + 38, dy + 24], fill=(255, 230, 140, 255), outline=(220, 180, 50, 255))
    # Tầng pha lê 2 (nhỏ)
    draw.ellipse([dx + 12, dy + 22, dx + 32, dy + 32], fill=(255, 240, 170, 255), outline=(230, 195, 60, 255))
    # Giọt pha lê rủ giọt nước
    for gx in [dx + 10, dx + 16, dx + 22, dx + 28, dx + 34]:
        draw.line([gx, dy + 24, gx, dy + 36], fill=(255, 250, 210, 230), width=1)
        draw.point((gx, dy + 37), fill=(255, 255, 255, 255))

    # 6. Quầy Bar Cocktail & Tủ Rượu Vang Đèn LED (96 x 60 at 104, 60)
    rx, ry = 104, 60
    # Tủ kính trưng bày rượu tầng trên
    draw.rectangle([rx + 4, ry + 2, rx + 92, ry + 32], fill=(25, 20, 30, 255), outline=(180, 140, 60, 255), width=2)
    # Các chai rượu vang và sâm banh cao cấp
    for col, c_fill in enumerate([(190, 40, 40), (40, 160, 70), (220, 180, 50), (60, 100, 200), (210, 150, 40)]):
        ix = rx + 12 + col * 15
        draw.rectangle([ix, ry + 12, ix + 8, ry + 28], fill=c_fill)
        draw.rectangle([ix + 2, ry + 6, ix + 6, ry + 12], fill=(200, 200, 210, 255))
    # Mặt quầy bar đá cẩm thạch đen tia vàng
    draw.rectangle([rx, ry + 32, rx + 96, ry + 56], fill=(35, 35, 40, 255), outline=(230, 190, 70, 255), width=2)
    # Ghế xoay quầy bar chân kim loại
    for st_x in [rx + 16, rx + 48, rx + 80]:
        draw.ellipse([st_x - 6, ry + 44, st_x + 6, ry + 52], fill=(160, 30, 40, 255), outline=(240, 200, 70, 255))
        draw.line([st_x, ry + 52, st_x, ry + 59], fill=(180, 185, 195, 255), width=2)

    # 7. Vòng quay Roulette Hoàng Gia (Roulette Wheel - 48 x 48 at 204, 60)
    wx, wy = 204, 60
    draw.ellipse([wx, wy, wx + 46, wy + 46], fill=(65, 30, 15, 255), outline=(225, 185, 60, 255), width=2)
    draw.ellipse([wx + 5, wy + 5, wx + 41, wy + 41], fill=(20, 60, 35, 255))
    # Vành số đen đỏ xen kẽ
    draw.ellipse([wx + 9, wy + 9, wx + 37, wy + 37], outline=(200, 30, 30, 255), width=3)
    # Trục quay kim loại vàng ở tâm
    draw.ellipse([wx + 19, wy + 19, wx + 27, wy + 27], fill=(255, 220, 60, 255), outline=(150, 110, 20, 255))
    draw.line([wx + 15, wy + 23, wx + 31, wy + 23], fill=(255, 250, 160, 255), width=1)
    draw.line([wx + 23, wy + 15, wx + 23, wy + 31], fill=(255, 250, 160, 255), width=1)

    img.save(os.path.join(ASSETS_DIR, "casino_props.png"))
    print("[OK] Created casino_props.png")

def generate_school_props():
    W, H = 256, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Bàn học sinh đôi gỗ tự nhiên (48 x 36 at 0, 0)
    bx, by = 4, 4
    # Mặt bàn gỗ sáng màu
    draw.rectangle([bx, by + 4, bx + 44, by + 22], fill=(215, 165, 105, 255), outline=(145, 95, 45, 255), width=2)
    # Sách vở, hộp bút trên mặt bàn
    draw.rectangle([bx + 6, by + 7, bx + 16, by + 16], fill=(245, 245, 250, 255), outline=(40, 120, 200, 255))
    draw.rectangle([bx + 26, by + 8, bx + 36, by + 17], fill=(245, 245, 250, 255), outline=(210, 40, 40, 255))
    draw.line([bx + 18, by + 10, bx + 22, by + 15], fill=(240, 190, 40, 255), width=2) # bút chì
    # Hộc bàn & chân sắt sơn tĩnh điện
    draw.rectangle([bx + 2, by + 22, bx + 42, by + 28], fill=(160, 115, 65, 255))
    draw.line([bx + 5, by + 28, bx + 5, by + 34], fill=(60, 65, 75, 255), width=2)
    draw.line([bx + 39, by + 28, bx + 39, by + 34], fill=(60, 65, 75, 255), width=2)

    # 2. Ghế học sinh gỗ tựa lưng (22 x 26 at 54, 4)
    gx, gy = 56, 6
    draw.rectangle([gx + 2, gy + 2, gx + 18, gy + 8], fill=(195, 140, 85, 255), outline=(130, 80, 35, 255))
    draw.rectangle([gx + 2, gy + 12, gx + 18, gy + 18], fill=(215, 160, 100, 255))
    draw.line([gx + 4, gy + 8, gx + 4, gy + 24], fill=(60, 65, 75, 255), width=2)
    draw.line([gx + 16, gy + 8, gx + 16, gy + 24], fill=(60, 65, 75, 255), width=2)

    # 3. Bàn Giáo Viên bục giảng (64 x 42 at 84, 0)
    tx, ty = 86, 2
    draw.rectangle([tx, ty + 4, tx + 60, ty + 28], fill=(175, 110, 55, 255), outline=(110, 60, 25, 255), width=2)
    # Khăn trải bàn kẻ ô ren đỏ
    draw.rectangle([tx + 18, ty + 6, tx + 42, ty + 24], fill=(220, 65, 65, 255), outline=(255, 255, 255, 255))
    # Cốc cắm bút & chồng bài kiểm tra điểm 10 đỏ
    draw.rectangle([tx + 8, ty + 8, tx + 16, ty + 18], fill=(250, 250, 250, 255), outline=(210, 40, 40, 255))
    draw.point((tx + 12, ty + 12), fill=(210, 40, 40, 255)) # điểm 10
    draw.rectangle([tx + 46, ty + 9, tx + 53, ty + 19], fill=(60, 140, 210, 255))

    # 4. Trống Trường Học Truyền Thống sơn đỏ giá gỗ (44 x 50 at 154, 0)
    kx, ky = 156, 2
    # Thùng trống gỗ cong bọc da, sơn đỏ tươi
    draw.ellipse([kx + 4, ky + 10, kx + 36, ky + 34], fill=(195, 30, 30, 255), outline=(120, 15, 15, 255), width=2)
    # Mặt trống da trâu có đinh tán đồng
    draw.ellipse([kx + 6, ky + 8, kx + 34, ky + 20], fill=(225, 205, 150, 255), outline=(150, 120, 60, 255), width=2)
    # Hàng đinh tán vàng quanh tang trống
    for dx in range(kx + 8, kx + 33, 4):
        draw.point((dx, ky + 21), fill=(245, 210, 60, 255))
    # Giá đỡ gỗ chữ X màu cánh gián
    draw.line([kx + 6, ky + 26, kx + 14, ky + 46], fill=(120, 70, 35, 255), width=3)
    draw.line([kx + 34, ky + 26, kx + 26, ky + 46], fill=(120, 70, 35, 255), width=3)
    draw.line([kx + 10, ky + 44, kx + 30, ky + 44], fill=(140, 85, 45, 255), width=2)
    # Dùi trống gỗ
    draw.line([kx + 32, ky + 14, kx + 40, ky + 6], fill=(220, 180, 100, 255), width=2)

    # 5. Bản Đồ Việt Nam Treo Tường (Có Hoàng Sa - Trường Sa) (40 x 56 at 206, 0)
    vx, vy = 208, 0
    draw.rectangle([vx, vy + 2, vx + 38, vy + 52], fill=(235, 245, 255, 255), outline=(120, 80, 40, 255), width=2)
    # Nẹp gỗ treo bản đồ trên dưới
    draw.line([vx - 2, vy + 2, vx + 40, vy + 2], fill=(140, 85, 45, 255), width=3)
    draw.line([vx - 2, vy + 52, vx + 40, vy + 52], fill=(140, 85, 45, 255), width=3)
    # Dải đất hình chữ S màu xanh lá
    s_pts = [(vx+18, vy+8), (vx+24, vy+12), (vx+16, vy+18), (vx+20, vy+24), (vx+22, vy+32), (vx+18, vy+40), (vx+12, vy+44), (vx+15, vy+46)]
    for pt in s_pts:
        draw.ellipse([pt[0]-2, pt[1]-2, pt[0]+2, pt[1]+2], fill=(60, 160, 75, 255))
    # Quần đảo Hoàng Sa & Trường Sa màu vàng cam nổi bật
    draw.point((vx + 30, vy + 26), fill=(240, 120, 20, 255)) # Hoàng Sa
    draw.point((vx + 31, vy + 27), fill=(240, 120, 20, 255))
    draw.point((vx + 32, vy + 38), fill=(240, 120, 20, 255)) # Trường Sa
    draw.point((vx + 33, vy + 39), fill=(240, 120, 20, 255))
    draw.text((vx + 4, vy + 4), "VN", fill=(210, 30, 30, 255))

    # 6. Tủ Sách Thư Viện Lớp Học / Tủ Kính Danh Dự (64 x 68 at 0, 56)
    cx, cy = 4, 58
    draw.rectangle([cx, cy, cx + 60, cy + 64], fill=(140, 85, 45, 255), outline=(80, 45, 20, 255), width=2)
    # 3 ngăn kệ sách đầy ắp sách vở nhiều màu
    for row in range(3):
        ry = cy + 6 + row * 18
        draw.line([cx + 4, ry + 16, cx + 56, ry + 16], fill=(185, 125, 75, 255), width=2)
        for b_col, b_color in enumerate([(220, 50, 50), (45, 130, 220), (50, 180, 90), (240, 190, 40), (160, 60, 200), (230, 120, 40)]):
            bx_book = cx + 8 + b_col * 7
            draw.rectangle([bx_book, ry + 2, bx_book + 5, ry + 16], fill=b_color)
    # Cúp vàng danh dự trên nóc tủ
    draw.polygon([(cx + 26, cy - 2), (cx + 34, cy - 2), (cx + 32, cy + 4), (cx + 28, cy + 4)], fill=(255, 215, 50, 255))

    # 7. Cây Bàng / Cây Phượng Vĩ Sân Trường trong chậu xi măng (44 x 64 at 72, 56)
    px, py = 76, 56
    # Chậu xi măng bát giác
    draw.polygon([(px + 6, py + 48), (px + 34, py + 48), (px + 30, py + 62), (px + 10, py + 62)], fill=(160, 165, 175, 255), outline=(110, 115, 125, 255))
    # Thân cây gỗ nâu sần sùi
    draw.line([px + 20, py + 24, px + 20, py + 48], fill=(105, 65, 35, 255), width=4)
    # Tán lá bàng xanh mát có điểm xuyết hoa phượng vĩ đỏ thắm
    draw.ellipse([px + 2, py + 4, px + 38, py + 32], fill=(45, 140, 60, 255))
    draw.ellipse([px + 6, py + 6, px + 34, py + 26], fill=(70, 175, 80, 255))
    # Hoa phượng đỏ
    for fx, fy in [(px + 10, py + 12), (px + 22, py + 8), (px + 28, py + 18), (px + 16, py + 22)]:
        draw.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=(235, 45, 35, 255))

    # 8. Cột Cờ Tổ Quốc Sân Trường (Cờ đỏ sao vàng) (36 x 72 at 128, 56)
    fx, fy = 132, 54
    # Bệ cờ tam cấp đá hoa cương
    draw.rectangle([fx + 4, fy + 58, fx + 28, fy + 68], fill=(185, 55, 45, 255), outline=(130, 30, 25, 255))
    draw.rectangle([fx + 8, fy + 52, fx + 24, fy + 58], fill=(210, 75, 65, 255))
    # Cột cờ inox trắng sáng vút cao
    draw.line([fx + 16, fy + 4, fx + 16, fy + 52], fill=(235, 240, 245, 255), width=2)
    draw.ellipse([fx + 14, fy + 2, fx + 18, fy + 6], fill=(255, 220, 60, 255)) # quả cầu vàng đỉnh cột
    # Lá cờ đỏ sao vàng tung bay trong gió biển
    draw.polygon([(fx + 16, fy + 8), (fx + 36, fy + 12), (fx + 34, fy + 24), (fx + 16, fy + 22)], fill=(225, 30, 35, 255))
    draw.point((fx + 24, fy + 16), fill=(255, 235, 60, 255)) # sao vàng

    img.save(os.path.join(ASSETS_DIR, "school_props.png"))
    print("[OK] Created school_props.png")

def generate_racecourse_props():
    W, H = 256, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Khán đài danh dự mái vòm bạt trắng (Grandstand Canopy - 96 x 60 at 0, 0)
    gx, gy = 4, 4
    # Mái bạt vòm cong trắng ngà sọc đỏ thể thao
    draw.chord([gx, gy, gx + 92, gy + 32], 180, 360, fill=(245, 245, 250, 255), outline=(210, 45, 45, 255), width=2)
    # Các dải sọc đỏ lễ hội
    for sx in [gx + 18, gx + 36, gx + 54, gx + 72]:
        draw.line([sx, gy + 14, sx, gy + 26], fill=(220, 40, 40, 255), width=3)
    # Cột thép nâng đỡ
    draw.line([gx + 6, gy + 26, gx + 6, gy + 54], fill=(160, 170, 185, 255), width=3)
    draw.line([gx + 86, gy + 26, gx + 86, gy + 54], fill=(160, 170, 185, 255), width=3)
    # Các hàng ghế khán giả bậc thang rực rỡ
    draw.rectangle([gx + 12, gy + 30, gx + 80, gy + 38], fill=(60, 120, 220, 255)) # hàng 1 xanh dương
    draw.rectangle([gx + 10, gy + 40, gx + 82, gy + 48], fill=(225, 60, 60, 255)) # hàng 2 đỏ
    draw.rectangle([gx + 8, gy + 50, gx + 84, gy + 56], fill=(245, 195, 45, 255)) # hàng 3 vàng

    # 2. Cổng vòm Đích Đến / FINISH LINE Cờ Ca-rô (80 x 60 at 104, 0)
    fx, fy = 106, 4
    # 2 cột thép bên đường đua
    draw.rectangle([fx + 4, fy + 16, fx + 10, fy + 56], fill=(210, 215, 225, 255), outline=(60, 70, 85, 255))
    draw.rectangle([fx + 66, fy + 16, fx + 72, fy + 56], fill=(210, 215, 225, 255), outline=(60, 70, 85, 255))
    # Băng rôn FINISH cờ ca-rô đen trắng
    draw.rectangle([fx + 2, fy + 4, fx + 74, fy + 18], fill=(20, 25, 35, 255))
    for cx in range(fx + 4, fx + 72, 8):
        draw.rectangle([cx, fy + 6, cx + 4, fy + 10], fill=(255, 255, 255, 255))
        draw.rectangle([cx + 4, fy + 10, cx + 8, fy + 14], fill=(255, 255, 255, 255))
    draw.text((fx + 18, fy + 5), "FINISH", fill=(255, 220, 40, 255))

    # 3. Hàng rào gỗ trắng hoàng gia uốn lượn (White Racecourse Rail - 64 x 32 at 188, 0)
    rx, ry = 188, 12
    # 4 cột gỗ trắng đỉnh tròn
    for px in [rx + 4, rx + 22, rx + 40, rx + 58]:
        draw.rectangle([px, ry + 2, px + 4, ry + 26], fill=(245, 250, 255, 255), outline=(180, 190, 205, 255))
        draw.ellipse([px - 1, ry - 1, px + 5, ry + 5], fill=(255, 255, 255, 255))
    # 2 thanh giằng ngang bóng loáng
    draw.line([rx, ry + 6, rx + 62, ry + 6], fill=(255, 255, 255, 255), width=2)
    draw.line([rx, ry + 16, rx + 62, ry + 16], fill=(255, 255, 255, 255), width=2)

    # 4. Đài Phun Nước Trung Tâm Trường Đua (Fountain - 64 x 50 at 0, 68)
    wx, wy = 4, 70
    # Bể chứa nước tròn ốp đá xanh ngọc
    draw.ellipse([wx + 2, wy + 16, wx + 62, wy + 46], fill=(30, 130, 180, 255), outline=(185, 215, 235, 255), width=3)
    draw.ellipse([wx + 8, wy + 20, wx + 56, wy + 42], fill=(60, 175, 225, 255))
    # Trụ phun nước trung tâm & vòi bắn nước tỏa 4 hướng
    draw.ellipse([wx + 24, wy + 10, wx + 40, wy + 24], fill=(210, 225, 240, 255), outline=(130, 160, 190, 255))
    draw.line([wx + 32, wy + 2, wx + 32, wy + 16], fill=(255, 255, 255, 255), width=2)
    # Tia nước xòe cầu vồng
    draw.arc([wx + 18, wy + 2, wx + 46, wy + 26], 180, 360, fill=(230, 245, 255, 255), width=2)

    # 5. Bảng Điện Tử Tỉ Lệ Cược LED (Odds LED Board - 72 x 50 at 72, 68)
    ox, oy = 74, 70
    draw.rectangle([ox, oy, ox + 68, oy + 44], fill=(15, 18, 25, 255), outline=(230, 190, 50, 255), width=2)
    draw.text((ox + 6, oy + 4), "BẢNG CƯỢC ĐUA", fill=(255, 220, 60, 255))
    # 4 dòng ngựa đua với màu áo tương ứng
    horses_info = [("1 Sấm", (240, 60, 60), "1:2.5"), ("2 Gió", (60, 140, 240), "1:3.0"), ("3 Mây", (250, 210, 40), "1:4.2"), ("4 Lửa", (240, 120, 40), "1:5.0")]
    for idx, (hname, hcol, hodds) in enumerate(horses_info):
        ly_row = oy + 14 + idx * 7
        draw.rectangle([ox + 4, ly_row, ox + 8, ly_row + 4], fill=hcol)
        draw.text((ox + 12, ly_row - 2), hname, fill=(225, 230, 240, 255))
        draw.text((ox + 46, ly_row - 2), hodds, fill=(80, 240, 120, 255))

    # 6. Cúp Vàng Vô Địch Trường Đua (Champion Trophy - 36 x 48 at 150, 70)
    tx, ty = 152, 70
    # Bệ gỗ chạm khắc
    draw.rectangle([tx + 6, ty + 36, tx + 26, ty + 46], fill=(70, 35, 15, 255), outline=(180, 120, 50, 255))
    # Chân cúp vàng
    draw.polygon([(tx + 11, ty + 36), (tx + 21, ty + 36), (tx + 18, ty + 26), (tx + 14, ty + 26)], fill=(240, 190, 40, 255))
    # Thân cúp hình búp sen nở & quai cầm 2 bên
    draw.ellipse([tx + 8, ty + 8, tx + 24, ty + 26], fill=(255, 220, 60, 255), outline=(200, 150, 20, 255))
    draw.arc([tx + 2, ty + 10, tx + 14, ty + 22], 90, 270, fill=(245, 195, 45, 255), width=2)
    draw.arc([tx + 18, ty + 10, tx + 30, ty + 22], 270, 90, fill=(245, 195, 45, 255), width=2)

    img.save(os.path.join(ASSETS_DIR, "racecourse_props.png"))
    print("[OK] Created racecourse_props.png")

if __name__ == "__main__":
    generate_casino_props()
    generate_school_props()
    generate_racecourse_props()
