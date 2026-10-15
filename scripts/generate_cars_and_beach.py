import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_cars():
    # 5 types of cars, 2 directions (East=Facing Right, West=Facing Left)
    # Each cell: 72 x 36
    W, H = 360, 72
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    car_palettes = [
        {"body": (30, 115, 215, 255), "roof": (20, 95, 185, 255), "taxi": True, "name": "Blue Taxi"},
        {"body": (215, 45, 45, 255), "roof": (180, 30, 30, 255), "taxi": False, "name": "Red Sedan"},
        {"body": (235, 238, 242, 255), "roof": (210, 215, 222, 255), "van": True, "taxi": False, "name": "White Van"},
        {"body": (35, 160, 85, 255), "roof": (25, 130, 68, 255), "taxi": True, "name": "Green Taxi"},
        {"body": (245, 180, 25, 255), "roof": (215, 150, 15, 255), "taxi": False, "name": "Yellow Compact"},
    ]

    for col, pal in enumerate(car_palettes):
        # Row 0: Facing East (Right)
        x0 = col * 72
        y0 = 0
        draw_car(draw, x0 + 4, y0 + 6, pal, facing_right=True)

        # Row 1: Facing West (Left)
        y1 = 36
        draw_car(draw, x0 + 4, y1 + 6, pal, facing_right=False)

    img.save(os.path.join(ASSETS_DIR, "cars.png"))
    print("Created cars.png successfully!")

def draw_car(draw, cx, cy, pal, facing_right=True):
    # Base car dimensions: width ~62, height ~24
    w, h = 62, 24
    b_col = pal["body"]
    r_col = pal["roof"]
    is_van = pal.get("van", False)
    is_taxi = pal.get("taxi", False)

    # Shadow underneath
    draw.ellipse([cx + 2, cy + h - 4, cx + w - 2, cy + h + 2], fill=(20, 25, 30, 110))

    if facing_right:
        # Car body (front is right cx+w, back is left cx)
        if is_van:
            # Boxy van body
            draw.rounded_rectangle([cx + 2, cy + 2, cx + w - 2, cy + h - 5], radius=4, fill=b_col, outline=(40, 45, 50, 255))
            # Windshield (Right)
            draw.polygon([(cx + w - 16, cy + 4), (cx + w - 4, cy + 11), (cx + w - 16, cy + 11)], fill=(160, 220, 245, 255))
            # Side windows
            draw.rectangle([cx + 28, cy + 4, cx + w - 18, cy + 11], fill=(160, 220, 245, 255))
            draw.rectangle([cx + 10, cy + 4, cx + 25, cy + 11], fill=(160, 220, 245, 255))
        else:
            # Sedan body: lower rect
            draw.rounded_rectangle([cx + 2, cy + 8, cx + w - 2, cy + h - 5], radius=3, fill=b_col, outline=(30, 35, 40, 255))
            # Cabin / roof
            draw.polygon([(cx + 12, cy + 8), (cx + 18, cy + 2), (cx + w - 16, cy + 2), (cx + w - 10, cy + 8)], fill=r_col, outline=(30, 35, 40, 255))
            # Front windshield
            draw.polygon([(cx + w - 16, cy + 3), (cx + w - 11, cy + 8), (cx + w - 22, cy + 8), (cx + w - 22, cy + 3)], fill=(170, 225, 245, 255))
            # Side window
            draw.rectangle([cx + 19, cy + 3, cx + w - 24, cy + 8], fill=(170, 225, 245, 255))

        # Headlight (Right)
        draw.rectangle([cx + w - 3, cy + 10, cx + w - 1, cy + 14], fill=(255, 250, 160, 255))
        # Taillight (Left)
        draw.rectangle([cx + 1, cy + 10, cx + 3, cy + 14], fill=(240, 30, 30, 255))

        # Taxi sign on roof
        if is_taxi:
            draw.rectangle([cx + 26, cy - 2, cx + 38, cy + 2], fill=(255, 230, 30, 255), outline=(20, 20, 20, 255))
            draw.point((cx + 31, cy), fill=(20, 20, 20, 255))
            draw.point((cx + 33, cy), fill=(20, 20, 20, 255))

        # Wheels
        draw.ellipse([cx + 9, cy + h - 9, cx + 19, cy + h + 1], fill=(25, 25, 25, 255))
        draw.ellipse([cx + 12, cy + h - 6, cx + 16, cy + h - 2], fill=(190, 195, 200, 255)) # Rim

        draw.ellipse([cx + w - 19, cy + h - 9, cx + w - 9, cy + h + 1], fill=(25, 25, 25, 255))
        draw.ellipse([cx + w - 16, cy + h - 6, cx + w - 12, cy + h - 2], fill=(190, 195, 200, 255)) # Rim

    else:
        # Car body (front is left cx, back is right cx+w)
        if is_van:
            draw.rounded_rectangle([cx + 2, cy + 2, cx + w - 2, cy + h - 5], radius=4, fill=b_col, outline=(40, 45, 50, 255))
            # Windshield (Left)
            draw.polygon([(cx + 16, cy + 4), (cx + 4, cy + 11), (cx + 16, cy + 11)], fill=(160, 220, 245, 255))
            # Side windows
            draw.rectangle([cx + 18, cy + 4, cx + w - 28, cy + 11], fill=(160, 220, 245, 255))
            draw.rectangle([cx + w - 25, cy + 4, cx + w - 10, cy + 11], fill=(160, 220, 245, 255))
        else:
            draw.rounded_rectangle([cx + 2, cy + 8, cx + w - 2, cy + h - 5], radius=3, fill=b_col, outline=(30, 35, 40, 255))
            # Cabin / roof
            draw.polygon([(cx + 10, cy + 8), (cx + 16, cy + 2), (cx + w - 18, cy + 2), (cx + w - 12, cy + 8)], fill=r_col, outline=(30, 35, 40, 255))
            # Front windshield (Left)
            draw.polygon([(cx + 16, cy + 3), (cx + 11, cy + 8), (cx + 22, cy + 8), (cx + 22, cy + 3)], fill=(170, 225, 245, 255))
            # Side window
            draw.rectangle([cx + 24, cy + 3, cx + w - 19, cy + 8], fill=(170, 225, 245, 255))

        # Headlight (Left)
        draw.rectangle([cx + 1, cy + 10, cx + 3, cy + 14], fill=(255, 250, 160, 255))
        # Taillight (Right)
        draw.rectangle([cx + w - 3, cy + 10, cx + w - 1, cy + 14], fill=(240, 30, 30, 255))

        # Taxi sign on roof
        if is_taxi:
            draw.rectangle([cx + 24, cy - 2, cx + 36, cy + 2], fill=(255, 230, 30, 255), outline=(20, 20, 20, 255))
            draw.point((cx + 29, cy), fill=(20, 20, 20, 255))
            draw.point((cx + 31, cy), fill=(20, 20, 20, 255))

        # Wheels
        draw.ellipse([cx + 9, cy + h - 9, cx + 19, cy + h + 1], fill=(25, 25, 25, 255))
        draw.ellipse([cx + 12, cy + h - 6, cx + 16, cy + h - 2], fill=(190, 195, 200, 255))

        draw.ellipse([cx + w - 19, cy + h - 9, cx + w - 9, cy + h + 1], fill=(25, 25, 25, 255))
        draw.ellipse([cx + w - 16, cy + h - 6, cx + w - 12, cy + h - 2], fill=(190, 195, 200, 255))

