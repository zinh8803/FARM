"""
Script tạo sprite cho phương tiện (Xe đạp, Xe máy Super Cub)
và tinh chỉnh màu sắc gạch/nền nông trại theo đúng phong cách tham khảo.
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_vehicles():
    # Kích thước: 160 x 256
    # 5 cột x 8 hàng (Mỗi ô 32x32)
    # Cột 0..2: Hoạt ảnh người chơi lái xe 3 frames (Idle, Move1, Move2)
    # Cột 3: Xe dựng chân chống đứng yên (Parked)
    # Cột 4: Chi tiết phụ / Đèn / Khói
    # Hàng 0..3: Xe đạp (Down, Up, Left, Right)
    # Hàng 4..7: Xe máy (Down, Up, Left, Right)
    
    W, H = 160, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # -------------------------------------------------------------
    # 1. XE ĐẠP (BICYCLE) - HÀNG 0..3
    # -------------------------------------------------------------
    # Màu sắc xe đạp: Khung thép xanh cổ vịt (24, 78, 68), vành bánh xe bạc (190, 195, 200),
    # yên da nâu (120, 65, 30), giỏ mây vàng trước ghi đông (210, 175, 110)
    
    # Parked Bicycle (Cột 3)
    # Side view parked (Row 2, Col 3)
    px = 3 * 32
    py = 2 * 32
    # Bánh xe sau & trước (bán kính r=5)
    draw.ellipse([px + 3, py + 19, px + 13, py + 29], outline=(50, 50, 50, 255), fill=(185, 190, 195, 255))
    draw.ellipse([px + 5, py + 21, px + 11, py + 27], fill=(0, 0, 0, 0), outline=(100, 100, 100, 255))
    draw.ellipse([px + 19, py + 19, px + 29, py + 29], outline=(50, 50, 50, 255), fill=(185, 190, 195, 255))
    draw.ellipse([px + 21, py + 21, px + 27, py + 27], fill=(0, 0, 0, 0), outline=(100, 100, 100, 255))
    # Khung xe kim cương cổ điển
    draw.line([px + 8, py + 24, px + 14, py + 16], fill=(28, 88, 75, 255), width=2) # gióng đứng
    draw.line([px + 14, py + 16, px + 23, py + 16], fill=(28, 88, 75, 255), width=2) # gióng ngang
    draw.line([px + 14, py + 16, px + 16, py + 24], fill=(28, 88, 75, 255), width=2) # gióng chéo
    draw.line([px + 16, py + 24, px + 23, py + 16], fill=(28, 88, 75, 255), width=2) # gióng dưới
    draw.line([px + 23, py + 16, px + 24, py + 24], fill=(28, 88, 75, 255), width=2) # càng trước
    # Ghi đông & Giỏ xe
    draw.line([px + 23, py + 16, px + 22, py + 11], fill=(180, 185, 190, 255), width=2)
    draw.line([px + 20, py + 11, px + 25, py + 11], fill=(40, 40, 40, 255), width=2) # tay lái
    draw.rectangle([px + 24, py + 12, px + 29, py + 17], fill=(215, 180, 115, 255), outline=(140, 100, 50, 255)) # giỏ mây
    # Yên xe & Baga chở hàng
    draw.rectangle([px + 12, py + 14, px + 16, py + 16], fill=(135, 75, 35, 255)) # yên da
    draw.rectangle([px + 5, py + 16, px + 12, py + 18], fill=(160, 165, 170, 255)) # baga sau
    # Chân chống nghiêng
    draw.line([px + 15, py + 24, px + 12, py + 30], fill=(80, 80, 80, 255), width=1)

    # Lặp qua các hướng lái xe đạp (Player on Bicycle)
    for row, dir_name in enumerate(["down", "up", "left", "right"]):
        for col in range(3):
            fx = col * 32
            fy = row * 32
            pedal_shift = 0 if col == 0 else (-1 if col == 1 else 1)
            
            if dir_name in ["left", "right"]:
                # Vẽ xe đạp hướng ngang
                flip = (dir_name == "left")
                
                # Bánh sau
                bx1 = fx + (19 if flip else 3)
                bx2 = fx + (29 if flip else 13)
                draw.ellipse([bx1, fy + 19, bx2, fy + 29], outline=(50, 50, 50, 255), fill=(185, 190, 195, 255))
                # Bánh trước
                fx1 = fx + (3 if flip else 19)
                fx2 = fx + (13 if flip else 29)
                draw.ellipse([fx1, fy + 19, fx2, fy + 29], outline=(50, 50, 50, 255), fill=(185, 190, 195, 255))
                
                # Khung sườn
                cx = fx + (17 if flip else 15)
                draw.line([bx1 + 5, fy + 24, cx, fy + 18], fill=(28, 88, 75, 255), width=2)
                draw.line([cx, fy + 18, fx1 + 5, fy + 24], fill=(28, 88, 75, 255), width=2)
                
                # Bàn đạp & Chân đạp
                draw.ellipse([cx - 2, fy + 22, cx + 2, fy + 26], fill=(160, 160, 160, 255))
                
                # Người nông dân ngồi trên xe đạp
                # Chân
                draw.rectangle([cx - 2, fy + 19, cx + 2, fy + 24 + pedal_shift], fill=(75, 55, 40, 255))
                # Thân người & Áo bà ba vàng
                draw.rectangle([cx - 4, fy + 12, cx + 4, fy + 19], fill=(243, 187, 68, 255))
                # Tay cầm ghi đông
                hx = fx + (8 if flip else 24)
                draw.line([cx + (-1 if flip else 1), fy + 14, hx, fy + 15], fill=(240, 210, 170, 255), width=2)
                # Đầu & Nón lá
                head_x = cx + (-2 if flip else 2)
                draw.rectangle([head_x - 3, fy + 8, head_x + 3, fy + 12], fill=(252, 212, 169, 255))
                # Nón lá hình chóp nón
                draw.polygon([
                    (head_x, fy + 3),
                    (head_x - 8, fy + 8),
                    (head_x + 8, fy + 8)
                ], fill=(245, 230, 185, 255), outline=(190, 170, 120, 255))
                
                # Giỏ xe đằng trước
                gx = fx + (2 if flip else 25)
                draw.rectangle([gx, fy + 15, gx + 5, fy + 19], fill=(215, 180, 115, 255))
                
            elif dir_name == "down":
                # Nhìn từ phía trước
                cx = fx + 16
                # Bánh xe trước
                draw.rectangle([cx - 2, fy + 20, cx + 2, fy + 30], fill=(50, 50, 50, 255))
                # Ghi đông ngang
                draw.line([cx - 8, fy + 17, cx + 8, fy + 17], fill=(180, 185, 190, 255), width=2)
                # Giỏ trước
                draw.rectangle([cx - 5, fy + 18, cx + 5, fy + 23], fill=(215, 180, 115, 255), outline=(140, 100, 50, 255))
                # Chân hai bên bàn đạp
                draw.rectangle([cx - 6, fy + 21, cx - 4, fy + 26 + pedal_shift], fill=(75, 55, 40, 255))
                draw.rectangle([cx + 4, fy + 21, cx + 6, fy + 26 - pedal_shift], fill=(75, 55, 40, 255))
                # Thân người & Áo vàng
                draw.rectangle([cx - 5, fy + 12, cx + 5, fy + 20], fill=(243, 187, 68, 255))
                draw.line([cx - 5, fy + 14, cx - 7, fy + 17], fill=(240, 210, 170, 255), width=2)
                draw.line([cx + 5, fy + 14, cx + 7, fy + 17], fill=(240, 210, 170, 255), width=2)
                # Mặt
                draw.rectangle([cx - 3, fy + 8, cx + 3, fy + 12], fill=(252, 212, 169, 255))
                draw.point((cx - 2, fy + 10), fill=(40, 30, 20, 255))
                draw.point((cx + 2, fy + 10), fill=(40, 30, 20, 255))
                # Nón lá
                draw.polygon([(cx, fy + 3), (cx - 9, fy + 8), (cx + 9, fy + 8)], fill=(245, 230, 185, 255), outline=(190, 170, 120, 255))

            elif dir_name == "up":
                # Nhìn từ phía sau
                cx = fx + 16
                # Bánh xe sau
                draw.rectangle([cx - 2, fy + 21, cx + 2, fy + 30], fill=(50, 50, 50, 255))
                # Baga sau
                draw.rectangle([cx - 4, fy + 19, cx + 4, fy + 22], fill=(160, 165, 170, 255))
                # Chân
                draw.rectangle([cx - 6, fy + 20, cx - 4, fy + 26 + pedal_shift], fill=(75, 55, 40, 255))
                draw.rectangle([cx + 4, fy + 20, cx + 6, fy + 26 - pedal_shift], fill=(75, 55, 40, 255))
                # Lưng áo vàng
                draw.rectangle([cx - 5, fy + 12, cx + 5, fy + 20], fill=(243, 187, 68, 255))
                # Nón lá nhìn từ sau
                draw.polygon([(cx, fy + 3), (cx - 9, fy + 9), (cx + 9, fy + 9)], fill=(245, 230, 185, 255), outline=(190, 170, 120, 255))


    # -------------------------------------------------------------
    # 2. XE MÁY (MOTORBIKE - HONDA SUPER CUB / WAVE) - HÀNG 4..7
    # -------------------------------------------------------------
    # Màu sắc: Sơn xanh biển retro (32, 125, 160), Yếm trắng sữa (245, 245, 240),
    # Yên đen (40, 40, 40), Ống bô kim loại mạ crom (210, 215, 220), Đèn pha tròn sáng vàng (255, 235, 130)

    # Parked Motorbike (Cột 3, Row 6)
    mx = 3 * 32
    my = 6 * 32
    # Bánh sau & Bánh trước
    draw.ellipse([mx + 2, my + 18, mx + 13, my + 29], outline=(40, 40, 40, 255), fill=(170, 175, 180, 255))
    draw.ellipse([mx + 5, my + 21, mx + 10, my + 26], fill=(40, 40, 40, 255))
    draw.ellipse([mx + 19, my + 18, mx + 30, my + 29], outline=(40, 40, 40, 255), fill=(170, 175, 180, 255))
    draw.ellipse([mx + 22, my + 21, mx + 27, my + 26], fill=(40, 40, 40, 255))
    # Thân xe máy xanh retro
    draw.rectangle([mx + 8, my + 17, mx + 20, my + 22], fill=(32, 125, 160, 255))
    # Yếm trắng sữa đặc trưng Super Cub
    draw.polygon([(mx + 16, my + 14), (mx + 22, my + 14), (mx + 23, my + 24), (mx + 18, my + 24)], fill=(245, 245, 238, 255), outline=(210, 210, 200, 255))
    # Yên xe dài đen
    draw.rectangle([mx + 7, my + 14, mx + 16, my + 17], fill=(45, 45, 45, 255))
    # Đầu xe & Đèn pha tròn
    draw.rectangle([mx + 21, my + 12, mx + 25, my + 15], fill=(32, 125, 160, 255))
    draw.ellipse([mx + 24, my + 12, mx + 27, my + 15], fill=(255, 240, 140, 255), outline=(210, 215, 220, 255)) # Đèn pha
    # Gương chiếu hậu
    draw.line([mx + 23, my + 12, mx + 22, my + 8], fill=(160, 160, 160, 255), width=1)
    draw.ellipse([mx + 21, my + 7, mx + 24, my + 9], fill=(200, 220, 240, 255))
    # Ống xả bô mạ crom
    draw.line([mx + 7, my + 25, mx + 18, my + 25], fill=(215, 220, 225, 255), width=2)
    # Chân chống nghiêng
    draw.line([mx + 15, my + 24, mx + 12, my + 30], fill=(60, 60, 60, 255), width=2)

    # Lặp qua các hướng lái xe máy
    for r_idx, dir_name in enumerate(["down", "up", "left", "right"]):
        row = 4 + r_idx
        for col in range(3):
            fx = col * 32
            fy = row * 32
            vibe = 0 if col == 0 else (-1 if col == 1 else 1) # rung lắc nhẹ khi chạy
            
            if dir_name in ["left", "right"]:
                flip = (dir_name == "left")
                
                # Bánh sau & trước
                bx1 = fx + (19 if flip else 2)
                bx2 = fx + (30 if flip else 13)
                draw.ellipse([bx1, fy + 18, bx2, fy + 29], outline=(40, 40, 40, 255), fill=(170, 175, 180, 255))
                fx1 = fx + (2 if flip else 19)
                fx2 = fx + (13 if flip else 30)
                draw.ellipse([fx1, fy + 18, fx2, fy + 29], outline=(40, 40, 40, 255), fill=(170, 175, 180, 255))
                
                # Thân xe & Ống bô
                draw.rectangle([fx + 8, fy + 17, fx + 24, fy + 23], fill=(32, 125, 160, 255))
                # Yếm trắng
                yx = fx + (10 if flip else 17)
                draw.rectangle([yx, fy + 15, yx + 5, fy + 23], fill=(245, 245, 238, 255))
                # Ống bô sau xả khói
                exhaust_x = bx1 + (2 if flip else 6)
                draw.line([fx + 10, fy + 25, exhaust_x, fy + 25], fill=(215, 220, 225, 255), width=2)
                
                # Đèn pha trước chiếu sáng
                lx = fx + (2 if flip else 27)
                draw.ellipse([lx - 1, fy + 13, lx + 2, fy + 16], fill=(255, 245, 160, 255))
                
                # Người lái xe máy
                seat_x = fx + (18 if flip else 12)
                # Quần nâu ngồi trên yên
                draw.rectangle([seat_x - 3, fy + 15, seat_x + 4, fy + 22], fill=(75, 55, 40, 255))
                # Thân người hơi nghiêng về phía trước đón gió
                lean = -1 if flip else 1
                draw.rectangle([seat_x - 3 + lean, fy + 10 + vibe, seat_x + 4 + lean, fy + 17 + vibe], fill=(243, 187, 68, 255))
                # Tay lái vươn ra cầm tay ga
                hx = fx + (8 if flip else 23)
                draw.line([seat_x + lean, fy + 13 + vibe, hx, fy + 14], fill=(240, 210, 170, 255), width=2)
                # Đầu & Nón lá
                head_x = seat_x + lean * 2
                draw.rectangle([head_x - 3, fy + 6 + vibe, head_x + 3, fy + 10 + vibe], fill=(252, 212, 169, 255))
                # Nón lá buộc dây bay nhẹ
                draw.polygon([
                    (head_x, fy + 1 + vibe),
                    (head_x - 8, fy + 6 + vibe),
                    (head_x + 8, fy + 6 + vibe)
                ], fill=(245, 230, 185, 255), outline=(190, 170, 120, 255))
                
            elif dir_name == "down":
                cx = fx + 16
                # Bánh xe trước bản to
                draw.rectangle([cx - 2, fy + 21, cx + 2, fy + 30], fill=(40, 40, 40, 255))
                # Yếm xe trắng 2 bên
                draw.rectangle([cx - 7, fy + 17, cx - 3, fy + 24], fill=(245, 245, 238, 255))
                draw.rectangle([cx + 3, fy + 17, cx + 7, fy + 24], fill=(245, 245, 238, 255))
                # Đèn pha tròn lớn ở chính giữa
                draw.ellipse([cx - 3, fy + 15, cx + 3, fy + 20], fill=(255, 250, 170, 255), outline=(210, 215, 220, 255))
                # Gương chiếu hậu 2 bên
                draw.ellipse([cx - 9, fy + 10, cx - 6, fy + 13], fill=(200, 225, 245, 255))
                draw.ellipse([cx + 6, fy + 10, cx + 9, fy + 13], fill=(200, 225, 245, 255))
                # Chân gác để chân
                draw.rectangle([cx - 6, fy + 20, cx - 4, fy + 25], fill=(75, 55, 40, 255))
                draw.rectangle([cx + 4, fy + 20, cx + 6, fy + 25], fill=(75, 55, 40, 255))
                # Thân người & Nón lá
                draw.rectangle([cx - 5, fy + 10 + vibe, cx + 5, fy + 17 + vibe], fill=(243, 187, 68, 255))
                draw.rectangle([cx - 3, fy + 6 + vibe, cx + 3, fy + 10 + vibe], fill=(252, 212, 169, 255))
                draw.point((cx - 2, fy + 8 + vibe), fill=(40, 30, 20, 255))
                draw.point((cx + 2, fy + 8 + vibe), fill=(40, 30, 20, 255))
                draw.polygon([(cx, fy + 1 + vibe), (cx - 9, fy + 6 + vibe), (cx + 9, fy + 6 + vibe)], fill=(245, 230, 185, 255), outline=(190, 170, 120, 255))

            elif dir_name == "up":
                cx = fx + 16
                # Bánh sau & Biển số xe & Đèn hậu đỏ
                draw.rectangle([cx - 2, fy + 22, cx + 2, fy + 30], fill=(40, 40, 40, 255))
                draw.rectangle([cx - 4, fy + 18, cx + 4, fy + 21], fill=(225, 45, 45, 255)) # Đèn hậu đỏ
                draw.rectangle([cx - 5, fy + 21, cx + 5, fy + 24], fill=(245, 245, 245, 255)) # Biển số xe trắng
                # Chân
                draw.rectangle([cx - 6, fy + 19, cx - 4, fy + 25], fill=(75, 55, 40, 255))
                draw.rectangle([cx + 4, fy + 19, cx + 6, fy + 25], fill=(75, 55, 40, 255))
                # Lưng áo vàng & Nón lá
                draw.rectangle([cx - 5, fy + 10 + vibe, cx + 5, fy + 17 + vibe], fill=(243, 187, 68, 255))
                draw.polygon([(cx, fy + 1 + vibe), (cx - 9, fy + 7 + vibe), (cx + 9, fy + 7 + vibe)], fill=(245, 230, 185, 255), outline=(190, 170, 120, 255))

    # Cột 4: Hiệu ứng khói xả và đốm bụi
    for i in range(4):
        ey = (4 + i) * 32
        draw.ellipse([4 * 32 + 8, ey + 18, 4 * 32 + 16, ey + 26], fill=(220, 220, 220, 180))
        draw.ellipse([4 * 32 + 18, ey + 15, 4 * 32 + 24, ey + 21], fill=(235, 235, 235, 120))

    img.save(os.path.join(ASSETS_DIR, "vehicles.png"))
    print("Created vehicles.png successfully!")

def update_farm_tiles():
    TILE_SIZE = 32
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def fill_tile(x, y, color):
        draw.rectangle([x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE - 1, (y + 1) * TILE_SIZE - 1], fill=color)

    # 1. Grass Tile (0, 0) - Màu cỏ đồng quê tự nhiên tươi mát theo đúng ảnh tham khảo (#70b56b)
    fill_tile(0, 0, (112, 181, 107, 255))
    # Chấm cỏ và hoa dại li ti
    for px, py, col in [
        (4, 5, (95, 160, 90)), (14, 16, (95, 160, 90)), (24, 7, (95, 160, 90)),
        (18, 25, (132, 198, 125)), (7, 21, (132, 198, 125)), (26, 23, (132, 198, 125)),
        (9, 9, (250, 250, 240)), (21, 13, (245, 235, 130)) # hoa cúc dại vàng trắng
    ]:
        draw.point((px, py), fill=col)

    # 2. Dirt Path Tile (1, 0) - Đường đất làng quê ấm áp (#ddcfb3)
    fill_tile(1, 0, (221, 207, 179, 255))
    ox = 1 * TILE_SIZE
    for px, py, col in [
        (5, 7, (198, 182, 150)), (19, 12, (198, 182, 150)), (14, 25, (198, 182, 150)),
        (26, 6, (235, 225, 202)), (8, 20, (175, 158, 130)), (23, 21, (175, 158, 130)),
        (12, 14, (140, 160, 120)) # mầm cỏ nhỏ ven đường
    ]:
        draw.point((ox + px, py), fill=col)

    # 3. Animal Pen Sand/Dirt (2, 0) - Bãi cát chuồng trại vàng óng (#e8d8a7)
    fill_tile(2, 0, (232, 216, 167, 255))
    ox = 2 * TILE_SIZE
    for px, py, col in [
        (4, 8, (212, 194, 142)), (18, 14, (212, 194, 142)), (11, 24, (212, 194, 142)),
        (24, 26, (244, 230, 185)), (14, 6, (195, 175, 125))
    ]:
        draw.point((ox + px, py), fill=col)

    # 4. Tilled Soil (Dry) (3, 0) - Luống đất nâu đỏ màu mỡ (#68462b)
    fill_tile(3, 0, (104, 70, 43, 255))
    ox = 3 * TILE_SIZE
    for y in range(4, 32, 8):
        draw.rectangle([ox, y, ox + 31, y + 2], fill=(85, 56, 34, 255))
        draw.rectangle([ox, y + 3, ox + 31, y + 4], fill=(125, 86, 54, 255))
    for px, py, col in [(6, 12, (140, 98, 62)), (22, 20, (68, 44, 26)), (15, 28, (140, 98, 62))]:
        draw.point((ox + px, py), fill=col)

    # 5. Tilled Soil (Wet) (4, 0) - Luống đất tưới đẫm nước nâu thẫm (#422b1a)
    fill_tile(4, 0, (66, 43, 26, 255))
    ox = 4 * TILE_SIZE
    for y in range(4, 32, 8):
        draw.rectangle([ox, y, ox + 31, y + 2], fill=(46, 29, 17, 255))
        draw.rectangle([ox, y + 3, ox + 31, y + 4], fill=(86, 57, 36, 255))
    for px, py, col in [(8, 12, (98, 72, 49)), (20, 20, (36, 21, 12)), (14, 28, (98, 72, 49))]:
        draw.point((ox + px, py), fill=col)

    # 6. Untilled Soil (5, 0) - Đất hoang xám rêu có cỏ và sỏi dại đúng như ảnh mẫu (#929e84)
    fill_tile(5, 0, (146, 158, 132, 255))
    ox = 5 * TILE_SIZE
    # Viền mép ô đất luống
    draw.rectangle([ox, 0, ox + 31, 1], fill=(120, 132, 108, 255))
    draw.rectangle([ox, 30, ox + 31, 31], fill=(120, 132, 108, 255))
    draw.rectangle([ox, 0, ox + 1, 31], fill=(120, 132, 108, 255))
    draw.rectangle([ox + 30, 0, ox + 31, 31], fill=(120, 132, 108, 255))
    # Mầm cỏ dại xanh và hoa dại
    for px, py, col in [
        (6, 8, (100, 150, 75)), (7, 7, (100, 150, 75)), (8, 8, (100, 150, 75)),
        (18, 14, (100, 150, 75)), (19, 13, (100, 150, 75)),
        (23, 22, (100, 150, 75)), (24, 21, (100, 150, 75)),
        (11, 24, (240, 230, 130)), # hoa cúc dại li ti
        (14, 18, (120, 130, 110)), (25, 9, (165, 175, 150)) # sỏi nhỏ
    ]:
        draw.point((ox + px, py), fill=col)

    # 7. Wooden Fence Horizontal (0, 1)
    ox = 0 * TILE_SIZE
    oy = 1 * TILE_SIZE
    draw.rectangle([ox + 2, oy + 4, ox + 8, oy + 28], fill=(145, 95, 55, 255))
    draw.rectangle([ox + 24, oy + 4, ox + 30, oy + 28], fill=(145, 95, 55, 255))
    draw.rectangle([ox, oy + 8, ox + 31, oy + 12], fill=(175, 118, 70, 255))
    draw.rectangle([ox, oy + 18, ox + 31, oy + 22], fill=(175, 118, 70, 255))
    draw.rectangle([ox, oy + 8, ox + 31, oy + 9], fill=(200, 145, 95, 255))
    draw.rectangle([ox, oy + 18, ox + 31, oy + 19], fill=(200, 145, 95, 255))

    # 8. Wooden Fence Vertical (1, 1)
    ox = 1 * TILE_SIZE
    oy = 1 * TILE_SIZE
    draw.rectangle([ox + 10, oy, ox + 18, oy + 31], fill=(145, 95, 55, 255))
    draw.rectangle([ox + 12, oy, ox + 14, oy + 31], fill=(175, 118, 70, 255))
    draw.rectangle([ox + 6, oy + 6, ox + 22, oy + 10], fill=(125, 80, 45, 255))
    draw.rectangle([ox + 6, oy + 20, ox + 22, oy + 24], fill=(125, 80, 45, 255))

    # 9. Stone Wall / Perimeter (2, 1)
    ox = 2 * TILE_SIZE
    oy = 1 * TILE_SIZE
    fill_tile(2, 1, (222, 224, 218, 255))
    draw.rectangle([ox, oy, ox + 31, oy + 4], fill=(185, 190, 182, 255))
    draw.rectangle([ox, oy + 28, ox + 31, oy + 31], fill=(160, 165, 158, 255))

    img.save(os.path.join(ASSETS_DIR, "farm_tiles.png"))
    print("Updated farm_tiles.png with authentic harmonious palette!")

if __name__ == "__main__":
    generate_vehicles()
    update_farm_tiles()
