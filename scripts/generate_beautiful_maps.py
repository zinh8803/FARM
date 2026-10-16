"""
Script vẽ sprite sheet pixel-art chi tiết cao cho 3 map đặc biệt:
  casino_props.png, school_props.png, racecourse_props.png
Kích thước 512x512 - gấp đôi chi tiết cũ, phong cách pixel art
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ============================================================
# CASINO PROPS (512 x 512)
# ============================================================
def generate_casino_props():
    W, H = 512, 512
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # -------- 1. Bàn Blackjack (160 x 108 at 0, 0) --------
    bx, by = 8, 8
    # Viền gỗ gụ sẫm (chân bàn)
    draw.rounded_rectangle([bx, by+8, bx+152, by+100], radius=40, fill=(60, 28, 14, 255), outline=(100, 55, 25, 255), width=3)
    # Mặt nỉ xanh ngọc emerald
    draw.rounded_rectangle([bx+10, by+14, bx+142, by+92], radius=34, fill=(12, 85, 52, 255))
    # Đường viền cược vàng bên trong
    draw.rounded_rectangle([bx+22, by+24, bx+130, by+82], radius=26, fill=None, outline=(220, 185, 65, 255), width=2)
    # Các ô cược (7 ô tròn vàng)
    for i, angle in enumerate(range(7)):
        cx = bx + 30 + i * 15
        cy = by + 72 - abs(i - 3) * 5
        draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=(230, 200, 70, 255), outline=(160, 120, 30, 255), width=1)
    # Quân bài
    for i, (px, py, c) in enumerate([(bx+60, by+30, (250,250,250)), (bx+72, by+28, (250,250,250)), (bx+84, by+32, (250,250,250))]):
        draw.rectangle([px, py, px+14, py+20], fill=c, outline=(180, 30, 30, 255) if i%2==0 else (20, 20, 20, 255), width=1)
    # Chip cược nhiều màu
    for cx, cy, col in [(bx+40, by+50, (220,40,40)), (bx+55, by+46, (40,100,220)), (bx+110, by+48, (240,200,50)), (bx+100, by+54, (30,30,30))]:
        draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=col, outline=(255,255,255,180), width=1)

    # -------- 2. Bàn Poker oval (176 x 108 at 168, 0) --------
    px, py = 172, 8
    draw.ellipse([px, py+4, px+168, py+96], fill=(50, 22, 12, 255), outline=(110, 58, 28, 255), width=4)
    draw.ellipse([px+14, py+14, px+154, py+86], fill=(140, 18, 30, 255))
    draw.ellipse([px+24, py+22, px+144, py+78], outline=(215, 175, 60, 255), width=2)
    # Chip poker ở giữa (pot)
    for cx, cy, col in [(px+72, py+44, (40,100,220)), (px+84, py+40, (220,40,40)), (px+80, py+48, (240,200,50)), (px+92, py+46, (20,150,60)), (px+76, py+36, (30,30,30))]:
        draw.ellipse([cx-5, cy-3, cx+5, cy+3], fill=col, outline=(255,255,255,140), width=1)
    # Vị trí 6 người chơi
    for i, angle_x in enumerate([px+24, px+56, px+88, px+120, px+144, px+40]):
        ay = py+78 if i < 3 else py+20
        draw.ellipse([angle_x-3, ay-3, angle_x+3, ay+3], fill=(200, 180, 60, 255))

    # -------- 3. Bàn Bi-da (160 x 96 at 348, 0) --------
    lx, ly = 352, 12
    draw.rectangle([lx, ly, lx+152, ly+88], fill=(55, 28, 14, 255), outline=(100, 58, 28, 255), width=4)
    draw.rectangle([lx+12, ly+12, lx+140, ly+76], fill=(18, 105, 68, 255))
    # 6 lỗ
    for hx, hy in [(lx+12, ly+12), (lx+76, ly+12), (lx+140, ly+12), (lx+12, ly+76), (lx+76, ly+76), (lx+140, ly+76)]:
        draw.ellipse([hx-5, hy-5, hx+5, hy+5], fill=(12, 12, 16, 255))
    # Bi cái trắng
    draw.ellipse([lx+40, ly+42, lx+48, ly+50], fill=(255, 255, 255, 255), outline=(200,200,200,255))
    # Tam giác bi màu
    bi_colors = [(220,40,40), (240,210,40), (30,70,180), (50,160,50), (200,80,30), (120,30,120)]
    for i, (bcx, bcy) in enumerate([(lx+96, ly+38), (lx+104, ly+34), (lx+104, ly+42), (lx+112, ly+30), (lx+112, ly+38), (lx+112, ly+46)]):
        draw.ellipse([bcx-4, bcy-4, bcx+4, bcy+4], fill=bi_colors[i], outline=(255,255,255,120))
    # Gậy cơ
    draw.line([lx+24, ly+82, lx+128, ly+82], fill=(210, 170, 100, 255), width=3)
    draw.line([lx+24, ly+82, lx+30, ly+82], fill=(240,220,160,255), width=3)

    # -------- 4. Máy Slot (80 x 128 at 0, 120) --------
    sx, sy = 12, 124
    # Thùng máy gradient tím đỏ
    draw.rectangle([sx, sy+8, sx+68, sy+120], fill=(40, 15, 50, 255), outline=(255, 210, 55, 255), width=3)
    # Mái vòm trên cùng
    draw.rounded_rectangle([sx-4, sy, sx+72, sy+24], radius=12, fill=(180, 20, 45, 255), outline=(255, 215, 60, 255), width=2)
    # JACKPOT text
    draw.text((sx+6, sy+6), "J A C K P O T", fill=(255, 240, 100, 255))
    # Ngôi sao trang trí
    draw.polygon([(sx+34, sy+2), (sx+36, sy+6), (sx+40, sy+6), (sx+37, sy+9), (sx+38, sy+13), (sx+34, sy+10), (sx+30, sy+13), (sx+31, sy+9), (sx+28, sy+6), (sx+32, sy+6)], fill=(255, 255, 200, 255))
    # Màn hình 3 cuộn
    draw.rectangle([sx+8, sy+30, sx+60, sy+70], fill=(235, 240, 245, 255), outline=(40, 20, 60, 255), width=2)
    # Chia 3 cuộn
    draw.line([sx+26, sy+30, sx+26, sy+70], fill=(150, 160, 175, 255), width=2)
    draw.line([sx+42, sy+30, sx+42, sy+70], fill=(150, 160, 175, 255), width=2)
    # Biểu tượng trên cuộn (cherry, 7, bar)
    draw.ellipse([sx+12, sy+44, sx+22, sy+54], fill=(220, 30, 30, 255))  # cherry
    draw.text((sx+29, sy+42), "7", fill=(255, 200, 40, 255))  # lucky 7
    draw.ellipse([sx+46, sy+44, sx+56, sy+54], fill=(50, 180, 70, 255))  # green gem
    # Cần gạt
    draw.line([sx+68, sy+60, sx+76, sy+40], fill=(180, 185, 195, 255), width=3)
    draw.ellipse([sx+72, sy+34, sx+82, sy+44], fill=(230, 30, 40, 255), outline=(180,20,30,255))
    # Khay xu
    draw.rounded_rectangle([sx+10, sy+90, sx+58, sy+112], radius=4, fill=(65, 70, 82, 255), outline=(210, 190, 70, 255), width=2)
    # Xu tràn
    for coin_x in range(sx+16, sx+54, 8):
        draw.ellipse([coin_x, sy+96, coin_x+6, sy+102], fill=(240, 210, 60, 255), outline=(180,150,30,255))

    # -------- 5. Đèn chùm pha lê (88 x 88 at 100, 120) --------
    dx, dy = 108, 120
    # Dây xích vàng
    draw.line([dx+40, dy+4, dx+40, dy+20], fill=(215, 175, 55, 255), width=3)
    # Tầng 1 (lớn)
    draw.ellipse([dx+8, dy+18, dx+72, dy+40], fill=(255, 225, 130, 255), outline=(215, 175, 50, 255), width=2)
    # Tầng 2 (trung)
    draw.ellipse([dx+16, dy+36, dx+64, dy+54], fill=(255, 235, 155, 255), outline=(225, 190, 55, 255), width=2)
    # Tầng 3 (nhỏ)
    draw.ellipse([dx+24, dy+50, dx+56, dy+64], fill=(255, 240, 175, 255), outline=(230, 195, 60, 255), width=2)
    # Giọt pha lê rủ
    for gx in range(dx+12, dx+70, 8):
        draw.line([gx, dy+40, gx, dy+72], fill=(255, 248, 205, 200), width=1)
        draw.ellipse([gx-2, dy+72, gx+2, dy+76], fill=(255, 255, 255, 255))
    # Ánh sáng tỏa ra
    draw.ellipse([dx+2, dy+14, dx+78, dy+68], outline=(255, 245, 200, 60), width=1)

    # -------- 6. Quầy Bar Cocktail (192 x 120 at 208, 120) --------
    rx, ry = 216, 120
    # Tủ rượu kính phía sau (tầng trên)
    draw.rectangle([rx+8, ry+4, rx+184, ry+56], fill=(22, 18, 28, 255), outline=(175, 135, 55, 255), width=3)
    # Kệ kính
    draw.line([rx+12, ry+30, rx+180, ry+30], fill=(200, 200, 210, 180), width=1)
    # Chai rượu nhiều loại
    bottle_colors = [(190,40,40), (40,160,70), (220,180,50), (60,100,200), (210,150,40), (180,30,120), (40,180,180), (220,100,40)]
    for i, col in enumerate(bottle_colors):
        ix = rx + 18 + i * 20
        # Thân chai
        draw.rectangle([ix, ry+14, ix+12, ry+44], fill=col, outline=(255,255,255,60))
        # Cổ chai
        draw.rectangle([ix+3, ry+6, ix+9, ry+14], fill=(*col[:3], 200))
        # Nắp
        draw.rectangle([ix+4, ry+4, ix+8, ry+7], fill=(200, 200, 210, 255))
    # Mặt quầy bar đá cẩm thạch
    draw.rectangle([rx, ry+56, rx+192, ry+86], fill=(32, 32, 38, 255), outline=(225, 185, 65, 255), width=3)
    # Vân đá marble trên mặt quầy
    draw.line([rx+20, ry+66, rx+60, ry+72], fill=(50, 50, 56, 255), width=1)
    draw.line([rx+100, ry+62, rx+160, ry+78], fill=(50, 50, 56, 255), width=1)
    # Ly cocktail trên quầy
    for lx_pos in [rx+30, rx+80, rx+130, rx+170]:
        draw.polygon([(lx_pos, ry+58), (lx_pos+4, ry+68), (lx_pos-4, ry+68)], fill=(255, 200, 220, 200))
        draw.line([lx_pos, ry+68, lx_pos, ry+74], fill=(200, 200, 210, 255), width=1)
        draw.line([lx_pos-4, ry+74, lx_pos+4, ry+74], fill=(200, 200, 210, 255), width=1)
    # Ghế bar
    for st_x in [rx+30, rx+70, rx+110, rx+150]:
        draw.ellipse([st_x-8, ry+86, st_x+8, ry+98], fill=(155, 28, 38, 255), outline=(235, 195, 65, 255), width=2)
        draw.line([st_x, ry+98, st_x, ry+112], fill=(175, 180, 192, 255), width=3)
        draw.line([st_x-6, ry+110, st_x+6, ry+110], fill=(175, 180, 192, 255), width=2)

    # -------- 7. Roulette Wheel (96 x 96 at 408, 120) --------
    wx, wy = 412, 124
    draw.ellipse([wx, wy, wx+92, wy+92], fill=(60, 28, 12, 255), outline=(220, 180, 55, 255), width=3)
    draw.ellipse([wx+8, wy+8, wx+84, wy+84], fill=(18, 55, 32, 255))
    # Vành số đen đỏ
    for i in range(18):
        angle_start = i * 20
        col = (200, 25, 25, 255) if i % 2 == 0 else (20, 20, 25, 255)
        draw.pieslice([wx+12, wy+12, wx+80, wy+80], angle_start, angle_start+20, fill=col)
    # Tâm vàng kim
    draw.ellipse([wx+32, wy+32, wx+60, wy+60], fill=(40, 80, 48, 255), outline=(200, 160, 40, 255), width=2)
    draw.ellipse([wx+38, wy+38, wx+54, wy+54], fill=(245, 215, 55, 255), outline=(180, 140, 30, 255))
    # Kim xoay
    draw.line([wx+46, wy+28, wx+46, wy+64], fill=(255, 245, 155, 255), width=2)
    draw.line([wx+28, wy+46, wx+64, wy+46], fill=(255, 245, 155, 255), width=2)

    # -------- 8. Sàn gạch ô vuông Casino (256 x 64 at 0, 260) cho trang trí sàn --------
    for row in range(4):
        for col in range(16):
            tx = col * 32
            ty = 264 + row * 16
            fill_c = (25, 15, 30, 255) if (row + col) % 2 == 0 else (50, 25, 55, 255)
            draw.rectangle([tx, ty, tx+32, ty+16], fill=fill_c)

    # -------- 9. Cây cọ trang trí Casino (48 x 96 at 0, 340) --------
    cx, cy = 16, 340
    # Chậu vàng
    draw.polygon([(cx+4, cy+70), (cx+36, cy+70), (cx+32, cy+92), (cx+8, cy+92)], fill=(200, 170, 50, 255), outline=(160, 130, 30, 255), width=2)
    # Thân
    draw.line([cx+20, cy+40, cx+20, cy+72], fill=(100, 65, 30, 255), width=4)
    # Lá cọ
    for angle_off, length in [((-16, -30), 1), ((16, -30), 1), ((-20, -20), 1), ((20, -20), 1), ((0, -35), 1)]:
        draw.line([cx+20, cy+40, cx+20+angle_off[0], cy+40+angle_off[1]], fill=(40, 150, 55, 255), width=3)
    draw.ellipse([cx+4, cy+16, cx+36, cy+46], fill=(50, 160, 60, 255))
    draw.ellipse([cx+8, cy+20, cx+32, cy+42], fill=(65, 180, 72, 255))

    # -------- 10. Dải đèn LED neon (256 x 20 at 0, 448) --------
    for i in range(32):
        nx = i * 16
        neon_col = [(255, 60, 120), (60, 200, 255), (255, 200, 60), (120, 255, 60)][i % 4]
        draw.ellipse([nx+4, 452, nx+12, 460], fill=neon_col, outline=(255,255,255,80))

    # -------- 11. Thảm đỏ sàn Casino viền vàng (512 x 32 at 0, 476) --------
    draw.rectangle([0, 478, 512, 510], fill=(140, 20, 35, 255), outline=(220, 180, 50, 255), width=2)
    # Hoa văn thảm
    for i in range(0, 512, 24):
        draw.rectangle([i+4, 484, i+20, 504], fill=(160, 30, 42, 255))
        draw.rectangle([i+8, 488, i+16, 500], fill=(180, 40, 52, 255))

    img.save(os.path.join(ASSETS_DIR, "casino_props.png"))
    print("[OK] Created casino_props.png (512x512)")


# ============================================================
# SCHOOL PROPS (512 x 512)
# ============================================================
def generate_school_props():
    W, H = 512, 512
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # -------- 1. Bàn học sinh đôi (96 x 72 at 0, 0) --------
    bx, by = 8, 8
    # Mặt bàn gỗ tự nhiên ấm áp
    draw.rectangle([bx, by+8, bx+88, by+42], fill=(210, 160, 98, 255), outline=(140, 90, 42, 255), width=3)
    # Sách vở trên bàn
    draw.rectangle([bx+10, by+14, bx+28, by+30], fill=(245, 245, 250, 255), outline=(40, 120, 200, 255), width=1)
    draw.rectangle([bx+50, by+15, bx+68, by+31], fill=(245, 245, 250, 255), outline=(210, 40, 40, 255), width=1)
    # Bút chì vàng
    draw.line([bx+34, by+16, bx+44, by+26], fill=(240, 195, 45, 255), width=3)
    draw.point((bx+44, by+26), fill=(30, 30, 30, 255))
    # Hộc bàn
    draw.rectangle([bx+2, by+42, bx+86, by+54], fill=(155, 110, 60, 255), outline=(120, 80, 40, 255))
    # Chân bàn sắt
    draw.line([bx+8, by+54, bx+8, by+66], fill=(60, 65, 75, 255), width=3)
    draw.line([bx+80, by+54, bx+80, by+66], fill=(60, 65, 75, 255), width=3)

    # -------- 2. Bàn Giáo Viên (124 x 84 at 112, 0) --------
    tx, ty = 118, 4
    draw.rectangle([tx, ty+8, tx+118, ty+52], fill=(170, 105, 50, 255), outline=(105, 55, 22, 255), width=3)
    # Khăn trải bàn đỏ
    draw.rectangle([tx+32, ty+12, tx+86, ty+48], fill=(215, 60, 60, 255), outline=(255, 255, 255, 200), width=1)
    # Giáo án, cốc bút, bảng tên
    draw.rectangle([tx+12, ty+14, tx+28, ty+34], fill=(250, 250, 250, 255), outline=(40, 100, 200, 255))
    draw.text((tx+15, ty+20), "10", fill=(210, 40, 40, 255))
    draw.rectangle([tx+90, ty+14, tx+106, ty+40], fill=(55, 135, 205, 255))
    draw.rectangle([tx+92, ty+10, tx+100, ty+14], fill=(55, 135, 205, 180))
    # Bút trong cốc
    draw.line([tx+94, ty+8, tx+96, ty+14], fill=(240, 50, 50, 255), width=1)
    draw.line([tx+96, ty+6, tx+98, ty+14], fill=(40, 40, 220, 255), width=1)
    # Chân bàn
    draw.rectangle([tx+4, ty+52, tx+114, ty+60], fill=(140, 85, 40, 255))
    draw.line([tx+10, ty+60, tx+10, ty+76], fill=(100, 60, 30, 255), width=4)
    draw.line([tx+108, ty+60, tx+108, ty+76], fill=(100, 60, 30, 255), width=4)

    # -------- 3. Bảng đen phấn trắng (180 x 80 at 248, 0) --------
    cx, cy = 254, 4
    # Khung gỗ bảng
    draw.rectangle([cx, cy, cx+172, cy+72], fill=(100, 55, 22, 255), outline=(75, 40, 15, 255), width=4)
    # Mặt bảng xanh đen
    draw.rectangle([cx+8, cy+8, cx+164, cy+64], fill=(8, 48, 32, 255))
    # Chữ phấn trắng
    draw.text((cx+20, cy+14), "TIÊN HỌC LỄ", fill=(240, 240, 235, 255))
    draw.text((cx+20, cy+28), "HẬU HỌC VĂN", fill=(240, 240, 235, 255))
    draw.text((cx+20, cy+46), "2 + 3 = 5", fill=(255, 255, 200, 255))
    # Hoa điểm 10
    draw.ellipse([cx+130, cy+14, cx+150, cy+34], fill=(220, 50, 50, 255))
    draw.text((cx+134, cy+18), "10", fill=(255, 255, 255, 255))
    # Máng phấn
    draw.rectangle([cx+4, cy+64, cx+168, cy+72], fill=(130, 75, 32, 255))
    # Phấn trắng trên máng
    draw.rectangle([cx+20, cy+66, cx+32, cy+70], fill=(255, 255, 255, 255))
    draw.rectangle([cx+36, cy+66, cx+44, cy+70], fill=(255, 240, 60, 255))

    # -------- 4. Trống trường học (88 x 100 at 440, 0) --------
    kx, ky = 444, 4
    # Giá đỡ gỗ X
    draw.line([kx+10, ky+52, kx+28, ky+94], fill=(115, 65, 30, 255), width=5)
    draw.line([kx+54, ky+52, kx+36, ky+94], fill=(115, 65, 30, 255), width=5)
    draw.line([kx+18, ky+88, kx+46, ky+88], fill=(135, 80, 40, 255), width=3)
    # Thùng trống
    draw.ellipse([kx+6, ky+18, kx+58, ky+58], fill=(190, 28, 28, 255), outline=(120, 12, 12, 255), width=3)
    # Mặt trống da trâu
    draw.ellipse([kx+8, ky+14, kx+56, ky+34], fill=(220, 200, 145, 255), outline=(145, 115, 55, 255), width=3)
    # Đinh tán vàng
    for dx in range(kx+14, kx+52, 5):
        draw.ellipse([dx-2, ky+35, dx+2, ky+39], fill=(240, 205, 55, 255))
    # Dùi trống
    draw.line([kx+52, ky+22, kx+68, ky+8], fill=(215, 175, 100, 255), width=3)
    draw.ellipse([kx+66, ky+4, kx+72, ky+10], fill=(180, 140, 70, 255))

    # -------- 5. Bản đồ Việt Nam (80 x 112 at 0, 100) --------
    vx, vy = 8, 104
    draw.rectangle([vx, vy, vx+72, vy+104], fill=(230, 240, 250, 255), outline=(115, 75, 35, 255), width=3)
    # Nẹp gỗ trên dưới
    draw.rectangle([vx-4, vy-2, vx+76, vy+4], fill=(135, 80, 40, 255))
    draw.rectangle([vx-4, vy+100, vx+76, vy+106], fill=(135, 80, 40, 255))
    # Dải đất hình chữ S
    s_points = [(vx+36, vy+14), (vx+44, vy+20), (vx+40, vy+28), (vx+34, vy+34), (vx+38, vy+42),
                (vx+42, vy+50), (vx+40, vy+58), (vx+36, vy+66), (vx+30, vy+74), (vx+26, vy+82),
                (vx+24, vy+88), (vx+28, vy+92)]
    for pt in s_points:
        draw.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill=(55, 155, 70, 255))
    # Hoàng Sa & Trường Sa (nổi bật)
    draw.ellipse([vx+52, vy+48, vx+58, vy+54], fill=(240, 115, 18, 255))
    draw.text((vx+48, vy+56), "HS", fill=(220, 100, 15, 255))
    draw.ellipse([vx+56, vy+72, vx+62, vy+78], fill=(240, 115, 18, 255))
    draw.text((vx+52, vy+80), "TS", fill=(220, 100, 15, 255))
    # Tiêu đề
    draw.text((vx+8, vy+8), "VIETNAM", fill=(210, 30, 30, 255))

    # -------- 6. Tủ sách thư viện (120 x 132 at 96, 100) --------
    sx, sy = 100, 100
    draw.rectangle([sx, sy, sx+112, sy+124], fill=(135, 80, 40, 255), outline=(75, 42, 18, 255), width=3)
    # 4 kệ sách
    for row in range(4):
        ry = sy + 8 + row * 28
        draw.line([sx+6, ry+24, sx+106, ry+24], fill=(180, 120, 70, 255), width=3)
        # Sách nhiều màu
        book_cols = [(220,50,50), (45,130,220), (50,180,90), (240,190,40), (160,60,200), (230,120,40), (40,180,180)]
        for b, b_col in enumerate(book_cols):
            bx_b = sx + 10 + b * 13
            h_var = [22, 20, 24, 18, 22, 20, 24][b]
            draw.rectangle([bx_b, ry+24-h_var, bx_b+9, ry+24], fill=b_col)
    # Cúp vàng trên nóc
    draw.polygon([(sx+46, sy-4), (sx+56, sy-4), (sx+54, sy+4), (sx+48, sy+4)], fill=(255, 215, 50, 255), outline=(200, 160, 30, 255))

    # -------- 7. Cây phượng vĩ sân trường (88 x 128 at 224, 100) --------
    px, py = 230, 100
    # Chậu xi măng
    draw.polygon([(px+14, py+96), (px+66, py+96), (px+60, py+122), (px+20, py+122)], fill=(155, 160, 172, 255), outline=(105, 110, 122, 255), width=2)
    # Đất
    draw.ellipse([px+18, py+94, px+62, py+102], fill=(130, 90, 50, 255))
    # Thân cây nâu
    draw.line([px+40, py+50, px+40, py+96], fill=(100, 60, 30, 255), width=6)
    draw.line([px+38, py+60, px+26, py+42], fill=(90, 55, 28, 255), width=4)
    draw.line([px+42, py+55, px+56, py+40], fill=(90, 55, 28, 255), width=4)
    # Tán lá xanh mát
    draw.ellipse([px+4, py+8, px+76, py+60], fill=(42, 135, 55, 255))
    draw.ellipse([px+10, py+12, px+70, py+52], fill=(58, 170, 68, 255))
    draw.ellipse([px+16, py+18, px+64, py+48], fill=(72, 185, 78, 255))
    # Hoa phượng đỏ
    for fx, fy in [(px+14, py+20), (px+30, py+14), (px+50, py+18), (px+60, py+28), (px+24, py+36), (px+46, py+40), (px+38, py+10)]:
        draw.ellipse([fx-4, fy-4, fx+4, fy+4], fill=(232, 42, 32, 255))
        draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=(255, 80, 60, 255))

    # -------- 8. Cột cờ Tổ Quốc (60 x 140 at 328, 100) --------
    fx, fy = 334, 100
    # Bệ cờ 3 cấp
    draw.rectangle([fx+8, fy+116, fx+48, fy+134], fill=(180, 50, 42, 255), outline=(125, 28, 22, 255), width=2)
    draw.rectangle([fx+14, fy+108, fx+42, fy+118], fill=(205, 70, 60, 255))
    draw.rectangle([fx+18, fy+102, fx+38, fy+110], fill=(220, 85, 72, 255))
    # Cột cờ inox
    draw.line([fx+28, fy+8, fx+28, fy+102], fill=(230, 235, 242, 255), width=3)
    draw.ellipse([fx+24, fy+4, fx+32, fy+12], fill=(255, 218, 58, 255))
    # Lá cờ đỏ sao vàng tung bay
    draw.polygon([(fx+28, fy+14), (fx+60, fy+20), (fx+58, fy+42), (fx+28, fy+38)], fill=(222, 28, 32, 255))
    # Sao vàng 5 cánh
    star_cx, star_cy = fx+44, fy+28
    draw.polygon([
        (star_cx, star_cy-6), (star_cx+2, star_cy-2), (star_cx+6, star_cy-1),
        (star_cx+3, star_cy+2), (star_cx+4, star_cy+6), (star_cx, star_cy+4),
        (star_cx-4, star_cy+6), (star_cx-3, star_cy+2), (star_cx-6, star_cy-1),
        (star_cx-2, star_cy-2)
    ], fill=(255, 230, 55, 255))

    # -------- 9. Bàn ghế ngoài sân trường (96 x 64 at 408, 100) --------
    ox, oy = 414, 108
    # Ghế đá dài sân trường
    draw.rounded_rectangle([ox, oy+24, ox+88, oy+38], radius=4, fill=(180, 185, 195, 255), outline=(130, 135, 145, 255), width=2)
    # Chân ghế
    draw.rectangle([ox+8, oy+38, ox+14, oy+54], fill=(140, 145, 155, 255))
    draw.rectangle([ox+74, oy+38, ox+80, oy+54], fill=(140, 145, 155, 255))
    # Cây xanh nhỏ bên cạnh
    draw.ellipse([ox+68, oy, ox+92, oy+24], fill=(55, 150, 65, 255))
    draw.line([ox+80, oy+20, ox+80, oy+38], fill=(95, 60, 30, 255), width=3)

    # -------- 10. Sàn gạch bông vintage trường học (512 x 40 at 0, 256) --------
    for row in range(2):
        for col in range(32):
            tx = col * 16
            ty = 260 + row * 20
            c1 = (225, 218, 195, 255) if (row+col)%2==0 else (205, 195, 170, 255)
            draw.rectangle([tx, ty, tx+16, ty+20], fill=c1)

    img.save(os.path.join(ASSETS_DIR, "school_props.png"))
    print("[OK] Created school_props.png (512x512)")


# ============================================================
# RACECOURSE PROPS (512 x 512)
# ============================================================
def generate_racecourse_props():
    W, H = 512, 512
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # -------- 1. Khán đài hoàng gia (192 x 120 at 0, 0) --------
    gx, gy = 8, 8
    # Mái vòm bạt trắng sọc đỏ
    draw.rounded_rectangle([gx, gy, gx+184, gy+40], radius=20, fill=(242, 242, 248, 255), outline=(210, 42, 42, 255), width=3)
    # Sọc đỏ trắng
    for sx_pos in range(gx+20, gx+170, 20):
        draw.rectangle([sx_pos, gy+8, sx_pos+8, gy+32], fill=(220, 38, 38, 255))
    # Cột thép đỡ
    draw.rectangle([gx+6, gy+36, gx+12, gy+110], fill=(155, 165, 180, 255), outline=(100, 110, 125, 255))
    draw.rectangle([gx+172, gy+36, gx+178, gy+110], fill=(155, 165, 180, 255), outline=(100, 110, 125, 255))
    # 3 hàng ghế khán giả màu sắc
    draw.rectangle([gx+18, gy+42, gx+166, gy+58], fill=(55, 115, 215, 255))  # xanh dương
    draw.rectangle([gx+14, gy+62, gx+170, gy+78], fill=(220, 55, 55, 255))   # đỏ
    draw.rectangle([gx+10, gy+82, gx+174, gy+98], fill=(240, 190, 42, 255))   # vàng
    # Khán giả chấm pixel
    for row_y in [gy+48, gy+68, gy+88]:
        for kx in range(gx+24, gx+164, 14):
            skin = [(240,200,160), (220,180,140), (200,160,120)][kx % 3]
            draw.ellipse([kx-3, row_y-3, kx+3, row_y+3], fill=skin)

    # -------- 2. Cổng FINISH cờ ca-rô (160 x 120 at 208, 0) --------
    fx, fy = 214, 8
    # Cột thép 2 bên
    draw.rectangle([fx+6, fy+28, fx+16, fy+112], fill=(205, 210, 222, 255), outline=(55, 65, 80, 255), width=2)
    draw.rectangle([fx+136, fy+28, fx+146, fy+112], fill=(205, 210, 222, 255), outline=(55, 65, 80, 255), width=2)
    # Băng rôn FINISH
    draw.rectangle([fx, fy+4, fx+152, fy+32], fill=(18, 22, 32, 255), outline=(255, 215, 55, 255), width=2)
    # Ô ca-rô đen trắng
    for r in range(2):
        for c in range(19):
            cx_c = fx + 4 + c * 8
            cy_c = fy + 8 + r * 8
            col = (255, 255, 255, 255) if (r+c)%2==0 else (20, 20, 25, 255)
            draw.rectangle([cx_c, cy_c, cx_c+8, cy_c+8], fill=col)
    draw.text((fx+40, fy+10), "F I N I S H", fill=(255, 220, 40, 255))

    # -------- 3. Hàng rào trắng hoàng gia (128 x 64 at 376, 0) --------
    rx, ry = 382, 16
    for px_pos in [rx+4, rx+28, rx+52, rx+76, rx+100, rx+120]:
        draw.rectangle([px_pos, ry+4, px_pos+6, ry+48], fill=(242, 248, 255, 255), outline=(175, 185, 200, 255), width=1)
        draw.ellipse([px_pos-2, ry, px_pos+8, ry+8], fill=(255, 255, 255, 255))
    draw.line([rx, ry+12, rx+126, ry+12], fill=(255, 255, 255, 255), width=3)
    draw.line([rx, ry+28, rx+126, ry+28], fill=(255, 255, 255, 255), width=3)
    draw.line([rx, ry+42, rx+126, ry+42], fill=(245, 245, 255, 255), width=2)

    # -------- 4. Đài phun nước trung tâm (128 x 100 at 0, 140) --------
    wx, wy = 8, 144
    # Bể nước tròn ốp đá xanh
    draw.ellipse([wx, wy+32, wx+120, wy+90], fill=(28, 125, 175, 255), outline=(180, 210, 232, 255), width=4)
    draw.ellipse([wx+10, wy+38, wx+110, wy+84], fill=(55, 170, 220, 255))
    # Sóng nước
    for wave_x in range(wx+18, wx+104, 12):
        draw.arc([wave_x, wy+56, wave_x+12, wy+66], 0, 180, fill=(120, 210, 250, 255), width=1)
    # Trụ phun nước
    draw.rectangle([wx+50, wy+20, wx+70, wy+50], fill=(200, 215, 232, 255), outline=(125, 155, 185, 255), width=2)
    draw.line([wx+60, wy+4, wx+60, wy+24], fill=(255, 255, 255, 255), width=3)
    # Tia nước xòe
    draw.arc([wx+30, wy+2, wx+90, wy+40], 180, 360, fill=(225, 242, 255, 255), width=3)
    draw.arc([wx+38, wy+8, wx+82, wy+36], 180, 360, fill=(240, 250, 255, 255), width=2)

    # -------- 5. Bảng LED tỉ lệ cược (144 x 100 at 140, 140) --------
    ox, oy = 148, 144
    draw.rectangle([ox, oy, ox+136, oy+88], fill=(12, 15, 22, 255), outline=(225, 185, 48, 255), width=3)
    # Tiêu đề
    draw.rectangle([ox+6, oy+4, ox+130, oy+18], fill=(30, 35, 48, 255))
    draw.text((ox+14, oy+6), "BẢNG CƯỢC ĐUA NGỰA", fill=(255, 220, 55, 255))
    # Dòng header
    draw.text((ox+10, oy+22), "SỐ  TÊN       TỈ LỆ", fill=(180, 220, 255, 255))
    # 4 dòng ngựa
    horses = [("1", "Sấm", (240,60,60), "1:2.5"), ("2", "Gió", (60,140,240), "1:3.0"), ("3", "Mây", (250,210,40), "1:4.2"), ("4", "Bão", (240,120,40), "1:5.0")]
    for idx, (num, name, col, odds) in enumerate(horses):
        ry = oy + 34 + idx * 13
        draw.rectangle([ox+8, ry, ox+16, ry+8], fill=col)
        draw.text((ox+20, ry-1), f"{num}  {name}", fill=(222, 228, 238, 255))
        draw.text((ox+90, ry-1), odds, fill=(75, 235, 115, 255))

    # -------- 6. Cúp vàng vô địch (72 x 96 at 296, 140) --------
    tx, ty = 304, 144
    # Bệ gỗ
    draw.rectangle([tx+10, ty+70, tx+52, ty+90], fill=(65, 32, 12, 255), outline=(175, 115, 48, 255), width=2)
    draw.rectangle([tx+16, ty+64, tx+46, ty+72], fill=(85, 45, 18, 255))
    # Chân cúp
    draw.polygon([(tx+22, ty+64), (tx+40, ty+64), (tx+36, ty+50), (tx+26, ty+50)], fill=(238, 188, 38, 255))
    # Thân cúp hình búp sen
    draw.ellipse([tx+14, ty+16, tx+48, ty+50], fill=(252, 218, 55, 255), outline=(195, 148, 18, 255), width=2)
    # Quai cúp 2 bên
    draw.arc([tx+4, ty+18, tx+22, ty+38], 90, 270, fill=(242, 192, 42, 255), width=3)
    draw.arc([tx+40, ty+18, tx+58, ty+38], 270, 90, fill=(242, 192, 42, 255), width=3)
    # Ngôi sao trên cúp
    draw.polygon([(tx+31, ty+22), (tx+33, ty+28), (tx+38, ty+29), (tx+34, ty+33), (tx+36, ty+38), (tx+31, ty+35), (tx+26, ty+38), (tx+28, ty+33), (tx+24, ty+29), (tx+29, ty+28)], fill=(255, 255, 200, 255))
    # Số 1 vô địch
    draw.text((tx+28, ty+4), "1", fill=(255, 215, 55, 255))

    # -------- 7. Tháp quan sát trọng tài (64 x 128 at 388, 140) --------
    tw_x, tw_y = 396, 140
    # Thân tháp
    draw.rectangle([tw_x+12, tw_y+32, tw_x+48, tw_y+120], fill=(200, 205, 215, 255), outline=(140, 148, 160, 255), width=2)
    # Phòng quan sát trên cùng
    draw.rectangle([tw_x+4, tw_y+8, tw_x+56, tw_y+36], fill=(180, 188, 200, 255), outline=(110, 118, 130, 255), width=2)
    # Cửa kính
    draw.rectangle([tw_x+10, tw_y+12, tw_x+50, tw_y+30], fill=(130, 195, 240, 255), outline=(80, 140, 180, 255))
    # Mái nhọn
    draw.polygon([(tw_x+30, tw_y), (tw_x+4, tw_y+10), (tw_x+56, tw_y+10)], fill=(180, 45, 40, 255))
    # Cờ hiệu trên đỉnh
    draw.line([tw_x+30, tw_y-8, tw_x+30, tw_y+2], fill=(160, 165, 175, 255), width=2)
    draw.polygon([(tw_x+30, tw_y-8), (tw_x+42, tw_y-4), (tw_x+30, tw_y)], fill=(255, 215, 55, 255))
    # Cửa ra vào dưới
    draw.rectangle([tw_x+22, tw_y+96, tw_x+38, tw_y+120], fill=(120, 70, 35, 255), outline=(80, 45, 20, 255))

    # -------- 8. Starting Gate (128 x 80 at 0, 260) --------
    sg_x, sg_y = 8, 264
    # Khung sắt chính
    draw.rectangle([sg_x, sg_y, sg_x+120, sg_y+12], fill=(200, 205, 215, 255), outline=(140, 148, 160, 255), width=2)
    # 4 ngăn cho 4 ngựa
    for i in range(4):
        gx = sg_x + 4 + i * 30
        draw.rectangle([gx, sg_y+12, gx+26, sg_y+68], fill=(225, 230, 240, 255), outline=(160, 168, 180, 255), width=2)
        # Số ngăn
        draw.text((gx+10, sg_y+16), str(i+1), fill=(40, 40, 50, 255))
        # Cửa mở
        draw.rectangle([gx+2, sg_y+30, gx+24, sg_y+66], fill=(245, 248, 255, 255), outline=(180, 188, 200, 255))
    # Biển START
    draw.rectangle([sg_x+30, sg_y-8, sg_x+90, sg_y+2], fill=(40, 160, 55, 255))
    draw.text((sg_x+40, sg_y-6), "START", fill=(255, 255, 255, 255))

    # -------- 9. Cỏ xanh trang trí (256 x 32 at 0, 360) --------
    for gx_pos in range(0, 256, 4):
        h = 16 + (gx_pos * 7) % 12
        g_col = (40 + (gx_pos*3)%30, 145 + (gx_pos*5)%40, 50 + (gx_pos*2)%20, 255)
        draw.line([gx_pos*2, 390, gx_pos*2, 390-h], fill=g_col, width=2)

    # -------- 10. Hoa trang trí sân cỏ (128 x 32 at 0, 400) --------
    flower_colors = [(255,100,100), (255,200,100), (200,100,255), (100,200,255), (255,150,200)]
    for i, (fx, fy) in enumerate([(20, 410), (60, 415), (100, 408), (140, 418), (180, 412), (220, 416)]):
        col = flower_colors[i % len(flower_colors)]
        draw.ellipse([fx-6, fy-6, fx+6, fy+6], fill=col)
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=(255, 255, 200, 255))
        draw.line([fx, fy+6, fx, fy+18], fill=(50, 140, 50, 255), width=2)

    img.save(os.path.join(ASSETS_DIR, "racecourse_props.png"))
    print("[OK] Created racecourse_props.png (512x512)")


if __name__ == "__main__":
    generate_casino_props()
    generate_school_props()
    generate_racecourse_props()
    print("\n✅ Đã tạo xong tất cả sprite sheet mới (512x512)!")