def generate_beach_props():
    W, H = 256, 128
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Cầu thang đi xuống bãi cát ra biển (64 x 48 at 0, 0)
    sx, sy = 0, 0
    # Nền các bậc thang đá granite xám nhạt với gờ bóng & đổ bóng
    steps = 6
    step_h = 7
    for i in range(steps):
        y_step = sy + 3 + i * step_h
        # Bề mặt bậc
        draw.rectangle([sx + 6, y_step, sx + 57, y_step + 4], fill=(215, 220, 225, 255))
        # Gờ bậc nổi sáng
        draw.line([sx + 6, y_step, sx + 57, y_step], fill=(245, 248, 250, 255), width=1)
        # Rãnh đổ bóng dưới bậc
        draw.rectangle([sx + 6, y_step + 4, sx + 57, y_step + step_h - 1], fill=(155, 162, 170, 255))

    # Lan can hai bên (trái & phải) tay vịn gỗ nâu viền vàng
    # Lan can trái
    draw.rectangle([sx + 2, sy + 2, sx + 6, sy + 44], fill=(120, 75, 45, 255), outline=(75, 45, 25, 255))
    draw.line([sx + 3, sy + 2, sx + 3, sy + 44], fill=(195, 135, 80, 255))
    # Trụ lan can trái
    draw.rectangle([sx + 1, sy + 1, sx + 7, sy + 7], fill=(230, 200, 70, 255), outline=(130, 95, 30, 255))
    draw.rectangle([sx + 1, sy + 40, sx + 7, sy + 46], fill=(230, 200, 70, 255), outline=(130, 95, 30, 255))

    # Lan can phải
    draw.rectangle([sx + 57, sy + 2, sx + 61, sy + 44], fill=(120, 75, 45, 255), outline=(75, 45, 25, 255))
    draw.line([sx + 58, sy + 2, sx + 58, sy + 44], fill=(195, 135, 80, 255))
    # Trụ lan can phải
    draw.rectangle([sx + 56, sy + 1, sx + 62, sy + 7], fill=(230, 200, 70, 255), outline=(130, 95, 30, 255))
    draw.rectangle([sx + 56, sy + 40, sx + 62, sy + 46], fill=(230, 200, 70, 255), outline=(130, 95, 30, 255))

    # 2. Dù che bãi biển sọc nhiệt đới (48 x 48 at 64, 0)
    ux, uy = 64, 0
    # Bóng đổ
    draw.ellipse([ux + 8, uy + 38, ux + 40, uy + 46], fill=(20, 40, 60, 60))
    # Cột dù cắm cát
    draw.line([ux + 24, uy + 16, ux + 24, uy + 42], fill=(160, 130, 90, 255), width=2)
    # Tán dù hình nón sọc đỏ - trắng
    draw.polygon([(ux + 4, uy + 20), (ux + 24, uy + 4), (ux + 44, uy + 20)], fill=(235, 45, 45, 255), outline=(180, 30, 30, 255))
    for px in [ux + 14, ux + 24, ux + 34]:
        draw.line([px, uy + 10, px, uy + 20], fill=(255, 255, 255, 255), width=3)
    draw.polygon([(ux + 22, uy + 2), (ux + 26, uy + 2), (ux + 24, uy + 5)], fill=(255, 215, 0, 255))

    # 3. Ghế phơi nắng bãi biển (32 x 32 at 112, 0)
    gx, gy = 112, 0
    draw.ellipse([gx + 4, gy + 22, gx + 28, gy + 28], fill=(20, 40, 60, 50))
    # Khung gỗ ngả lưng
    draw.polygon([(gx + 4, gy + 8), (gx + 12, gy + 18), (gx + 26, gy + 18), (gx + 28, gy + 22)], fill=(150, 105, 60, 255))
    # Đệm vải sọc xanh ngọc
    draw.line([gx + 5, gy + 9, gx + 12, gy + 17], fill=(40, 190, 210, 255), width=3)
    draw.line([gx + 12, gy + 17, gx + 26, gy + 17], fill=(40, 190, 210, 255), width=3)
    draw.line([gx + 8, gy + 17, gx + 8, gy + 24], fill=(120, 80, 40, 255), width=2)
    draw.line([gx + 24, gy + 17, gx + 24, gy + 24], fill=(120, 80, 40, 255), width=2)

    # 4. Sóng biển bọt trắng rì rào (64 x 24 at 144, 0)
    wx, wy = 144, 0
    # Nước biển xanh ngọc
    draw.rectangle([wx, wy, wx + 63, wy + 14], fill=(65, 175, 225, 255))
    # Bọt sóng trắng viền bãi cát
    for bx in range(wx, wx + 60, 8):
        draw.ellipse([bx, wy + 10, bx + 10, wy + 18], fill=(245, 255, 255, 230))
        draw.ellipse([bx + 3, wy + 14, bx + 9, wy + 20], fill=(215, 245, 255, 180))

    # 5. Cua biển & Vỏ sò đại dương (32 x 32 at 208, 0)
    cx, cy = 208, 0
    # Chú cua đỏ tí hon
    draw.ellipse([cx + 6, cy + 6, cx + 18, cy + 14], fill=(235, 65, 35, 255))
    # 2 Càng cua
    draw.ellipse([cx + 2, cy + 3, cx + 6, cy + 8], fill=(235, 65, 35, 255))
    draw.ellipse([cx + 18, cy + 3, cx + 22, cy + 8], fill=(235, 65, 35, 255))
    # Mắt cua
    draw.point((cx + 9, cy + 7), fill=(255, 255, 255, 255))
    draw.point((cx + 15, cy + 7), fill=(255, 255, 255, 255))
    draw.point((cx + 10, cy + 7), fill=(0, 0, 0, 255))
    draw.point((cx + 14, cy + 7), fill=(0, 0, 0, 255))
    # Vỏ sò xoắn ốc hồng phấn bên cạnh
    draw.polygon([(cx + 18, cy + 20), (cx + 28, cy + 18), (cx + 24, cy + 28)], fill=(255, 195, 190, 255), outline=(215, 140, 140, 255))

    # 6. Lan can bờ kè đại lộ (64 x 24 at 0, 48)
    rx, ry = 0, 48
    draw.rectangle([rx, ry + 4, rx + 63, ry + 8], fill=(220, 225, 230, 255), outline=(160, 168, 175, 255))
    for px in range(rx + 4, rx + 64, 8):
        draw.line([px, ry + 8, px, ry + 20], fill=(190, 195, 202, 255), width=2)
    draw.rectangle([rx, ry + 18, rx + 63, ry + 22], fill=(175, 182, 190, 255))

    img.save(os.path.join(ASSETS_DIR, "beach_props.png"))
    print("Created beach_props.png successfully!")

