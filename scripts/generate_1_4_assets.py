"""
Script tạo đầy đủ tài nguyên cho bản 1.4:
1. player_outfits.png: Trang phục nhân vật (Áo bà ba vàng, xanh, nâu, áo dài, khăn rằn, nón lá)
2. rural_decorations.png: Bù nhìn rơm, chậu hoa cúc Tết, hàng rào tre, giàn mướp/bầu, bàn ghế cẩm thạch, quạt trần, tivi cổ, sập gỗ
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_player_outfits():
    # 4 outfit styles, each has 4 directions (down, up, left, right) x 3 frames (idle, walk1, walk2)
    # Total width: 3 frames * 32 = 96
    # Total height: 4 directions * 32 * 4 styles = 512
    # Style 0: Áo bà ba vàng + nón lá (Mặc định)
    # Style 1: Áo bà ba xanh lá sen + nón lá
    # Style 2: Áo bà ba nâu đất + khăn rằn Nam Bộ
    # Style 3: Áo dài truyền thống gấm đỏ du xuân
    
    W = 96
    H = 512
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    outfits = [
        {"name": "baba_yellow", "shirt_main": (243, 187, 68), "shirt_hi": (250, 205, 95), "pants": (75, 55, 40), "hat": "nonla", "scarf": False},
        {"name": "baba_green",  "shirt_main": (60, 155, 90),  "shirt_hi": (85, 180, 115), "pants": (50, 45, 40), "hat": "nonla", "scarf": False},
        {"name": "baba_brown",  "shirt_main": (120, 75, 45),  "shirt_hi": (145, 95, 60),  "pants": (40, 35, 30), "hat": "none",  "scarf": True},
        {"name": "aodai_red",   "shirt_main": (200, 35, 40),  "shirt_hi": (225, 60, 65),  "pants": (245, 240, 230), "hat": "khan_dong", "scarf": False}
    ]
    
    for s_idx, outfit in enumerate(outfits):
        base_s_y = s_idx * 128
        for row, direction in enumerate(["down", "up", "left", "right"]):
            for col, step in enumerate([0, 1, 2]):
                fx = col * 32
                fy = base_s_y + row * 32
                leg_offset = 0 if step == 0 else (-2 if step == 1 else 2)
                
                # Quần / Chân
                p_col = outfit["pants"]
                if direction in ["down", "up"]:
                    draw.rectangle([fx + 11, fy + 22, fx + 14, fy + 29 + (1 if step == 1 else 0)], fill=p_col)
                    draw.rectangle([fx + 17, fy + 22, fx + 20, fy + 29 + (1 if step == 2 else 0)], fill=p_col)
                    draw.rectangle([fx + 11, fy + 29, fx + 14, fy + 31], fill=(240, 210, 170, 255))
                    draw.rectangle([fx + 17, fy + 29, fx + 20, fy + 31], fill=(240, 210, 170, 255))
                else:
                    draw.rectangle([fx + 13 + leg_offset, fy + 22, fx + 18 - leg_offset, fy + 30], fill=p_col)
                    draw.rectangle([fx + 13 + leg_offset, fy + 29, fx + 18 - leg_offset, fy + 31], fill=(240, 210, 170, 255))
                
                # Thân áo
                s_main = outfit["shirt_main"]
                s_hi = outfit["shirt_hi"]
                if outfit["name"] == "aodai_red":
                    # Tà áo dài thướt tha xuống qua gối
                    draw.rectangle([fx + 11, fy + 14, fx + 20, fy + 26], fill=s_main)
                    draw.rectangle([fx + 12, fy + 15, fx + 19, fy + 25], fill=s_hi)
                    # Họa tiết hoa mai vàng trước ngực
                    if direction == "down":
                        draw.point((fx + 15, fy + 17), fill=(255, 220, 60))
                        draw.point((fx + 16, fy + 18), fill=(255, 240, 100))
                else:
                    # Áo bà ba
                    draw.rectangle([fx + 11, fy + 14, fx + 20, fy + 23], fill=s_main)
                    draw.rectangle([fx + 12, fy + 15, fx + 19, fy + 22], fill=s_hi)
                    if direction == "down":
                        for by in [fy + 16, fy + 18, fy + 20]:
                            draw.point((fx + 15, by), fill=(40, 30, 20, 255))
                
                # Tay áo
                if direction == "down":
                    draw.rectangle([fx + 8, fy + 15, fx + 10, fy + 22], fill=(240, 210, 170, 255))
                    draw.rectangle([fx + 21, fy + 15, fx + 23, fy + 22], fill=(240, 210, 170, 255))
                elif direction == "left":
                    draw.rectangle([fx + 10, fy + 15, fx + 13, fy + 22], fill=(240, 210, 170, 255))
                elif direction == "right":
                    draw.rectangle([fx + 18, fy + 15, fx + 21, fy + 22], fill=(240, 210, 170, 255))
                
                # Khăn rằn Nam Bộ (kẻ caro đen trắng vắt chéo cổ)
                if outfit["scarf"]:
                    if direction in ["down", "left", "right"]:
                        draw.rectangle([fx + 11, fy + 13, fx + 20, fy + 16], fill=(230, 230, 230, 255))
                        for sx in range(fx + 11, fx + 20, 2):
                            draw.point((sx, fy + 14), fill=(30, 30, 30, 255))
                        # Vạt khăn rủ xuống ngực
                        if direction == "down":
                            draw.rectangle([fx + 13, fy + 16, fx + 15, fy + 22], fill=(230, 230, 230, 255))
                            draw.point((fx + 14, fy + 18), fill=(30, 30, 30, 255))
                            draw.point((fx + 14, fy + 21), fill=(30, 30, 30, 255))
                
                # Đầu & Mặt
                draw.rectangle([fx + 12, fy + 8, fx + 19, fy + 14], fill=(252, 212, 169, 255))
                if direction == "down":
                    draw.point((fx + 14, fy + 11), fill=(40, 30, 20, 255))
                    draw.point((fx + 17, fy + 11), fill=(40, 30, 20, 255))
                    draw.point((fx + 15, fy + 13), fill=(210, 110, 90, 255))
                    draw.point((fx + 16, fy + 13), fill=(210, 110, 90, 255))
                elif direction == "left":
                    draw.point((fx + 13, fy + 11), fill=(40, 30, 20, 255))
                elif direction == "right":
                    draw.point((fx + 18, fy + 11), fill=(40, 30, 20, 255))
                elif direction == "up":
                    # Tóc đen sau gáy
                    draw.rectangle([fx + 12, fy + 8, fx + 19, fy + 13], fill=(30, 25, 20, 255))
                
                # Mũ / Nón / Khăn đóng
                if outfit["hat"] == "nonla":
                    draw.polygon([(fx + 15, fy + 1), (fx + 26, fy + 9), (fx + 5, fy + 9)], fill=(222, 209, 150, 255))
                    draw.line([fx + 8, fy + 7, fx + 23, fy + 7], fill=(195, 180, 120, 255), width=1)
                    draw.line([fx + 11, fy + 5, fx + 20, fy + 5], fill=(195, 180, 120, 255), width=1)
                    draw.point((fx + 15, fy + 1), fill=(170, 150, 90, 255))
                    if direction == "down":
                        draw.line([fx + 10, fy + 9, fx + 14, fy + 14], fill=(200, 60, 60, 255), width=1)
                        draw.line([fx + 21, fy + 9, fx + 17, fy + 14], fill=(200, 60, 60, 255), width=1)
                elif outfit["hat"] == "khan_dong":
                    # Khăn đóng gấm vàng truyền thống
                    draw.rectangle([fx + 11, fy + 6, fx + 20, fy + 10], fill=(240, 190, 50, 255), outline=(180, 130, 30, 255))
                    draw.line([fx + 12, fy + 8, fx + 19, fy + 8], fill=(255, 230, 100, 255))
                elif outfit["hat"] == "none":
                    # Tóc chải mộc nông dân
                    draw.rectangle([fx + 12, fy + 6, fx + 19, fy + 9], fill=(35, 30, 25, 255))
    
    out_path = os.path.join(ASSETS_DIR, "player_outfits.png")
    img.save(out_path)
    print("Created player_outfits.png successfully!")

def generate_rural_decorations():
    # 256 x 256 atlas chứa các đồ nội thất và ngoại thất bản 1.4:
    # 1. Bù nhìn rơm (Scarecrow) (48 x 56 at 0, 0)
    # 2. Chậu cúc mâm xôi Tết vàng rực (32 x 36 at 48, 0)
    # 3. Hàng rào tre Việt Nam (64 x 32 at 80, 0)
    # 4. Giàn bầu / mướp trĩu quả (64 x 64 at 144, 0)
    # 5. Bộ bàn ghế cẩm thạch xưa (64 x 50 at 0, 64)
    # 6. Sập gỗ lim / Phản nằm (64 x 40 at 64, 64)
    # 7. Tivi đen trắng cổ điển có ăng-ten râu (32 x 36 at 128, 64)
    # 8. Quạt trần cổ 3 cánh quay (48 x 48 at 160, 64)
    
    W = 256
    H = 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Bù nhìn rơm đuổi chim (Scarecrow) at (0, 0)
    ox, oy = 8, 4
    # Cọc gỗ chữ thập
    draw.line([ox + 16, oy + 8, ox + 16, oy + 48], fill=(110, 70, 35, 255), width=3)
    draw.line([ox + 2, oy + 18, ox + 30, oy + 18], fill=(110, 70, 35, 255), width=2)
    # Áo bà ba cũ rách bọc rơm
    draw.polygon([(ox + 8, oy + 16), (ox + 24, oy + 16), (ox + 22, oy + 36), (ox + 10, oy + 36)], fill=(185, 120, 50, 255))
    # Rơm thò ra ở tay và chân
    for rx, ry in [(ox + 4, oy + 18), (ox + 28, oy + 18), (ox + 12, oy + 38), (ox + 18, oy + 38)]:
        draw.line([rx, ry, rx - 3, ry + 4], fill=(240, 210, 90, 255), width=2)
        draw.line([rx, ry, rx + 3, ry + 5], fill=(240, 210, 90, 255), width=2)
    # Đầu bí ngô / bao bố đội nón lá nhỏ
    draw.ellipse([ox + 11, oy + 6, ox + 21, oy + 15], fill=(220, 190, 140, 255))
    draw.point((ox + 14, oy + 10), fill=(40, 30, 20, 255))
    draw.point((ox + 18, oy + 10), fill=(40, 30, 20, 255))
    draw.polygon([(ox + 16, oy + 1), (ox + 25, oy + 7), (ox + 7, oy + 7)], fill=(225, 200, 120, 255)) # nón lá
    
    # 2. Chậu cúc mâm xôi Tết vàng rực at (48, 4)
    cx, cy = 52, 6
    # Chậu đất nung đỏ cam
    draw.polygon([(cx + 4, cy + 18), (cx + 24, cy + 18), (cx + 20, cy + 30), (cx + 8, cy + 30)], fill=(195, 75, 45, 255))
    draw.rectangle([cx + 2, cy + 16, cx + 26, cy + 18], fill=(220, 95, 60, 255)) # vành chậu
    # Mâm hoa cúc vàng hình cầu nở tròn rực rỡ
    draw.ellipse([cx + 2, cy + 2, cx + 26, cy + 18], fill=(240, 185, 30, 255))
    for hx in range(cx + 4, cx + 25, 3):
        for hy in range(cy + 4, cy + 17, 3):
            draw.point((hx, hy), fill=(255, 230, 70, 255))
            draw.point((hx + 1, hy), fill=(210, 150, 10, 255))
    
    # 3. Hàng rào tre Việt Nam at (84, 8)
    rx, ry = 84, 8
    for fx in range(rx, rx + 56, 10):
        draw.line([fx, ry + 2, fx, ry + 26], fill=(130, 175, 80, 255), width=3) # thân tre
        draw.line([fx - 1, ry + 8, fx + 2, ry + 8], fill=(200, 220, 130, 255), width=2) # đốt
        draw.line([fx - 1, ry + 18, fx + 2, ry + 18], fill=(200, 220, 130, 255), width=2)
    # Hai thanh ngang giằng rào
    draw.line([rx - 2, ry + 8, rx + 58, ry + 8], fill=(100, 145, 65, 255), width=2)
    draw.line([rx - 2, ry + 20, rx + 58, ry + 20], fill=(100, 145, 65, 255), width=2)
    
    # 4. Giàn bầu / mướp ngõ vào at (150, 0)
    gx, gy = 150, 4
    # Cọc tre 4 góc
    draw.line([gx + 6, gy + 12, gx + 6, gy + 56], fill=(120, 80, 40, 255), width=3)
    draw.line([gx + 54, gy + 12, gx + 54, gy + 56], fill=(120, 80, 40, 255), width=3)
    # Lưới giàn ngang trên nóc
    for ly in range(gy + 6, gy + 22, 5):
        draw.line([gx + 2, ly, gx + 58, ly], fill=(150, 105, 55, 255), width=1)
    for lx in range(gx + 6, gx + 56, 7):
        draw.line([lx, gy + 4, lx, gy + 22], fill=(150, 105, 55, 255), width=1)
    # Lá mướp xanh xum xuê
    for lx in range(gx + 8, gx + 52, 6):
        draw.ellipse([lx, gy + 4, lx + 9, gy + 16], fill=(55, 130, 60, 230))
        draw.ellipse([lx + 2, gy + 6, lx + 7, gy + 14], fill=(85, 175, 80, 255))
    # Quả mướp / bầu dài lòng thòng đung đưa
    for bx, by, blen in [(gx + 16, gy + 16, 18), (gx + 32, gy + 18, 22), (gx + 44, gy + 15, 16)]:
        draw.line([bx, by, bx, by + blen], fill=(110, 180, 70, 255), width=3)
        draw.point((bx, by + blen + 1), fill=(255, 230, 50, 255)) # hoa vàng nhỏ ở chóp quả
    
    # 5. Bộ bàn ghế cẩm thạch xưa at (0, 68)
    tx, ty = 4, 70
    # Bàn tròn mặt đá cẩm thạch hoa văn xanh ngọc
    draw.ellipse([tx + 12, ty + 10, tx + 44, ty + 32], fill=(205, 225, 220, 255), outline=(130, 155, 150, 255))
    draw.ellipse([tx + 15, ty + 12, tx + 41, ty + 30], fill=(230, 245, 240, 255))
    # Vân đá cẩm thạch
    draw.line([tx + 20, ty + 18, tx + 34, ty + 24], fill=(160, 190, 180, 255), width=1)
    draw.line([tx + 24, ty + 15, tx + 36, ty + 20], fill=(175, 205, 195, 255), width=1)
    # Chân bàn trụ gỗ lim
    draw.rectangle([tx + 25, ty + 28, tx + 31, ty + 42], fill=(90, 50, 25, 255))
    # 2 đôn ghế đá 2 bên
    draw.ellipse([tx + 2, ty + 18, tx + 12, ty + 26], fill=(205, 225, 220, 255), outline=(100, 65, 35, 255))
    draw.ellipse([tx + 44, ty + 18, tx + 54, ty + 26], fill=(205, 225, 220, 255), outline=(100, 65, 35, 255))
    
    # 6. Sập gỗ lim / Phản nằm sang trọng at (68, 70)
    sx, sy = 68, 70
    # Mặt sập bóng loáng màu nâu cánh gián
    draw.polygon([(sx + 10, sy + 6), (sx + 54, sy + 6), (sx + 58, sy + 28), (sx + 4, sy + 28)], fill=(135, 75, 35, 255))
    draw.polygon([(sx + 12, sy + 8), (sx + 52, sy + 8), (sx + 55, sy + 26), (sx + 7, sy + 26)], fill=(160, 90, 45, 255))
    # Dạ sập chạm trổ & 4 chân quỳ vững chãi
    draw.rectangle([sx + 4, sy + 28, sx + 58, sy + 34], fill=(105, 55, 25, 255))
    draw.rectangle([sx + 5, sy + 34, sx + 12, sy + 40], fill=(75, 40, 20, 255))
    draw.rectangle([sx + 50, sy + 34, sx + 57, sy + 40], fill=(75, 40, 20, 255))
    # Chiếu cói hoa dệt trải giữa sập
    draw.polygon([(sx + 18, sy + 10), (sx + 46, sy + 10), (sx + 48, sy + 24), (sx + 16, sy + 24)], fill=(225, 205, 150, 255), outline=(190, 50, 50, 255))
    
    # 7. Tivi đen trắng cổ điển at (132, 70)
    vx, vy = 132, 70
    # Ăng-ten râu chữ V
    draw.line([vx + 14, vy + 4, vx + 6, vy - 4], fill=(180, 180, 180, 255), width=1)
    draw.line([vx + 16, vy + 4, vx + 24, vy - 4], fill=(180, 180, 180, 255), width=1)
    # Thùng tivi vỏ gỗ
    draw.rectangle([vx + 2, vy + 4, vx + 28, vy + 28], fill=(125, 70, 35, 255), outline=(65, 35, 18, 255))
    # Màn hình cong lồi phát xạ
    draw.rectangle([vx + 5, vy + 7, vx + 21, vy + 23], fill=(45, 55, 60, 255), outline=(90, 105, 110, 255))
    # Núm xoay đài kênh & loa nan gỗ
    draw.ellipse([vx + 23, vy + 9, vx + 26, vy + 12], fill=(190, 190, 190, 255))
    draw.ellipse([vx + 23, vy + 15, vx + 26, vy + 18], fill=(190, 190, 190, 255))
    draw.line([vx + 23, vy + 21, vx + 26, vy + 21], fill=(40, 25, 15, 255))
    draw.line([vx + 23, vy + 24, vx + 26, vy + 24], fill=(40, 25, 15, 255))
    
    # 8. Quạt trần cổ điển 3 cánh at (168, 70)
    qx, qy = 180, 80
    draw.ellipse([qx + 6, qy + 6, qx + 16, qy + 16], fill=(60, 75, 65, 255), outline=(120, 140, 130, 255))
    # Cánh 1 (lên)
    draw.polygon([(qx + 10, qy + 6), (qx + 12, qy + 6), (qx + 13, qy - 12), (qx + 9, qy - 12)], fill=(80, 100, 85, 255))
    # Cánh 2 (phải dưới)
    draw.polygon([(qx + 15, qy + 13), (qx + 14, qy + 15), (qx + 28, qy + 24), (qx + 30, qy + 21)], fill=(80, 100, 85, 255))
    # Cánh 3 (trái dưới)
    draw.polygon([(qx + 7, qy + 13), (qx + 8, qy + 15), (qx - 6, qy + 24), (qx - 8, qy + 21)], fill=(80, 100, 85, 255))
    
    out_path = os.path.join(ASSETS_DIR, "rural_decorations.png")
    img.save(out_path)
    print("Created rural_decorations.png successfully!")

if __name__ == "__main__":
    generate_player_outfits()
    generate_rural_decorations()
