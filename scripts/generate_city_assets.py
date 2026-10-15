"""
Script tạo toàn bộ sprite đồ họa kiến trúc thành phố hiện đại:
1. city_buildings.png: Tòa nhà chọc trời Sky Tower, Ngân hàng trung tâm, Cửa hàng tiện lợi 24/7, Biệt thự thông minh.
2. city_props.png: Đèn đường LED, cây cảnh đô thị, trạm ATM, xe thể thao, biển hiệu LED.
3. city_interiors.png: Nội thất ngân hàng, siêu thị mini, sảnh chọc trời, biệt thự cao cấp.
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_city_buildings():
    W, H = 512, 512
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # -------------------------------------------------------------
    # 1. TOÀ NHÀ CHỌC TRỜI - SKY TOWER (160 x 220 at 0, 0)
    # -------------------------------------------------------------
    bx, by = 0, 0
    # Spire / Antena trên đỉnh
    draw.line([bx + 80, by + 4, bx + 80, by + 28], fill=(210, 225, 240, 255), width=2)
    draw.ellipse([bx + 78, by + 2, bx + 82, by + 6], fill=(255, 60, 60, 255)) # Đèn tín hiệu hàng không
    # Tháp chóp (Stepped crown)
    draw.polygon([(bx + 62, by + 38), (bx + 98, by + 38), (bx + 86, by + 24), (bx + 74, by + 24)], fill=(80, 115, 150, 255))
    draw.polygon([(bx + 50, by + 55), (bx + 110, by + 55), (bx + 98, by + 38), (bx + 62, by + 38)], fill=(95, 135, 175, 255))
    
    # Khung thân toà nhà (Glass curtain wall)
    draw.rectangle([bx + 20, by + 55, bx + 140, by + 218], fill=(35, 55, 80, 255), outline=(70, 105, 140, 255), width=2)
    # Các dải kính phản chiếu & tầng lầu
    for row in range(9):
        ry = by + 60 + row * 15
        draw.rectangle([bx + 26, ry, bx + 134, ry + 10], fill=(70, 120, 175, 255))
        # Cửa kính văn phòng phát sáng
        for col in range(6):
            cx = bx + 30 + col * 17
            color_win = (195, 235, 255, 255) if (row + col) % 3 != 0 else (255, 245, 180, 230)
            draw.rectangle([cx, ry + 2, cx + 13, ry + 8], fill=color_win)
    
    # Trục trang trí kim loại thẳng đứng (Vertical Mullions)
    for col in range(7):
        cx = bx + 26 + col * 18
        draw.line([cx, by + 55, cx, by + 195], fill=(130, 165, 200, 255), width=1)
        
    # Tầng trệt & Sảnh đón (Grand Lobby)
    draw.rectangle([bx + 14, by + 195, bx + 146, by + 218], fill=(45, 65, 90, 255), outline=(160, 190, 220, 255), width=2)
    # Biển tên SKY TOWER phát sáng vàng kim
    draw.rectangle([bx + 35, by + 190, bx + 125, by + 198], fill=(20, 30, 45, 255))
    draw.text((bx + 40, by + 189), "SKY TOWER", fill=(255, 215, 80, 255))
    # Cửa kính xoay / Cửa tự động
    draw.rectangle([bx + 62, by + 200, bx + 98, by + 218], fill=(140, 210, 245, 220), outline=(220, 235, 250, 255))
    draw.line([bx + 80, by + 200, bx + 80, by + 218], fill=(60, 90, 120, 255), width=1)

    # -------------------------------------------------------------
    # 2. NGÂN HÀNG TRUNG TÂM - CENTRAL BANK (140 x 140 at 165, 0)
    # -------------------------------------------------------------
    bx, by = 165, 20
    # Mái vòm / Tam giác cổ điển kết hợp kính hiện đại (Pediment)
    draw.polygon([(bx + 8, by + 28), (bx + 132, by + 28), (bx + 70, by + 6)], fill=(225, 230, 235, 255), outline=(150, 165, 180, 255), width=2)
    # Chữ NGÂN HÀNG / BANK
    draw.rectangle([bx + 30, by + 18, bx + 110, by + 26], fill=(25, 75, 45, 255))
    draw.text((bx + 36, by + 16), "VIETCOMBANK", fill=(255, 225, 90, 255))
    
    # Thân ngân hàng đá hoa cương trắng xám
    draw.rectangle([bx + 12, by + 28, bx + 128, by + 128], fill=(235, 240, 245, 255), outline=(160, 175, 190, 255), width=2)
    # 4 Cột đá trụ vuông hiện đại
    for i in range(4):
        col_x = bx + 22 + i * 28
        draw.rectangle([col_x, by + 30, col_x + 16, by + 128], fill=(210, 220, 230, 255), outline=(170, 185, 200, 255), width=1)
        # Khắc rãnh cột
        draw.line([col_x + 8, by + 32, col_x + 8, by + 126], fill=(185, 200, 215, 255), width=1)
        
    # Kính xanh ngân hàng ở giữa các cột
    draw.rectangle([bx + 42, by + 40, bx + 98, by + 80], fill=(40, 120, 165, 255), outline=(100, 170, 210, 255))
    # Cửa kính lớn ra vào
    draw.rectangle([bx + 52, by + 90, bx + 88, by + 128], fill=(120, 195, 235, 230), outline=(50, 90, 130, 255), width=2)
    draw.line([bx + 70, by + 90, bx + 70, by + 128], fill=(40, 70, 100, 255), width=2)
    # Cây ATM gắn liền mặt tiền
    draw.rectangle([bx + 104, by + 95, bx + 122, by + 124], fill=(20, 80, 50, 255), outline=(255, 215, 80, 255))
    draw.rectangle([bx + 107, by + 98, bx + 119, by + 108], fill=(120, 235, 180, 255)) # màn hình ATM
    draw.text((bx + 106, by + 110), "ATM", fill=(255, 255, 255, 255))

    # -------------------------------------------------------------
    # 3. CỬA HÀNG TIỆN LỢI 24/7 - SUPER MART (130 x 120 at 310, 20)
    # -------------------------------------------------------------
    bx, by = 310, 20
    # Khối nhà chính
    draw.rectangle([bx + 8, by + 16, bx + 122, by + 116], fill=(245, 245, 248, 255), outline=(190, 195, 200, 255), width=2)
    # Biển hiệu Neon đỏ - xanh - trắng đặc trưng cửa hàng tiện lợi
    draw.rectangle([bx + 6, by + 10, bx + 124, by + 34], fill=(225, 45, 45, 255), outline=(180, 20, 20, 255))
    draw.rectangle([bx + 8, by + 26, bx + 122, by + 32], fill=(245, 140, 30, 255))
    draw.text((bx + 24, by + 13), "24/7 WINMART", fill=(255, 255, 255, 255))
    
    # Cửa kính lớn nhìn thấy đồ bên trong
    draw.rectangle([bx + 14, by + 42, bx + 58, by + 98], fill=(140, 215, 245, 200), outline=(90, 145, 185, 255))
    # Giá hàng bên trong qua kính
    draw.line([bx + 18, by + 60, bx + 54, by + 60], fill=(240, 100, 80, 255), width=3)
    draw.line([bx + 18, by + 75, bx + 54, by + 75], fill=(80, 180, 120, 255), width=3)
    draw.line([bx + 18, by + 90, bx + 54, by + 90], fill=(240, 200, 60, 255), width=3)
    
    # Cửa trượt tự động kính (Automatic Sliding Doors)
    draw.rectangle([bx + 68, by + 45, bx + 112, by + 116], fill=(160, 225, 255, 220), outline=(60, 100, 140, 255), width=2)
    draw.line([bx + 90, by + 45, bx + 90, by + 116], fill=(45, 80, 115, 255), width=2)
    # Tay nắm cửa xanh
    draw.rectangle([bx + 86, by + 78, bx + 88, by + 92], fill=(220, 40, 40, 255))
    draw.rectangle([bx + 92, by + 78, bx + 94, by + 92], fill=(220, 40, 40, 255))

    # -------------------------------------------------------------
    # 4. BIỆT THỰ THÔNG MINH HIỆN ĐẠI - SMART VILLA (160 x 140 at 0, 230)
    # -------------------------------------------------------------
    bx, by = 0, 230
    # Tấm pin năng lượng mặt trời trên mái (Solar Panels)
    for p in range(4):
        px = bx + 36 + p * 18
        draw.polygon([(px, by + 14), (px + 14, by + 14), (px + 18, by + 26), (px + 4, by + 26)], fill=(25, 50, 95, 255), outline=(130, 170, 210, 255))
    
    # Khối tầng 2 vươn ra (Cantilevered 2nd Floor)
    draw.rectangle([bx + 20, by + 26, bx + 140, by + 80], fill=(245, 245, 245, 255), outline=(180, 185, 190, 255), width=2)
    # Mảng ốp gỗ Conwood sang trọng (Wood slat panel)
    for s in range(7):
        sy = by + 30 + s * 7
        draw.line([bx + 24, sy, bx + 64, sy], fill=(165, 105, 55, 255), width=3)
    # Cửa kính ban công lớn tầng 2
    draw.rectangle([bx + 74, by + 32, bx + 132, by + 74], fill=(70, 135, 185, 230), outline=(40, 80, 120, 255))
    # Lan can kính ban công (Glass railing)
    draw.rectangle([bx + 70, by + 64, bx + 136, by + 80], fill=(175, 220, 245, 160), outline=(210, 235, 250, 255))
    
    # Tầng trệt (Ground Floor)
    draw.rectangle([bx + 30, by + 80, bx + 145, by + 135], fill=(55, 60, 68, 255), outline=(35, 40, 46, 255), width=2)
    # Cửa chính gỗ nguyên khối thông minh (Smart Door with keyless lock)
    draw.rectangle([bx + 40, by + 88, bx + 68, by + 135], fill=(140, 80, 35, 255), outline=(90, 50, 20, 255), width=2)
    draw.rectangle([bx + 62, by + 110, bx + 65, by + 116], fill=(255, 215, 60, 255)) # Khóa vân tay phát sáng
    # Cửa sổ kính phòng khách tầng trệt
    draw.rectangle([bx + 78, by + 90, bx + 138, by + 130], fill=(110, 185, 230, 230), outline=(190, 220, 245, 255))
    # Cây cảnh ban công / trước nhà
    draw.ellipse([bx + 16, by + 110, bx + 28, by + 130], fill=(60, 150, 75, 255))

    img.save(os.path.join(ASSETS_DIR, "city_buildings.png"))
    print("[OK] Created city_buildings.png")

def generate_city_props():
    W, H = 256, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Đèn đường LED hiện đại (Modern Streetlight - 32 x 64 at 0, 0)
    sx, sy = 0, 0
    draw.line([sx + 16, sy + 16, sx + 16, sy + 62], fill=(70, 75, 85, 255), width=3) # cột thép
    draw.line([sx + 16, sy + 16, sx + 28, sy + 10], fill=(70, 75, 85, 255), width=3) # tay đèn
    draw.rectangle([sx + 22, sy + 8, sx + 31, sy + 14], fill=(235, 240, 245, 255)) # đầu đèn
    draw.ellipse([sx + 23, sy + 11, sx + 30, sy + 15], fill=(255, 255, 200, 255)) # ánh sáng LED

    # 2. Cây ATM độc lập ngoài trời (Standalone ATM - 32 x 48 at 36, 0)
    ax, ay = 36, 12
    draw.rectangle([ax + 4, ay + 4, ax + 28, ay + 48], fill=(30, 75, 120, 255), outline=(210, 230, 250, 255), width=2)
    draw.rectangle([ax + 8, ay + 8, ax + 24, ay + 16], fill=(255, 215, 60, 255))
    draw.text((ax + 9, ay + 8), "ATM", fill=(20, 50, 80, 255))
    draw.rectangle([ax + 8, ay + 20, ax + 24, ay + 32], fill=(120, 220, 255, 255)) # màn hình
    draw.line([ax + 10, ay + 38, ax + 22, ay + 38], fill=(230, 235, 240, 255), width=2) # khe tiền

    # 3. Biển hiệu điện tử LED / Billboard (Digital Billboard - 64 x 48 at 72, 0)
    bx, by = 72, 8
    draw.rectangle([bx + 4, by + 4, bx + 60, by + 44], fill=(20, 22, 28, 255), outline=(80, 90, 110, 255), width=2)
    draw.rectangle([bx + 8, by + 8, bx + 56, by + 40], fill=(15, 45, 85, 255))
    # Hiệu ứng màn hình LED thành phố thông minh
    draw.text((bx + 18, by + 12), "SMART", fill=(80, 240, 255, 255))
    draw.text((bx + 21, by + 24), "CITY", fill=(255, 220, 70, 255))

    # 4. Cây cọ / Chậu cây cảnh đô thị (Urban Planter Tree - 48 x 64 at 140, 0)
    tx, ty = 140, 0
    # Chậu bê tông xám vuông
    draw.rectangle([tx + 14, ty + 46, tx + 34, ty + 62], fill=(140, 145, 155, 255), outline=(100, 105, 115, 255))
    # Thân cây
    draw.line([tx + 24, ty + 24, tx + 24, ty + 46], fill=(120, 80, 45, 255), width=3)
    # Tán lá nhiệt đới xanh mướt
    draw.ellipse([tx + 6, ty + 4, tx + 42, ty + 30], fill=(45, 145, 65, 255))
    draw.ellipse([tx + 12, ty + 8, tx + 36, ty + 24], fill=(80, 190, 95, 255))

    # 5. Ghế băng công viên hiện đại (Modern Park Bench - 48 x 32 at 0, 70)
    gx, gy = 0, 70
    draw.rectangle([gx + 6, gy + 14, gx + 42, gy + 20], fill=(160, 95, 45, 255))
    draw.rectangle([gx + 6, gy + 22, gx + 42, gy + 26], fill=(135, 75, 35, 255))
    draw.line([gx + 10, gy + 14, gx + 10, gy + 30], fill=(50, 55, 65, 255), width=2)
    draw.line([gx + 38, gy + 14, gx + 38, gy + 30], fill=(50, 55, 65, 255), width=2)

    # 6. Siêu xe thể thao màu đỏ / Cyber Roadster (64 x 32 at 60, 70)
    cx, cy = 60, 70
    # Thân xe khí động học
    draw.polygon([(cx + 4, cy + 22), (cx + 12, cy + 14), (cx + 44, cy + 14), (cx + 58, cy + 18), (cx + 62, cy + 25), (cx + 4, cy + 25)], fill=(225, 30, 40, 255))
    # Mui kính đen bóng (Tinted canopy)
    draw.polygon([(cx + 18, cy + 14), (cx + 26, cy + 8), (cx + 40, cy + 8), (cx + 46, cy + 14)], fill=(30, 35, 45, 255))
    # Bánh xe mâm đúc
    draw.ellipse([cx + 10, cy + 18, cx + 22, cy + 30], fill=(30, 30, 30, 255), outline=(180, 185, 190, 255))
    draw.ellipse([cx + 44, cy + 18, cx + 56, cy + 30], fill=(30, 30, 30, 255), outline=(180, 185, 190, 255))
    # Đèn LED pha mảnh
    draw.line([cx + 58, cy + 20, cx + 62, cy + 21], fill=(160, 240, 255, 255), width=2)

    img.save(os.path.join(ASSETS_DIR, "city_props.png"))
    print("[OK] Created city_props.png")

def generate_city_interiors():
    W, H = 512, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Quầy giao dịch Ngân Hàng có vách kính (Bank Teller Counter - 96 x 48 at 0, 0)
    bx, by = 0, 0
    # Mặt bàn gỗ sồi & chân đá cẩm thạch
    draw.rectangle([bx + 4, by + 20, bx + 92, by + 46], fill=(220, 225, 230, 255), outline=(150, 160, 175, 255), width=2)
    # Vách kính an ninh
    draw.rectangle([bx + 8, by + 4, bx + 88, by + 20], fill=(160, 220, 250, 180), outline=(210, 235, 250, 255))
    # Khe nhận tiền & micro nói chuyện
    draw.rectangle([bx + 38, by + 18, bx + 58, by + 23], fill=(80, 90, 105, 255))
    draw.text((bx + 26, by + 28), "QUẦY GIAO DỊCH", fill=(20, 70, 45, 255))

    # 2. Cửa kho tiền Titanium cực lớn (Vault Door - 48 x 64 at 100, 0)
    vx, vy = 100, 0
    draw.ellipse([vx + 2, vy + 4, vx + 46, vy + 60], fill=(85, 95, 110, 255), outline=(160, 175, 195, 255), width=3)
    draw.ellipse([vx + 10, vy + 12, vx + 38, vy + 52], fill=(65, 75, 90, 255), outline=(200, 215, 230, 255), width=2)
    # Vòng tay xoay mở khoá vàng
    draw.ellipse([vx + 18, vy + 24, vx + 30, vy + 40], fill=(240, 200, 60, 255), outline=(180, 140, 20, 255))
    draw.line([vx + 12, vy + 32, vx + 36, vy + 32], fill=(255, 225, 80, 255), width=2)
    draw.line([vx + 24, vy + 20, vx + 24, vy + 44], fill=(255, 225, 80, 255), width=2)

    # 3. Kệ hàng Snack siêu thị (Mart Gondola - 64 x 48 at 155, 0)
    mx, my = 155, 0
    draw.rectangle([mx + 4, my + 6, mx + 60, my + 46], fill=(230, 235, 240, 255), outline=(170, 180, 190, 255), width=2)
    # Các tầng kệ chứa bánh kẹo nhiều màu
    draw.line([mx + 6, my + 18, mx + 58, my + 18], fill=(230, 50, 50, 255), width=4) # bánh quy đỏ
    draw.line([mx + 6, my + 28, mx + 58, my + 28], fill=(245, 180, 30, 255), width=4) # khoai tây vàng
    draw.line([mx + 6, my + 38, mx + 58, my + 38], fill=(40, 160, 90, 255), width=4) # trà xanh

    # 4. Tủ mát đồ uống phát sáng (Drink Cooler Wall - 96 x 64 at 225, 0)
    cx, cy = 225, 0
    draw.rectangle([cx + 4, cy + 4, cx + 92, cy + 62], fill=(25, 45, 70, 255), outline=(140, 180, 220, 255), width=2)
    # 3 ô cửa kính mát lạnh
    for k in range(3):
        kx = cx + 8 + k * 28
        draw.rectangle([kx, cy + 8, kx + 24, cy + 58], fill=(140, 225, 255, 190), outline=(210, 240, 255, 255))
        # Lon nước ngọt & sữa
        draw.line([kx + 4, cy + 20, kx + 20, cy + 20], fill=(240, 40, 40, 255), width=3)
        draw.line([kx + 4, cy + 34, kx + 20, cy + 34], fill=(40, 200, 100, 255), width=3)
        draw.line([kx + 4, cy + 48, kx + 20, cy + 48], fill=(255, 220, 50, 255), width=3)

    # 5. Cửa Thang Máy Tòa Nhà Chọc Trời (Elevator Bank - 64 x 64 at 330, 0)
    ex, ey = 330, 0
    draw.rectangle([ex + 4, ey + 4, ex + 60, ey + 62], fill=(185, 195, 205, 255), outline=(130, 140, 150, 255), width=2)
    # Bảng số tầng LED
    draw.rectangle([ex + 22, ey + 8, ex + 42, ey + 18], fill=(20, 20, 20, 255))
    draw.text((ex + 26, ey + 8), "▲ 81", fill=(255, 60, 60, 255))
    # Cửa kim loại bạc trượt đôi
    draw.rectangle([ex + 10, ey + 20, ex + 31, ey + 62], fill=(225, 230, 235, 255), outline=(160, 170, 180, 255))
    draw.rectangle([ex + 33, ey + 20, ex + 54, ey + 62], fill=(225, 230, 235, 255), outline=(160, 170, 180, 255))

    # 6. Màn Hình OLED TV 85 inch Biệt Thự (OLED TV Wall - 64 x 64 at 400, 0)
    tx, ty = 400, 0
    # Vách ốp nan gỗ acoustic
    draw.rectangle([tx + 2, ty + 2, tx + 62, ty + 62], fill=(130, 80, 45, 255))
    for s in range(14):
        sx = tx + 4 + s * 4
        draw.line([sx, ty + 4, sx, ty + 60], fill=(100, 60, 30, 255), width=1)
    # Màn hình TV viền siêu mỏng hiển thị hình ảnh 4K
    draw.rectangle([tx + 8, ty + 12, tx + 56, ty + 44], fill=(10, 15, 25, 255), outline=(220, 225, 230, 255), width=1)
    draw.rectangle([tx + 10, ty + 14, tx + 54, ty + 42], fill=(30, 75, 140, 255)) # màn hình nền biển xanh

    # 7. Sofa Hiện Đại Chữ L (Modern Sectional Sofa - 64 x 48 at 0, 70)
    ox, oy = 0, 70
    # Nệm nỉ xám cao cấp
    draw.rectangle([ox + 4, oy + 8, ox + 60, oy + 28], fill=(195, 200, 208, 255), outline=(150, 155, 165, 255), width=2)
    draw.rectangle([ox + 40, oy + 28, ox + 60, oy + 44], fill=(195, 200, 208, 255), outline=(150, 155, 165, 255), width=2)
    # Gối tựa lưng vàng mù tạt & cam
    draw.rectangle([ox + 10, oy + 10, ox + 22, oy + 18], fill=(235, 190, 60, 255))
    draw.rectangle([ox + 26, oy + 10, ox + 38, oy + 18], fill=(225, 110, 65, 255))

    # 8. Đảo Bếp Hiện Đại (Kitchen Island - 64 x 32 at 70, 70)
    kx, ky = 70, 70
    draw.rectangle([kx + 4, ky + 6, kx + 60, ky + 30], fill=(245, 245, 248, 255), outline=(160, 165, 175, 255), width=2)
    draw.rectangle([kx + 6, ky + 8, kx + 58, ky + 14], fill=(45, 48, 55, 255)) # mặt đá thạch anh đen
    # Chậu rửa chén vòi inox
    draw.rectangle([kx + 12, ky + 16, kx + 24, ky + 24], fill=(185, 195, 205, 255))
    draw.line([kx + 18, ky + 12, kx + 18, ky + 18], fill=(225, 230, 235, 255), width=2)

    # 9. Quầy Lễ Tân Sky Tower (Executive Reception Desk - 96 x 48 at 140, 70)
    rx, ry = 140, 70
    # Thân quầy bo cong màu trắng bóng acrylic & viền LED xanh cyan
    draw.rounded_rectangle([rx + 4, ry + 16, rx + 92, ry + 44], radius=6, fill=(240, 245, 250, 255), outline=(90, 200, 240, 255), width=2)
    # Dải đèn LED phát sáng dưới chân quầy
    draw.line([rx + 10, ry + 42, rx + 86, ry + 42], fill=(40, 210, 255, 255), width=2)
    # Màn hình máy tính mỏng và bảng check-in cho khách
    draw.rectangle([rx + 38, ry + 4, rx + 58, ry + 18], fill=(25, 30, 40, 255), outline=(170, 185, 200, 255), width=1)
    draw.rectangle([rx + 40, ry + 6, rx + 56, ry + 16], fill=(50, 130, 200, 255)) # màn hình xanh
    draw.line([rx + 48, ry + 18, rx + 48, ry + 22], fill=(160, 170, 180, 255), width=2)
    # Logo chữ SKY 81
    draw.text((rx + 30, ry + 24), "SKY 81 LOBBY", fill=(30, 70, 110, 255))

    # 10. Quầy Thu Ngân Siêu Thị (Mart Cashier Counter - 80 x 48 at 240, 70)
    cx, cy = 240, 70
    draw.rectangle([cx + 4, cy + 12, cx + 76, cy + 44], fill=(235, 238, 242, 255), outline=(150, 160, 170, 255), width=2)
    # Băng chuyền hàng hóa màu đen
    draw.rectangle([cx + 8, cy + 16, cx + 46, cy + 26], fill=(40, 42, 48, 255))
    # Máy quét mã vạch và màn hình tính tiền POS
    draw.rectangle([cx + 52, cy + 6, cx + 70, cy + 22], fill=(30, 35, 45, 255), outline=(100, 110, 120, 255))
    draw.rectangle([cx + 54, cy + 8, cx + 68, cy + 18], fill=(80, 220, 130, 255)) # màn hình POS xanh lá
    # Giá kẹo cao su và pin trước quầy
    draw.line([cx + 10, cy + 32, cx + 44, cy + 32], fill=(240, 60, 60, 255), width=3)
    draw.line([cx + 10, cy + 38, cx + 44, cy + 38], fill=(250, 200, 40, 255), width=3)
    draw.text((cx + 18, cy + 24), "WINMART POS", fill=(200, 40, 40, 255))

    # 11. Bàn Ăn Mặt Đá Hiện Đại (Modern Dining Table - 80 x 48 at 325, 70)
    dx, dy = 325, 70
    # Mặt bàn đá phiến cẩm thạch trắng vân mây
    draw.rounded_rectangle([dx + 8, dy + 10, dx + 72, dy + 38], radius=4, fill=(248, 248, 250, 255), outline=(180, 185, 195, 255), width=2)
    # Bình hoa thủy tinh ở giữa bàn
    draw.ellipse([dx + 36, dy + 20, dx + 44, dy + 28], fill=(60, 170, 220, 200), outline=(255, 255, 255, 255))
    # 4 ghế ăn bọc da màu cam đất
    draw.rectangle([dx + 16, dy + 2, dx + 30, dy + 9], fill=(215, 115, 60, 255))
    draw.rectangle([dx + 50, dy + 2, dx + 64, dy + 9], fill=(215, 115, 60, 255))
    draw.rectangle([dx + 16, dy + 39, dx + 30, dy + 46], fill=(215, 115, 60, 255))
    draw.rectangle([dx + 50, dy + 39, dx + 64, dy + 46], fill=(215, 115, 60, 255))

    # 12. Bàn Trà Mặt Kính Đen (Modern Coffee Table - 44 x 28 at 410, 70)
    tx, ty = 410, 70
    draw.rounded_rectangle([tx + 4, ty + 4, tx + 40, ty + 24], radius=3, fill=(35, 40, 48, 255), outline=(130, 140, 155, 255), width=2)
    # Tạp chí & ly cà phê trên bàn
    draw.rectangle([tx + 10, ty + 8, tx + 20, ty + 16], fill=(240, 220, 180, 255))
    draw.ellipse([tx + 26, ty + 10, tx + 32, ty + 16], fill=(255, 255, 255, 255), outline=(160, 100, 50, 255))

    img.save(os.path.join(ASSETS_DIR, "city_interiors.png"))
    print("[OK] Created city_interiors.png")

def generate_city_npcs():
    W, H = 320, 32
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Banker Chị Mai (0..32, 0)
    ox = 0
    draw.rectangle([ox + 10, 3, ox + 22, 9], fill=(25, 25, 28, 255))
    draw.ellipse([ox + 13, 1, ox + 19, 5], fill=(25, 25, 28, 255))
    draw.rectangle([ox + 11, 7, ox + 21, 14], fill=(250, 215, 190, 255))
    draw.rectangle([ox + 13, 14, ox + 19, 16], fill=(240, 205, 180, 255))
    draw.point((ox + 13, 10), fill=(20, 20, 20, 255))
    draw.point((ox + 18, 10), fill=(20, 20, 20, 255))
    draw.rectangle([ox + 9, 16, ox + 23, 22], fill=(245, 248, 252, 255))
    draw.polygon([(ox + 14, 16), (ox + 18, 16), (ox + 17, 21), (ox + 15, 21)], fill=(30, 140, 75, 255))
    draw.rectangle([ox + 10, 18, ox + 12, 19], fill=(240, 200, 50, 255))
    draw.rectangle([ox + 7, 16, ox + 9, 21], fill=(245, 248, 252, 255))
    draw.rectangle([ox + 23, 16, ox + 25, 21], fill=(245, 248, 252, 255))
    draw.rectangle([ox + 7, 21, ox + 9, 23], fill=(250, 215, 190, 255))
    draw.rectangle([ox + 23, 21, ox + 25, 23], fill=(250, 215, 190, 255))
    draw.rectangle([ox + 11, 23, ox + 21, 27], fill=(30, 32, 38, 255))
    draw.line([ox + 13, 28, ox + 13, 31], fill=(25, 25, 28, 255), width=2)
    draw.line([ox + 18, 28, ox + 18, 31], fill=(25, 25, 28, 255), width=2)

    # 2. Bank Manager Anh Cường (32..64, 0)
    ox = 32
    draw.rectangle([ox + 11, 3, ox + 21, 7], fill=(25, 25, 30, 255))
    draw.rectangle([ox + 11, 7, ox + 21, 14], fill=(245, 210, 185, 255))
    draw.point((ox + 13, 9), fill=(15, 15, 15, 255))
    draw.point((ox + 18, 9), fill=(15, 15, 15, 255))
    draw.rectangle([ox + 8, 14, ox + 24, 23], fill=(35, 48, 75, 255))
    draw.polygon([(ox + 14, 14), (ox + 18, 14), (ox + 16, 17)], fill=(250, 250, 255, 255))
    draw.line([ox + 16, 16, ox + 16, 21], fill=(195, 35, 35, 255), width=2)
    draw.rectangle([ox + 6, 15, ox + 8, 21], fill=(35, 48, 75, 255))
    draw.rectangle([ox + 24, 15, ox + 26, 21], fill=(35, 48, 75, 255))
    draw.point((ox + 7, 21), fill=(240, 200, 40, 255))
    draw.rectangle([ox + 6, 22, ox + 8, 23], fill=(245, 210, 185, 255))
    draw.rectangle([ox + 24, 22, ox + 26, 23], fill=(245, 210, 185, 255))
    draw.rectangle([ox + 11, 23, ox + 15, 28], fill=(35, 48, 75, 255))
    draw.rectangle([ox + 17, 23, ox + 21, 28], fill=(35, 48, 75, 255))
    draw.rectangle([ox + 11, 29, ox + 15, 31], fill=(20, 20, 25, 255))
    draw.rectangle([ox + 17, 29, ox + 21, 31], fill=(20, 20, 25, 255))

    # 3. Receptionist Thư Ký Phương (64..96, 0)
    ox = 64
    draw.rectangle([ox + 10, 3, ox + 22, 9], fill=(85, 50, 30, 255))
    draw.line([ox + 21, 6, ox + 24, 14], fill=(85, 50, 30, 255), width=2)
    draw.rectangle([ox + 9, 8, ox + 11, 11], fill=(180, 190, 200, 255))
    draw.point((ox + 12, 11), fill=(40, 180, 240, 255))
    draw.rectangle([ox + 11, 7, ox + 21, 14], fill=(255, 220, 195, 255))
    draw.point((ox + 13, 10), fill=(30, 20, 20, 255))
    draw.point((ox + 18, 10), fill=(30, 20, 20, 255))
    draw.point((ox + 15, 12), fill=(230, 90, 90, 255))
    draw.rectangle([ox + 8, 14, ox + 24, 23], fill=(120, 125, 135, 255))
    draw.rectangle([ox + 14, 14, ox + 18, 19], fill=(255, 255, 255, 255))
    draw.point((ox + 11, 17), fill=(40, 210, 255, 255))
    draw.rectangle([ox + 6, 15, ox + 8, 21], fill=(120, 125, 135, 255))
    draw.rectangle([ox + 24, 15, ox + 26, 21], fill=(120, 125, 135, 255))
    draw.rectangle([ox + 6, 22, ox + 8, 23], fill=(255, 220, 195, 255))
    draw.rectangle([ox + 24, 22, ox + 26, 23], fill=(255, 220, 195, 255))
    draw.rectangle([ox + 11, 23, ox + 21, 27], fill=(100, 105, 115, 255))
    draw.line([ox + 13, 28, ox + 13, 31], fill=(50, 50, 55, 255), width=2)
    draw.line([ox + 18, 28, ox + 18, 31], fill=(50, 50, 55, 255), width=2)

    # 4. Security Guard Anh Tuấn (96..128, 0)
    ox = 96
    draw.rectangle([ox + 9, 2, ox + 23, 6], fill=(30, 42, 65, 255))
    draw.line([ox + 8, 6, ox + 24, 6], fill=(230, 190, 50, 255), width=1)
    draw.point((ox + 16, 4), fill=(250, 215, 60, 255))
    draw.rectangle([ox + 11, 7, ox + 21, 14], fill=(235, 195, 165, 255))
    draw.point((ox + 13, 10), fill=(20, 20, 20, 255))
    draw.point((ox + 18, 10), fill=(20, 20, 20, 255))
    draw.rectangle([ox + 8, 14, ox + 24, 22], fill=(45, 65, 100, 255))
    draw.point((ox + 9, 14), fill=(240, 200, 50, 255))
    draw.point((ox + 23, 14), fill=(240, 200, 50, 255))
    draw.point((ox + 12, 17), fill=(255, 215, 60, 255))
    draw.rectangle([ox + 6, 12, ox + 8, 18], fill=(25, 25, 30, 255))
    draw.rectangle([ox + 8, 22, ox + 24, 24], fill=(25, 28, 35, 255))
    draw.point((ox + 16, 23), fill=(220, 180, 50, 255))
    draw.rectangle([ox + 10, 24, ox + 14, 28], fill=(35, 48, 72, 255))
    draw.rectangle([ox + 18, 24, ox + 22, 28], fill=(35, 48, 72, 255))
    draw.rectangle([ox + 9, 29, ox + 14, 31], fill=(20, 22, 28, 255))
    draw.rectangle([ox + 18, 29, ox + 23, 31], fill=(20, 22, 28, 255))

    # 5. WinMart Cashier Em Linh (128..160, 0)
    ox = 128
    draw.rectangle([ox + 10, 3, ox + 22, 6], fill=(220, 40, 40, 255))
    draw.line([ox + 8, 6, ox + 24, 6], fill=(255, 255, 255, 255), width=1)
    draw.rectangle([ox + 11, 7, ox + 13, 12], fill=(70, 45, 30, 255))
    draw.rectangle([ox + 19, 7, ox + 21, 12], fill=(70, 45, 30, 255))
    draw.rectangle([ox + 12, 7, ox + 20, 14], fill=(255, 220, 195, 255))
    draw.point((ox + 14, 10), fill=(30, 25, 25, 255))
    draw.point((ox + 18, 10), fill=(30, 25, 25, 255))
    draw.point((ox + 16, 12), fill=(230, 100, 100, 255))
    draw.rectangle([ox + 8, 14, ox + 24, 23], fill=(220, 40, 40, 255))
    draw.rectangle([ox + 11, 18, ox + 21, 23], fill=(45, 48, 55, 255))
    draw.rectangle([ox + 12, 19, ox + 15, 20], fill=(255, 255, 255, 255))
    draw.rectangle([ox + 11, 24, ox + 14, 28], fill=(30, 32, 38, 255))
    draw.rectangle([ox + 18, 24, ox + 21, 28], fill=(30, 32, 38, 255))
    draw.rectangle([ox + 10, 29, ox + 14, 31], fill=(245, 245, 245, 255))
    draw.rectangle([ox + 18, 29, ox + 22, 31], fill=(245, 245, 245, 255))

    # 6. Trendy Mart Customer Anh Hoàng (160..192, 0)
    ox = 160
    draw.arc([ox + 10, 2, ox + 22, 10], start=180, end=0, fill=(245, 245, 250, 255), width=2)
    draw.rectangle([ox + 8, 7, ox + 10, 11], fill=(245, 245, 250, 255))
    draw.rectangle([ox + 22, 7, ox + 24, 11], fill=(245, 245, 250, 255))
    draw.rectangle([ox + 11, 4, ox + 21, 8], fill=(35, 30, 35, 255))
    draw.rectangle([ox + 11, 8, ox + 21, 14], fill=(245, 215, 190, 255))
    draw.point((ox + 13, 10), fill=(20, 20, 20, 255))
    draw.point((ox + 18, 10), fill=(20, 20, 20, 255))
    draw.rectangle([ox + 7, 14, ox + 25, 23], fill=(230, 175, 45, 255))
    draw.line([ox + 14, 16, ox + 14, 19], fill=(255, 255, 255, 255), width=1)
    draw.line([ox + 18, 16, ox + 18, 19], fill=(255, 255, 255, 255), width=1)
    draw.rectangle([ox + 10, 23, ox + 14, 28], fill=(60, 100, 150, 255))
    draw.rectangle([ox + 18, 23, ox + 22, 28], fill=(60, 100, 150, 255))
    draw.rectangle([ox + 9, 29, ox + 14, 31], fill=(250, 250, 250, 255))
    draw.line([ox + 9, 31, ox + 14, 31], fill=(220, 50, 50, 255), width=1)
    draw.rectangle([ox + 18, 29, ox + 23, 31], fill=(250, 250, 250, 255))
    draw.line([ox + 18, 31, ox + 23, 31], fill=(220, 50, 50, 255), width=1)

    # 7. Jarvis AI Butler (192..224, 0)
    ox = 192
    draw.rectangle([ox + 11, 3, ox + 21, 7], fill=(200, 205, 215, 255))
    draw.point((ox + 10, 8), fill=(40, 230, 255, 255))
    draw.rectangle([ox + 11, 7, ox + 21, 14], fill=(245, 225, 215, 255))
    draw.point((ox + 13, 9), fill=(30, 140, 220, 255))
    draw.point((ox + 18, 9), fill=(30, 140, 220, 255))
    draw.rectangle([ox + 8, 14, ox + 24, 23], fill=(20, 22, 28, 255))
    draw.polygon([(ox + 13, 14), (ox + 19, 14), (ox + 16, 20)], fill=(255, 255, 255, 255))
    draw.point((ox + 16, 16), fill=(10, 10, 15, 255))
    draw.point((ox + 15, 16), fill=(10, 10, 15, 255))
    draw.point((ox + 17, 16), fill=(10, 10, 15, 255))
    draw.rectangle([ox + 6, 20, ox + 8, 22], fill=(250, 250, 255, 255))
    draw.rectangle([ox + 24, 20, ox + 26, 22], fill=(250, 250, 255, 255))
    draw.rectangle([ox + 11, 23, ox + 15, 28], fill=(20, 22, 28, 255))
    draw.rectangle([ox + 17, 23, ox + 21, 28], fill=(20, 22, 28, 255))
    draw.rectangle([ox + 10, 29, ox + 15, 31], fill=(10, 12, 16, 255))
    draw.rectangle([ox + 17, 29, ox + 22, 31], fill=(10, 12, 16, 255))

    # 8. Tech CEO Minh (224..256, 0)
    ox = 224
    draw.rectangle([ox + 11, 3, ox + 21, 7], fill=(30, 25, 25, 255))
    draw.rectangle([ox + 11, 7, ox + 21, 14], fill=(245, 210, 185, 255))
    draw.rectangle([ox + 12, 8, ox + 15, 10], outline=(15, 15, 20, 255))
    draw.rectangle([ox + 17, 8, ox + 20, 10], outline=(15, 15, 20, 255))
    draw.line([ox + 15, 9, ox + 17, 9], fill=(15, 15, 20, 255))
    draw.rectangle([ox + 8, 14, ox + 24, 23], fill=(65, 70, 78, 255))
    draw.rectangle([ox + 14, 14, ox + 18, 17], fill=(25, 25, 30, 255))
    draw.rectangle([ox + 4, 18, ox + 8, 24], fill=(190, 200, 210, 255), outline=(130, 140, 150, 255))
    draw.rectangle([ox + 11, 23, ox + 15, 28], fill=(55, 60, 68, 255))
    draw.rectangle([ox + 17, 23, ox + 21, 28], fill=(55, 60, 68, 255))
    draw.rectangle([ox + 10, 29, ox + 15, 31], fill=(125, 65, 25, 255))
    draw.rectangle([ox + 17, 29, ox + 22, 31], fill=(125, 65, 25, 255))

    # 9. Shipper Thành (256..288, 0)
    ox = 256
    draw.rectangle([ox + 10, 2, ox + 22, 7], fill=(35, 185, 85, 255))
    draw.rectangle([ox + 11, 7, ox + 21, 9], fill=(40, 45, 55, 255))
    draw.rectangle([ox + 12, 9, ox + 20, 14], fill=(235, 185, 150, 255))
    draw.point((ox + 14, 11), fill=(20, 20, 20, 255))
    draw.point((ox + 18, 11), fill=(20, 20, 20, 255))
    draw.rectangle([ox + 7, 14, ox + 25, 23], fill=(35, 185, 85, 255))
    draw.line([ox + 7, 18, ox + 25, 18], fill=(240, 255, 150, 255), width=2)
    draw.line([ox + 10, 14, ox + 10, 22], fill=(25, 25, 30, 255), width=1)
    draw.line([ox + 22, 14, ox + 22, 22], fill=(25, 25, 30, 255), width=1)
    draw.rectangle([ox + 10, 23, ox + 14, 28], fill=(45, 50, 58, 255))
    draw.rectangle([ox + 18, 23, ox + 22, 28], fill=(45, 50, 58, 255))
    draw.rectangle([ox + 9, 29, ox + 14, 31], fill=(30, 140, 70, 255))
    draw.rectangle([ox + 18, 29, ox + 23, 31], fill=(30, 140, 70, 255))

    # 10. Tourist / Office Lady Hương (288..320, 0)
    ox = 288
    draw.rectangle([ox + 12, 2, ox + 20, 4], fill=(30, 30, 35, 255))
    draw.rectangle([ox + 10, 4, ox + 22, 10], fill=(135, 80, 50, 255))
    draw.line([ox + 9, 8, ox + 9, 16], fill=(135, 80, 50, 255), width=2)
    draw.line([ox + 23, 8, ox + 23, 16], fill=(135, 80, 50, 255), width=2)
    draw.rectangle([ox + 11, 7, ox + 21, 14], fill=(255, 225, 200, 255))
    draw.point((ox + 13, 10), fill=(40, 25, 25, 255))
    draw.point((ox + 18, 10), fill=(40, 25, 25, 255))
    draw.point((ox + 16, 12), fill=(240, 110, 120, 255))
    draw.rectangle([ox + 8, 14, ox + 24, 25], fill=(240, 185, 195, 255))
    draw.line([ox + 16, 14, ox + 16, 25], fill=(225, 160, 175, 255), width=1)
    draw.line([ox + 10, 14, ox + 25, 21], fill=(235, 195, 60, 255), width=1)
    draw.rectangle([ox + 24, 20, ox + 28, 24], fill=(230, 215, 190, 255))
    draw.line([ox + 13, 26, ox + 13, 31], fill=(205, 170, 135, 255), width=2)
    draw.line([ox + 18, 26, ox + 18, 31], fill=(205, 170, 135, 255), width=2)

    img.save(os.path.join(ASSETS_DIR, "city_npcs.png"))
    print("[OK] Created city_npcs.png")

if __name__ == "__main__":
    generate_city_buildings()
    generate_city_props()
    generate_city_interiors()
    generate_city_npcs()
    print("=== All Modern City Assets Generated Successfully! ===")