def generate_street_vendors():
    # 4 distinct street vendors (64 x 48 each)
    W, H = 256, 48
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Chị Ba Bán Nước Mía & Dừa Xiêm Lạnh (0, 0)
    vx, vy = 0, 0
    # Bóng đổ
    draw.ellipse([vx + 6, vy + 38, vx + 58, vy + 46], fill=(20, 30, 40, 70))
    # Xe inox nước mía
    draw.rectangle([vx + 8, vy + 18, vx + 38, vy + 40], fill=(215, 222, 228, 255), outline=(130, 138, 145, 255))
    # Buồng kính đựng mía
    draw.rectangle([vx + 10, vy + 6, vx + 26, vy + 18], fill=(195, 235, 250, 180), outline=(140, 160, 180, 255))
    # Cây mía cạo vỏ màu xanh vàng bên trong buồng kính
    draw.line([vx + 14, vy + 7, vx + 14, vy + 17], fill=(160, 215, 75, 255), width=2)
    draw.line([vx + 18, vy + 7, vx + 18, vy + 17], fill=(175, 225, 85, 255), width=2)
    draw.line([vx + 22, vy + 7, vy + 7, vy + 17], fill=(160, 215, 75, 255), width=2)
    # Bánh đà quay tay màu đỏ
    draw.ellipse([vx + 27, vy + 10, vx + 35, vy + 18], fill=(225, 45, 45, 255), outline=(150, 25, 25, 255))
    # Chùm dừa xiêm xanh treo lủng lẳng
    draw.ellipse([vx + 34, vy + 14, vx + 40, vy + 20], fill=(105, 175, 60, 255))
    draw.ellipse([vx + 38, vy + 16, vx + 44, vy + 22], fill=(115, 185, 70, 255))
    # Bánh xe đẩy bên dưới
    draw.ellipse([vx + 10, vy + 36, vx + 18, vy + 44], fill=(40, 40, 40, 255))
    draw.ellipse([vx + 28, vy + 36, vx + 36, vy + 44], fill=(40, 40, 40, 255))
    # Cô bán hàng mặc áo hoa xanh, nón lá
    draw.polygon([(vx + 42, vy + 10), (vx + 54, vy + 10), (vx + 48, vy + 4)], fill=(235, 220, 160, 255), outline=(180, 160, 100, 255)) # Nón lá
    draw.rectangle([vx + 45, vy + 11, vx + 51, vy + 15], fill=(255, 215, 185, 255)) # Mặt
    draw.rectangle([vx + 44, vy + 16, vx + 52, vy + 28], fill=(50, 160, 185, 255)) # Áo bà ba ngọc bích
    draw.rectangle([vx + 45, vy + 29, vx + 51, vy + 38], fill=(30, 35, 40, 255)) # Quần đen

    # 2. Bác Tư Gánh Bánh Mì Nóng Giòn & Trái Cây (64, 0)
    vx, vy = 64, 0
    draw.ellipse([vx + 4, vy + 38, vx + 60, vy + 46], fill=(20, 30, 40, 70))
    # Người gánh hàng rong ở giữa
    # Nón lá
    draw.polygon([(vx + 26, vy + 8), (vx + 38, vy + 8), (vx + 32, vy + 2)], fill=(235, 220, 160, 255), outline=(180, 160, 100, 255))
    draw.rectangle([vx + 29, vy + 9, vx + 35, vy + 13], fill=(255, 210, 180, 255))
    draw.rectangle([vx + 28, vy + 14, vx + 36, vy + 26], fill=(130, 75, 40, 255)) # Áo nâu sồng
    draw.rectangle([vx + 29, vy + 27, vx + 35, vy + 37], fill=(40, 40, 45, 255))
    # Đòn gánh tre uốn cong
    draw.arc([vx + 8, vy + 10, vx + 56, vy + 22], start=180, end=360, fill=(190, 150, 90, 255), width=2)
    # Thúng trước (Bánh mì vàng ươm dựng đứng)
    draw.ellipse([vx + 6, vy + 22, vx + 22, vy + 36], fill=(185, 140, 80, 255), outline=(120, 85, 45, 255))
    for bx in [vx + 8, vx + 12, vx + 16]:
        draw.rectangle([bx, vy + 16, bx + 3, vy + 25], fill=(235, 175, 55, 255), outline=(160, 100, 30, 255))
    # Thúng sau (Trái cây: chuối vàng, cam tròn)
    draw.ellipse([vx + 42, vy + 22, vx + 58, vy + 36], fill=(185, 140, 80, 255), outline=(120, 85, 45, 255))
    draw.ellipse([vx + 44, vy + 20, vx + 49, vy + 25], fill=(245, 140, 20, 255)) # Cam
    draw.ellipse([vx + 51, vy + 19, vx + 56, vy + 24], fill=(245, 215, 30, 255)) # Chuối

    # 3. Anh Bảy Bán Cá Viên Chiên & Bắp Xào Bơ (128, 0)
    vx, vy = 128, 0
    draw.ellipse([vx + 6, vy + 38, vx + 58, vy + 46], fill=(20, 30, 40, 70))
    # Xe đẩy inox
    draw.rectangle([vx + 10, vy + 18, vx + 42, vy + 38], fill=(205, 212, 218, 255), outline=(120, 128, 135, 255))
    # Bếp ga & Chảo dầu đang sôi
    draw.ellipse([vx + 14, vy + 16, vx + 28, vy + 22], fill=(60, 65, 70, 255))
    draw.ellipse([vx + 16, vy + 17, vx + 26, vy + 21], fill=(235, 185, 60, 255)) # Dầu sôi vàng
    # Khay xiên que nhiều màu
    draw.rectangle([vx + 30, vy + 14, vx + 40, vy + 20], fill=(240, 240, 240, 255))
    draw.line([vx + 32, vy + 12, vx + 32, vy + 18], fill=(215, 50, 40, 255), width=2) # Xúc xích đỏ
    draw.line([vx + 36, vy + 12, vx + 36, vy + 18], fill=(235, 215, 160, 255), width=2) # Cá viên
    # Bánh xe đẩy
    draw.ellipse([vx + 12, vy + 34, vx + 20, vy + 42], fill=(40, 40, 40, 255))
    draw.ellipse([vx + 32, vy + 34, vx + 40, vy + 42], fill=(40, 40, 40, 255))
    # Người bán thanh niên áo thun đỏ, tạp dề trắng
    draw.ellipse([vx + 46, vy + 6, vx + 54, vy + 14], fill=(255, 210, 180, 255)) # Đầu
    draw.rectangle([vx + 45, vy + 14, vx + 55, vy + 26], fill=(220, 40, 40, 255)) # Áo đỏ
    draw.rectangle([vx + 47, vy + 17, vx + 53, vy + 28], fill=(250, 250, 250, 255)) # Tạp dề
    draw.rectangle([vx + 47, vy + 27, vx + 53, vy + 37], fill=(50, 65, 80, 255)) # Quần jean

    # 4. Cô Năm Quán Nước & Trà Đá Vỉa Hè (192, 0)
    vx, vy = 192, 0
    draw.ellipse([vx + 6, vy + 38, vx + 58, vy + 46], fill=(20, 30, 40, 70))
    # Bàn nhựa tròn màu đỏ
    draw.ellipse([vx + 12, vy + 22, vx + 34, vy + 32], fill=(225, 45, 45, 255), outline=(160, 25, 25, 255))
    # Bình trà đá quai xách màu cam & Phích nước
    draw.rectangle([vx + 16, vy + 14, vx + 22, vy + 22], fill=(245, 125, 30, 255), outline=(180, 80, 15, 255))
    draw.rectangle([vx + 24, vy + 16, vx + 28, vy + 22], fill=(170, 220, 245, 255)) # Ly trà đá
    # 2 Ghế đẩu nhựa xanh lùn
    draw.rectangle([vx + 6, vy + 27, vx + 12, vy + 34], fill=(30, 120, 215, 255))
    draw.rectangle([vx + 34, vy + 27, vx + 40, vy + 34], fill=(30, 120, 215, 255))
    # Cô Năm ngồi ghế trò chuyện
    draw.ellipse([vx + 46, vy + 8, vx + 54, vy + 16], fill=(255, 210, 180, 255))
    draw.rectangle([vx + 45, vy + 16, vx + 55, vy + 28], fill=(175, 65, 135, 255)) # Áo bà ba tím
    draw.rectangle([vx + 46, vy + 29, vx + 54, vy + 36], fill=(30, 30, 35, 255))

    img.save(os.path.join(ASSETS_DIR, "street_vendors.png"))
    print("Created street_vendors.png successfully!")

if __name__ == "__main__":
    generate_cars()
    generate_beach_props()
    generate_street_vendors()
