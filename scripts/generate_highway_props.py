"""
Tạo sprite cho Đại Lộ Sông Hàn & Đường Ven Biển Đà Nẵng:
- Cột đèn đường đô thị
- Biển báo giao thông ("Đà Nẵng", "Cầu Rồng")
- Quán Cà phê vỉa hè (Bàn ghế nhựa, dù che)
- Cờ đỏ sao vàng trên cột
- Hàng dừa ven biển & Cây phượng vĩ hoa đỏ
- Lan can cầu & Trụ dây văng
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_highway_props():
    W, H = 256, 128
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Cột đèn đường hiện đại (32 x 64 at 0, 0)
    lx, ly = 0, 0
    draw.rectangle([lx + 14, ly + 14, lx + 17, ly + 62], fill=(130, 138, 145, 255))
    draw.arc([lx + 6, ly + 2, lx + 26, ly + 22], start=180, end=360, fill=(130, 138, 145, 255), width=2)
    draw.ellipse([lx + 4, ly + 10, lx + 12, ly + 16], fill=(255, 245, 170, 255), outline=(100, 105, 110, 255))

    # 2. Cột cờ Tổ Quốc (32 x 64 at 32, 0)
    fx, fy = 32, 0
    draw.line([fx + 10, fy + 4, fx + 10, fy + 62], fill=(210, 215, 220, 255), width=2)
    # Lá cờ đỏ sao vàng
    draw.rectangle([fx + 11, fy + 6, fx + 30, fy + 19], fill=(225, 30, 30, 255))
    # Ngôi sao vàng 5 cánh ở giữa
    draw.ellipse([fx + 18, fy + 10, fx + 23, fy + 15], fill=(255, 225, 40, 255))

    # 3. Biển báo chỉ dẫn giao thông (32 x 48 at 64, 0)
    sx, sy = 64, 0
    draw.line([sx + 15, sy + 18, sx + 15, sy + 46], fill=(160, 165, 170, 255), width=2)
    # Biển xanh chữ trắng
    draw.rectangle([sx + 4, sy + 4, sx + 28, sy + 20], fill=(25, 95, 175, 255), outline=(240, 240, 240, 255))
    # Mũi tên trắng chỉ đường
    draw.line([sx + 8, sy + 12, sx + 22, sy + 12], fill=(255, 255, 255, 255), width=2)
    draw.line([sx + 18, sy + 8, sx + 23, sy + 12], fill=(255, 255, 255, 255), width=2)
    draw.line([sx + 18, sy + 16, sx + 23, sy + 12], fill=(255, 255, 255, 255), width=2)

    # 4. Quán Cà phê Sữa Đá vỉa hè (64 x 48 at 96, 0)
    cx, cy = 96, 0
    # Dù che nắng sọc xanh trắng
    draw.polygon([(cx + 4, cy + 16), (cx + 32, cy + 4), (cx + 60, cy + 16)], fill=(30, 115, 195, 255))
    for px in [cx + 16, cx + 32, cx + 48]:
        draw.line([px, cy + 8, px, cy + 16], fill=(250, 250, 250, 255), width=2)
    draw.line([cx + 32, cy + 16, cx + 32, cy + 46], fill=(120, 125, 130, 255), width=2) # cán dù
    # Bàn nhựa tròn màu đỏ
    draw.ellipse([cx + 24, cy + 28, cx + 40, cy + 36], fill=(225, 45, 45, 255), outline=(180, 30, 30, 255))
    # Ly cà phê sữa đá
    draw.rectangle([cx + 30, cy + 26, cx + 34, cy + 32], fill=(135, 75, 40, 255), outline=(230, 240, 250, 255))
    # 2 ghế nhựa xanh hai bên
    draw.rectangle([cx + 16, cy + 30, cx + 23, cy + 38], fill=(30, 110, 210, 255))
    draw.rectangle([cx + 41, cy + 30, cx + 48, cy + 38], fill=(30, 110, 210, 255))

    # 5. Cây Dừa ven biển (64 x 96 at 160, 0)
    dx, dy = 160, 0
    # Thân dừa uốn lượn duyên dáng
    draw.arc([dx - 10, dy + 20, dx + 70, dy + 92], start=200, end=300, fill=(145, 105, 65, 255), width=7)
    # Tán dừa xanh xòe rộng
    for angle_x, angle_y in [(-24, -8), (24, -8), (-32, 10), (32, 10), (0, -20), (-16, 22), (16, 22)]:
        draw.line([dx + 38, dy + 25, dx + 38 + angle_x, dy + 25 + angle_y], fill=(55, 145, 50, 255), width=4)
        draw.line([dx + 38, dy + 25, dx + 38 + angle_x, dy + 25 + angle_y], fill=(85, 185, 75, 255), width=2)
    # Chùm dừa tròn
    draw.ellipse([dx + 34, dy + 24, dx + 42, dy + 32], fill=(165, 185, 80, 255))

    # 6. Lan can cầu Rồng & Trụ đèn (64 x 32 at 0, 64)
    bx, by = 0, 64
    draw.rectangle([bx, by + 12, bx + 63, by + 16], fill=(210, 175, 40, 255)) # Gờ vàng Cầu Rồng
    for x in range(bx + 4, bx + 64, 12):
        draw.line([x, by + 16, x, by + 30], fill=(240, 205, 60, 255), width=2)
    draw.rectangle([bx, by + 28, bx + 63, by + 31], fill=(180, 145, 30, 255))

    # 7. Xe Xích Lô truyền thống Đà Nẵng (64 x 48 at 64, 64)
    xx, xy = 64, 64
    # 2 bánh trước lớn
    draw.ellipse([xx + 8, xy + 20, xx + 22, xy + 34], outline=(40, 40, 40, 255), fill=(180, 185, 190, 255))
    draw.ellipse([xx + 42, xy + 24, xx + 54, xy + 36], outline=(40, 40, 40, 255), fill=(180, 185, 190, 255))
    # Ghế ngồi đệm bọc đỏ có mái che vòm
    draw.arc([xx + 4, xy + 8, xx + 28, xy + 24], start=180, end=360, fill=(30, 30, 30, 255), width=3)
    draw.rectangle([xx + 8, xy + 14, xx + 24, xy + 24], fill=(215, 45, 45, 255))
    # Khung sắt & Yên bác tài đạp sau
    draw.line([xx + 22, xy + 22, xx + 46, xy + 26], fill=(30, 30, 30, 255), width=2)
    draw.rectangle([xx + 40, xy + 17, xx + 46, xy + 20], fill=(110, 60, 30, 255))

    img.save(os.path.join(ASSETS_DIR, "highway_props.png"))
    print("Created highway_props.png successfully!")

if __name__ == "__main__":
    create_highway_props()
