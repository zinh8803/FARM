"""
Script tạo đầy đủ các texture pixel art chất lượng cao cho game Little DaNang
theo đúng phong cách và hình mẫu tham khảo.
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_tiles():
    # 256x256 tileset (16x16 or 32x32 tiles, we use 32x32 for crisp pixel detail)
    # Tile size = 32x32
    TILE_SIZE = 32
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Helper to draw rect
    def fill_tile(x, y, color):
        draw.rectangle([x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE - 1, (y + 1) * TILE_SIZE - 1], fill=color)

    # 1. Grass Tile (0, 0)
    fill_tile(0, 0, (131, 184, 89, 255))
    for px, py, col in [
        (4, 5, (110, 162, 69)), (12, 18, (110, 162, 69)), (24, 8, (110, 162, 69)),
        (18, 26, (145, 198, 102)), (8, 22, (145, 198, 102)), (27, 24, (145, 198, 102)),
        (10, 10, (250, 250, 240)), (22, 14, (240, 230, 120)) # tiny daisies
    ]:
        draw.point((px, py), fill=col)

    # 2. Dirt Path Tile (1, 0)
    fill_tile(1, 0, (213, 199, 165, 255))
    ox = 1 * TILE_SIZE
    for px, py, col in [
        (5, 7, (185, 170, 138)), (19, 12, (185, 170, 138)), (14, 25, (185, 170, 138)),
        (26, 6, (228, 218, 190)), (8, 20, (160, 142, 115)), (23, 21, (160, 142, 115)),
        (12, 14, (130, 150, 110)) # tiny grass speck
    ]:
        draw.point((ox + px, py), fill=col)

    # 3. Animal Pen Sand/Dirt (2, 0)
    fill_tile(2, 0, (228, 200, 117, 255))
    ox = 2 * TILE_SIZE
    for px, py, col in [
        (4, 8, (210, 180, 95)), (18, 14, (210, 180, 95)), (11, 24, (210, 180, 95)),
        (24, 26, (240, 215, 140)), (14, 6, (190, 160, 80))
    ]:
        draw.point((ox + px, py), fill=col)

    # 4. Tilled Soil (Dry) (3, 0) - luống đất cày
    fill_tile(3, 0, (101, 67, 42, 255))
    ox = 3 * TILE_SIZE
    # Furrow lines
    for y in range(4, 32, 8):
        draw.rectangle([ox, y, ox + 31, y + 2], fill=(82, 54, 32, 255))
        draw.rectangle([ox, y + 3, ox + 31, y + 4], fill=(122, 82, 51, 255))
    # granule specks
    for px, py, col in [(6, 12, (135, 95, 60)), (22, 20, (65, 42, 25)), (15, 28, (135, 95, 60))]:
        draw.point((ox + px, py), fill=col)

    # 5. Tilled Soil (Wet / Watered) (4, 0)
    fill_tile(4, 0, (65, 42, 26, 255))
    ox = 4 * TILE_SIZE
    for y in range(4, 32, 8):
        draw.rectangle([ox, y, ox + 31, y + 2], fill=(45, 28, 16, 255))
        draw.rectangle([ox, y + 3, ox + 31, y + 4], fill=(85, 55, 35, 255))
    for px, py, col in [(8, 12, (95, 70, 48)), (20, 20, (35, 20, 12)), (14, 28, (95, 70, 48))]:
        draw.point((ox + px, py), fill=col)

    # 6. Untilled / Weedy Soil (5, 0)
    fill_tile(5, 0, (130, 139, 112, 255))
    ox = 5 * TILE_SIZE
    # patches of dried dirt and grass tufts
    for px, py, col in [
        (4, 6, (94, 122, 70)), (5, 5, (94, 122, 70)), (5, 6, (94, 122, 70)),
        (18, 16, (94, 122, 70)), (19, 15, (94, 122, 70)), (18, 17, (94, 122, 70)),
        (10, 24, (110, 118, 95)), (25, 8, (150, 160, 130)), (22, 26, (94, 122, 70))
    ]:
        draw.point((ox + px, py), fill=col)

    # 7. Wooden Fence Horizontal (0, 1)
    ox = 0 * TILE_SIZE
    oy = 1 * TILE_SIZE
    # fence posts
    draw.rectangle([ox + 2, oy + 4, ox + 8, oy + 28], fill=(138, 88, 50, 255))
    draw.rectangle([ox + 24, oy + 4, ox + 30, oy + 28], fill=(138, 88, 50, 255))
    # horizontal rails
    draw.rectangle([ox, oy + 8, ox + 31, oy + 12], fill=(168, 110, 65, 255))
    draw.rectangle([ox, oy + 18, ox + 31, oy + 22], fill=(168, 110, 65, 255))
    # highlights
    draw.rectangle([ox, oy + 8, ox + 31, oy + 9], fill=(195, 138, 90, 255))
    draw.rectangle([ox, oy + 18, ox + 31, oy + 19], fill=(195, 138, 90, 255))

    # 8. Wooden Fence Vertical (1, 1)
    ox = 1 * TILE_SIZE
    oy = 1 * TILE_SIZE
    draw.rectangle([ox + 10, oy, ox + 18, oy + 31], fill=(138, 88, 50, 255))
    draw.rectangle([ox + 12, oy, ox + 14, oy + 31], fill=(168, 110, 65, 255))
    # cross ties
    draw.rectangle([ox + 6, oy + 6, ox + 22, oy + 10], fill=(120, 75, 40, 255))
    draw.rectangle([ox + 6, oy + 20, ox + 22, oy + 24], fill=(120, 75, 40, 255))

    # 9. Stone Wall / Perimeter (2, 1)
    ox = 2 * TILE_SIZE
    oy = 1 * TILE_SIZE
    fill_tile(2, 1, (215, 218, 212, 255))
    # Stone border bricks
    draw.rectangle([ox, oy, ox + 31, oy + 4], fill=(175, 180, 172, 255))
    draw.rectangle([ox, oy + 28, ox + 31, oy + 31], fill=(150, 155, 148, 255))
    for y in [10, 18, 26]:
        draw.line([ox, oy + y, ox + 31, oy + y], fill=(170, 175, 168))
    for x in [8, 20]:
        draw.line([ox + x, oy + 5, ox + x, oy + 18], fill=(170, 175, 168))
    draw.line([ox + 14, oy + 18, ox + 14, oy + 28], fill=(170, 175, 168))

    img.save(os.path.join(ASSETS_DIR, "farm_tiles.png"))
    print("Created farm_tiles.png")

def create_house():
    # Traditional Vietnamese house with red tile roof, veranda, flower vines
    # Size: 192 x 160 (fits nicely as a prominent landmark)
    W, H = 192, 160
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Main Roof (Trapezoid / Vietnamese gable roof)
    # Roof base: y from 8 to 72
    roof_top_y = 10
    roof_bottom_y = 70
    roof_left_top = 28
    roof_right_top = 164
    roof_left_bot = 8
    roof_right_bot = 184

    # Roof fill
    draw.polygon([
        (roof_left_top, roof_top_y), (roof_right_top, roof_top_y),
        (roof_right_bot, roof_bottom_y), (roof_left_bot, roof_bottom_y)
    ], fill=(184, 62, 53, 255))

    # Red tile ridge at apex
    draw.rectangle([roof_left_top - 4, roof_top_y - 4, roof_right_top + 4, roof_top_y + 2], fill=(120, 35, 28, 255))
    draw.rectangle([roof_left_top - 2, roof_top_y - 2, roof_right_top + 2, roof_top_y], fill=(210, 88, 78, 255))
    # Chimney / vent on right
    draw.rectangle([150, 2, 158, 12], fill=(140, 50, 40, 255))

    # Tile lines & shingles
    for y in range(roof_top_y + 6, roof_bottom_y, 7):
        progress = (y - roof_top_y) / (roof_bottom_y - roof_top_y)
        cur_l = int(roof_left_top - progress * (roof_left_top - roof_left_bot))
        cur_r = int(roof_right_top + progress * (roof_right_bot - roof_right_top))
        draw.line([cur_l, y, cur_r, y], fill=(110, 35, 29, 255), width=2)
        draw.line([cur_l, y + 2, cur_r, y + 2], fill=(210, 88, 78, 255), width=1)

    # Vertical tile rows
    for x in range(roof_left_bot + 8, roof_right_bot - 8, 8):
        draw.line([x + 6, roof_top_y + 4, x, roof_bottom_y - 2], fill=(145, 45, 38, 180), width=1)

    # Roof eaves shadow
    draw.rectangle([roof_left_bot - 2, roof_bottom_y - 2, roof_right_bot + 2, roof_bottom_y + 4], fill=(70, 20, 16, 255))

    # 2. House Walls (under eaves)
    wall_l = 18
    wall_r = 174
    wall_top = roof_bottom_y + 4
    wall_bot = 140
    # Cream / ochre wall
    draw.rectangle([wall_l, wall_top, wall_r, wall_bot], fill=(234, 216, 176, 255))
    # Wall base foundation
    draw.rectangle([wall_l, wall_bot - 8, wall_r, wall_bot], fill=(190, 170, 130, 255))

    # 3. Veranda / Porch Floor (sân gạch trước hiên)
    draw.rectangle([10, wall_bot, 182, 154], fill=(200, 120, 85, 255))
    # Brick lines
    for x in range(10, 182, 14):
        draw.line([x, wall_bot, x, 154], fill=(160, 90, 60, 255))
    draw.line([10, 147, 182, 147], fill=(160, 90, 60, 255))
    # Foundation border
    draw.rectangle([8, 153, 184, 156], fill=(130, 135, 125, 255))

    # 4. Wooden Pillars
    for px in [24, 68, 124, 166]:
        draw.rectangle([px, wall_top, px + 6, wall_bot], fill=(120, 75, 40, 255))
        draw.rectangle([px + 1, wall_top, px + 3, wall_bot], fill=(155, 100, 55, 255))

    # 5. Main Double Wooden Door (Center)
    door_l, door_r = 78, 114
    door_top, door_bot = wall_top + 10, wall_bot
    # Door frame
    draw.rectangle([door_l - 2, door_top - 2, door_r + 2, door_bot], fill=(75, 45, 22, 255))
    # Door panels
    draw.rectangle([door_l, door_top, door_l + 16, door_bot], fill=(138, 85, 45, 255))
    draw.rectangle([door_l + 18, door_top, door_r, door_bot], fill=(138, 85, 45, 255))
    # Center open dark gap
    draw.rectangle([door_l + 14, door_top + 2, door_l + 20, door_bot], fill=(25, 20, 22, 255))
    # Red festival paper banner (bùa/khánh may mắn)
    draw.rectangle([door_l + 15, door_top + 8, door_l + 19, door_bot - 14], fill=(215, 38, 38, 255))
    draw.rectangle([door_l + 16, door_top + 14, door_l + 18, door_top + 20], fill=(245, 210, 60, 255))

    # 6. Windows with vertical wood bars (Left & Right)
    for wx in [36, 136]:
        draw.rectangle([wx, wall_top + 14, wx + 26, wall_top + 38], fill=(60, 40, 25, 255))
        draw.rectangle([wx + 2, wall_top + 16, wx + 24, wall_top + 36], fill=(30, 22, 16, 255))
        # vertical wooden bars
        for bx in [wx + 6, wx + 11, wx + 16, wx + 21]:
            draw.line([bx, wall_top + 16, bx, wall_top + 36], fill=(150, 95, 50, 255), width=2)
        # horizontal frame
        draw.line([wx + 2, wall_top + 26, wx + 24, wall_top + 26], fill=(100, 65, 35, 255), width=1)

    # 7. Flower Vines & Bougainvillea on Roof & Eaves (Giàn hoa giấy nở rộ)
    vine_pts = [
        (16, 48), (24, 42), (32, 52), (40, 46), (52, 40), (60, 50),
        (72, 44), (82, 54), (96, 48), (110, 56), (124, 48), (138, 54),
        (148, 44), (160, 52), (170, 46), (180, 56), (28, 64), (54, 68),
        (88, 70), (120, 68), (150, 70), (172, 66)
    ]
    # Green leaves
    for vx, vy in vine_pts:
        draw.ellipse([vx - 5, vy - 4, vx + 5, vy + 4], fill=(70, 125, 50, 240))
        draw.ellipse([vx - 3, vy - 2, vx + 3, vy + 2], fill=(95, 160, 65, 255))
    # Bright Pink Bougainvillea blossoms
    for vx, vy in vine_pts:
        draw.ellipse([vx - 3, vy - 3, vx + 3, vy + 3], fill=(216, 93, 123, 255))
        draw.ellipse([vx - 1, vy - 1, vx + 1, vy + 1], fill=(245, 150, 175, 255))

    # 8. Climbing Trellis on right side of porch
    draw.rectangle([170, wall_top, 178, wall_bot + 10], fill=(110, 70, 35, 255))
    for ty in range(wall_top + 4, wall_bot + 8, 8):
        draw.line([170, ty, 178, ty], fill=(160, 105, 55, 255), width=2)
    # leaves climbing up
    for ty in [wall_top + 8, wall_top + 20, wall_top + 32, wall_top + 44]:
        draw.ellipse([168, ty - 3, 174, ty + 3], fill=(70, 130, 50, 255))
        draw.ellipse([174, ty + 1, 180, ty + 7], fill=(216, 93, 123, 255))

    # 9. Ceramic Water Urn (Lu nước / Chum sành) & Broom on Porch
    # Urn at (152, 130)
    draw.ellipse([150, 124, 164, 140], fill=(120, 60, 30, 255))
    draw.ellipse([152, 122, 162, 127], fill=(85, 40, 20, 255))
    draw.ellipse([153, 127, 158, 135], fill=(160, 85, 45, 255)) # highlight
    # Broom (Chổi rơm) on left (60, 130)
    draw.line([64, 120, 60, 142], fill=(160, 110, 60, 255), width=2)
    draw.polygon([(57, 134), (64, 134), (66, 144), (54, 144)], fill=(225, 185, 85, 255))

    img.save(os.path.join(ASSETS_DIR, "house.png"))
    print("Created house.png")

def create_barn():
    # Barn for animals (Góc Tây Nam)
    # Size: 128 x 112
    W, H = 128, 112
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Roof (Gable roof, greenish-zinc / weathered wood)
    draw.polygon([(64, 6), (122, 42), (6, 42)], fill=(88, 107, 102, 255))
    draw.polygon([(64, 6), (68, 8), (122, 42), (118, 44), (6, 44)], fill=(65, 80, 75, 255))
    # Ridge highlight
    draw.line([64, 6, 6, 42], fill=(120, 145, 138, 255), width=2)
    draw.line([64, 6, 122, 42], fill=(120, 145, 138, 255), width=2)

    # Attic window
    draw.rectangle([56, 22, 72, 36], fill=(235, 230, 220, 255))
    draw.rectangle([58, 24, 70, 34], fill=(45, 55, 50, 255))
    draw.line([64, 24, 64, 34], fill=(235, 230, 220, 255), width=1)
    draw.line([58, 29, 70, 29], fill=(235, 230, 220, 255), width=1)

    # Walls (warm wood planks)
    draw.rectangle([14, 42, 114, 104], fill=(147, 90, 56, 255))
    # Plank vertical lines
    for x in range(14, 114, 10):
        draw.line([x, 42, x, 104], fill=(110, 65, 38, 255), width=1)

    # Windows on sides with white frames
    for wx in [20, 94]:
        draw.rectangle([wx, 54, wx + 16, 72], fill=(240, 240, 240, 255))
        draw.rectangle([wx + 2, 56, wx + 14, 70], fill=(110, 160, 200, 255)) # glass
        draw.line([wx + 8, 56, wx + 8, 70], fill=(240, 240, 240, 255), width=1)
        draw.line([wx + 2, 63, wx + 14, 63], fill=(240, 240, 240, 255), width=1)

    # Big Double Barn Door
    door_l, door_r = 44, 84
    draw.rectangle([door_l - 2, 50, door_r + 2, 104], fill=(60, 35, 20, 255))
    draw.rectangle([door_l, 52, door_l + 18, 104], fill=(235, 230, 220, 255))
    draw.rectangle([door_l + 20, 52, door_r, 104], fill=(235, 230, 220, 255))
    # Open center gap
    draw.rectangle([door_l + 15, 54, door_l + 23, 104], fill=(30, 20, 15, 255))
    # Barn door cross 'X'
    draw.line([door_l + 2, 54, door_l + 16, 102], fill=(180, 140, 100, 255), width=2)
    draw.line([door_l + 16, 54, door_l + 2, 102], fill=(180, 140, 100, 255), width=2)
    draw.line([door_l + 22, 54, door_r - 2, 102], fill=(180, 140, 100, 255), width=2)
    draw.line([door_r - 2, 54, door_l + 22, 102], fill=(180, 140, 100, 255), width=2)

    img.save(os.path.join(ASSETS_DIR, "barn.png"))
    print("Created barn.png")

def create_props():
    # Props sheet:
    # 1. Haystack (đống rơm tròn hình nón)
    # 2. Bamboo cluster (bụi tre)
    # 3. Banana tree with bunch & flower (cây chuối)
    # 4. Clothesline with clothes (dây phơi quần áo)
    # 5. Farm signpost (biển chỉ dẫn)
    # Size: 256 x 256
    W, H = 256, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Haystack (64 x 64 at 0, 0)
    # Golden dome / cone of straw
    draw.polygon([(32, 8), (56, 54), (8, 54)], fill=(217, 169, 50, 255))
    draw.ellipse([8, 46, 56, 60], fill=(217, 169, 50, 255))
    # Straw highlights & texture
    for _ in range(15):
        draw.line([24, 18, 16, 50], fill=(245, 205, 90, 255), width=1)
        draw.line([38, 20, 48, 52], fill=(180, 130, 35, 255), width=1)
        draw.line([32, 12, 34, 54], fill=(255, 225, 110, 255), width=1)
    # Wooden pole on top
    draw.line([32, 2, 32, 14], fill=(120, 80, 40, 255), width=2)

    # 2. Bamboo Cluster (Bụi tre - 64 x 96 at 64, 0)
    bx = 64
    for stem_x in [bx + 14, bx + 26, bx + 38, bx + 50]:
        # Tall green cane
        draw.rectangle([stem_x, 10, stem_x + 4, 90], fill=(67, 133, 59, 255))
        draw.rectangle([stem_x + 1, 10, stem_x + 2, 90], fill=(113, 168, 79, 255))
        # Joints (đốt tre)
        for jy in range(20, 90, 14):
            draw.line([stem_x - 1, jy, stem_x + 5, jy], fill=(175, 195, 110, 255), width=2)
            # Bamboo leaves shooting out
            draw.line([stem_x + 2, jy, stem_x - 8, jy - 6], fill=(55, 120, 50, 255), width=2)
            draw.line([stem_x + 2, jy, stem_x + 12, jy - 5], fill=(70, 140, 60, 255), width=2)

    # 3. Banana Tree (Cây chuối trổ buồng - 64 x 96 at 128, 0)
    cx = 128
    # Trunk
    draw.rectangle([cx + 28, 46, cx + 36, 92], fill=(125, 155, 90, 255))
    draw.line([cx + 31, 46, cx + 31, 92], fill=(150, 185, 110, 255), width=2)
    # Giant broad arching leaves
    # Top left leaf
    draw.polygon([(cx + 32, 50), (cx + 6, 20), (cx + 2, 28), (cx + 28, 54)], fill=(53, 122, 56, 255))
    draw.line([(cx + 32, 50), (cx + 4, 24)], fill=(120, 180, 80, 255), width=2)
    # Top right leaf
    draw.polygon([(cx + 32, 50), (cx + 58, 18), (cx + 62, 26), (cx + 36, 54)], fill=(65, 145, 68, 255))
    draw.line([(cx + 32, 50), (cx + 60, 22)], fill=(130, 195, 90, 255), width=2)
    # Middle leaves
    draw.polygon([(cx + 32, 52), (cx + 60, 48), (cx + 56, 56), (cx + 34, 58)], fill=(48, 110, 50, 255))
    draw.polygon([(cx + 32, 52), (cx + 4, 48), (cx + 8, 56), (cx + 30, 58)], fill=(45, 105, 48, 255))
    # Hanging Banana Bunch & Purple Flower (Bắp chuối)
    # bunch (yellow-green bananas)
    draw.ellipse([cx + 38, 58, cx + 46, 68], fill=(212, 180, 59, 255))
    # purple-red blossom
    draw.polygon([(cx + 40, 68), (cx + 44, 68), (cx + 42, 78)], fill=(120, 54, 79, 255))

    # 4. Clothesline with clothes (Dây phơi quần áo - 96 x 48 at 0, 96)
    lx = 0
    ly = 96
    # Left & right wooden posts
    draw.rectangle([lx + 6, ly + 8, lx + 10, ly + 46], fill=(138, 88, 50, 255))
    draw.rectangle([lx + 86, ly + 8, lx + 90, ly + 46], fill=(138, 88, 50, 255))
    # Cross t-bar on posts
    draw.line([lx + 2, ly + 10, lx + 14, ly + 10], fill=(168, 110, 65, 255), width=2)
    draw.line([lx + 82, ly + 10, lx + 94, ly + 10], fill=(168, 110, 65, 255), width=2)
    # Sagging rope
    draw.line([lx + 8, ly + 12, lx + 48, ly + 16], fill=(210, 200, 180, 255), width=1)
    draw.line([lx + 48, ly + 16, lx + 88, ly + 12], fill=(210, 200, 180, 255), width=1)
    # Clothes hanging:
    # 1. Red shirt
    draw.rectangle([lx + 18, ly + 14, lx + 32, ly + 28], fill=(214, 64, 64, 255))
    draw.rectangle([lx + 16, ly + 14, lx + 34, ly + 18], fill=(185, 45, 45, 255))
    # 2. Blue shirt
    draw.rectangle([lx + 38, ly + 16, lx + 54, ly + 32], fill=(44, 155, 196, 255))
    # 3. Yellow / White shirt
    draw.rectangle([lx + 60, ly + 15, lx + 76, ly + 30], fill=(245, 240, 225, 255))

    # 5. Farm Signpost (Biển chỉ dẫn - 32 x 32 at 100, 96)
    sx = 100
    sy = 96
    draw.rectangle([sx + 14, sy + 14, sx + 18, sy + 31], fill=(138, 88, 50, 255))
    draw.rectangle([sx + 6, sy + 4, sx + 26, sy + 16], fill=(235, 220, 190, 255))
    draw.rectangle([sx + 7, sy + 5, sx + 25, sy + 15], fill=(210, 190, 155, 255))
    draw.line([sx + 9, sy + 8, sx + 23, sy + 8], fill=(180, 50, 40, 255), width=1)
    draw.line([sx + 9, sy + 12, sx + 20, sy + 12], fill=(80, 60, 40, 255), width=1)

    # 6. Fruit Tree (Cây ăn quả - 64 x 64 at 192, 0)
    tx = 192
    ty = 0
    # Trunk
    draw.rectangle([tx + 28, ty + 36, tx + 36, ty + 60], fill=(130, 85, 50, 255))
    # Foliage round crown
    draw.ellipse([tx + 10, ty + 6, tx + 54, ty + 46], fill=(95, 160, 65, 255))
    draw.ellipse([tx + 14, ty + 10, tx + 50, ty + 42], fill=(120, 185, 80, 255))
    # Fruits (red/orange apples or mangoes)
    for fx, fy in [(tx + 22, ty + 18), (tx + 40, ty + 16), (tx + 26, ty + 30), (tx + 44, ty + 28)]:
        draw.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=(225, 65, 50, 255))

    img.save(os.path.join(ASSETS_DIR, "props.png"))
    print("Created props.png")

def create_player():
    # Player character (Nông dân đội nón lá, áo bà ba vàng, quần nâu)
    # Sprite sheet: 4 directions (Down, Up, Left, Right) x 3 frames (Idle, Walk1, Walk2)
    # Frame size: 32 x 32
    # Sheet size: 96 x 128 (3 cols x 4 rows)
    W, H = 96, 128
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for row, direction in enumerate(["down", "up", "left", "right"]):
        for col, step in enumerate([0, 1, 2]): # 0=idle, 1=walk1, 2=walk2
            fx = col * 32
            fy = row * 32
            leg_offset = 0 if step == 0 else (-2 if step == 1 else 2)

            # 1. Legs / Pants (Dark brown)
            if direction in ["down", "up"]:
                draw.rectangle([fx + 11, fy + 22, fx + 14, fy + 29 + (1 if step == 1 else 0)], fill=(75, 55, 40, 255))
                draw.rectangle([fx + 17, fy + 22, fx + 20, fy + 29 + (1 if step == 2 else 0)], fill=(75, 55, 40, 255))
                # Feet
                draw.rectangle([fx + 11, fy + 29, fx + 14, fy + 31], fill=(240, 210, 170, 255))
                draw.rectangle([fx + 17, fy + 29, fx + 20, fy + 31], fill=(240, 210, 170, 255))
            else: # left or right
                draw.rectangle([fx + 13 + leg_offset, fy + 22, fx + 18 - leg_offset, fy + 30], fill=(75, 55, 40, 255))
                draw.rectangle([fx + 13 + leg_offset, fy + 29, fx + 18 - leg_offset, fy + 31], fill=(240, 210, 170, 255))

            # 2. Body / Shirt (Áo bà ba vàng)
            draw.rectangle([fx + 11, fy + 14, fx + 20, fy + 23], fill=(243, 187, 68, 255))
            draw.rectangle([fx + 12, fy + 15, fx + 19, fy + 22], fill=(250, 205, 95, 255))
            # Buttons down the middle
            if direction == "down":
                for by in [fy + 16, fy + 18, fy + 20]:
                    draw.point((fx + 15, by), fill=(180, 120, 30, 255))

            # Arms
            if direction == "down":
                draw.rectangle([fx + 8, fy + 15, fx + 10, fy + 22], fill=(240, 210, 170, 255))
                draw.rectangle([fx + 21, fy + 15, fx + 23, fy + 22], fill=(240, 210, 170, 255))
            elif direction == "left":
                draw.rectangle([fx + 10, fy + 15, fx + 13, fy + 22], fill=(240, 210, 170, 255))
            elif direction == "right":
                draw.rectangle([fx + 18, fy + 15, fx + 21, fy + 22], fill=(240, 210, 170, 255))

            # 3. Head & Face (Skin tone)
            draw.rectangle([fx + 12, fy + 8, fx + 19, fy + 14], fill=(252, 212, 169, 255))
            if direction == "down":
                # eyes & smile
                draw.point((fx + 14, fy + 11), fill=(40, 30, 20, 255))
                draw.point((fx + 17, fy + 11), fill=(40, 30, 20, 255))
                draw.point((fx + 15, fy + 13), fill=(210, 110, 90, 255))
                draw.point((fx + 16, fy + 13), fill=(210, 110, 90, 255))
            elif direction == "left":
                draw.point((fx + 13, fy + 11), fill=(40, 30, 20, 255))
            elif direction == "right":
                draw.point((fx + 18, fy + 11), fill=(40, 30, 20, 255))

            # 4. Conical Hat (Nón lá Việt Nam - Iconic!)
            # Shape: triangle with broad circular base
            draw.polygon([(fx + 15, fy + 1), (fx + 26, fy + 9), (fx + 5, fy + 9)], fill=(222, 209, 150, 255))
            # Ring textures on the conical hat
            draw.line([fx + 8, fy + 7, fx + 23, fy + 7], fill=(195, 180, 120, 255), width=1)
            draw.line([fx + 11, fy + 5, fx + 20, fy + 5], fill=(195, 180, 120, 255), width=1)
            # Apex point
            draw.point((fx + 15, fy + 1), fill=(170, 150, 90, 255))
            # Hat string (quai nón) under chin
            if direction == "down":
                draw.line([fx + 10, fy + 9, fx + 14, fy + 14], fill=(200, 60, 60, 255), width=1)
                draw.line([fx + 21, fy + 9, fx + 17, fy + 14], fill=(200, 60, 60, 255), width=1)

    img.save(os.path.join(ASSETS_DIR, "player.png"))
    print("Created player.png")

def create_animals():
    # Animals:
    # 1. Chicken / Rooster (Gà)
    # 2. Duck (Vịt)
    # 3. Pig (Heo)
    # Sheet size: 96 x 96 (3 animals x 3 animation frames, 32x32 each)
    W, H = 96, 96
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Row 0: Rooster / Chicken (Gà)
    for col, step in enumerate([0, 1, 2]):
        fx = col * 32
        fy = 0
        peck_y = 2 if step == 1 else 0
        # Body
        draw.ellipse([fx + 10, fy + 12 + peck_y, fx + 22, fy + 24 + peck_y], fill=(168, 105, 60, 255))
        # Wing
        draw.ellipse([fx + 12, fy + 14 + peck_y, fx + 18, fy + 20 + peck_y], fill=(130, 75, 40, 255))
        # Tail feathers (black/green sheen)
        draw.polygon([(fx + 8, fy + 16 + peck_y), (fx + 4, fy + 10 + peck_y), (fx + 11, fy + 14 + peck_y)], fill=(35, 55, 45, 255))
        # Head & neck
        draw.ellipse([fx + 18, fy + 8 + peck_y, fx + 24, fy + 15 + peck_y], fill=(195, 125, 75, 255))
        # Eye
        draw.point((fx + 21, fy + 10 + peck_y), fill=(20, 20, 20, 255))
        # Yellow Beak
        draw.polygon([(fx + 24, fy + 11 + peck_y), (fx + 27, fy + 13 + peck_y), (fx + 24, fy + 14 + peck_y)], fill=(245, 190, 40, 255))
        # Red Comb (mào gà) & Wattle
        draw.polygon([(fx + 20, fy + 6 + peck_y), (fx + 23, fy + 4 + peck_y), (fx + 22, fy + 8 + peck_y)], fill=(220, 40, 40, 255))
        draw.point((fx + 22, fy + 14 + peck_y), fill=(220, 40, 40, 255))
        # Legs
        draw.line([fx + 14, fy + 24 + peck_y, fx + 14, fy + 28], fill=(245, 190, 40, 255), width=1)
        draw.line([fx + 18, fy + 24 + peck_y, fx + 18, fy + 28], fill=(245, 190, 40, 255), width=1)

    # Row 1: Duck (Vịt trắng)
    for col, step in enumerate([0, 1, 2]):
        fx = col * 32
        fy = 32
        waddle = -1 if step == 1 else (1 if step == 2 else 0)
        # White body
        draw.ellipse([fx + 9, fy + 14 + waddle, fx + 22, fy + 25 + waddle], fill=(248, 248, 248, 255))
        draw.ellipse([fx + 10, fy + 16 + waddle, fx + 17, fy + 22 + waddle], fill=(225, 225, 230, 255)) # wing
        # Neck & head
        draw.ellipse([fx + 18, fy + 8 + waddle, fx + 24, fy + 16 + waddle], fill=(255, 255, 255, 255))
        draw.point((fx + 21, fy + 10 + waddle), fill=(30, 30, 30, 255))
        # Yellow-orange beak (mỏ vịt bẹt)
        draw.rectangle([fx + 24, fy + 11 + waddle, fx + 28, fy + 14 + waddle], fill=(245, 170, 35, 255))
        # Orange webbed feet
        draw.rectangle([fx + 13, fy + 25, fx + 16, fy + 28], fill=(245, 140, 30, 255))
        draw.rectangle([fx + 18, fy + 25, fx + 21, fy + 28], fill=(245, 140, 30, 255))

    # Row 2: Pig (Heo / Lợn hồng)
    for col, step in enumerate([0, 1, 2]):
        fx = col * 32
        fy = 64
        trot = 1 if step == 1 else (-1 if step == 2 else 0)
        # Pink round body
        draw.ellipse([fx + 6, fy + 10, fx + 25, fy + 25], fill=(243, 165, 181, 255))
        # Head
        draw.ellipse([fx + 18, fy + 9, fx + 28, fy + 22], fill=(248, 175, 192, 255))
        # Snout (mõm lợn)
        draw.ellipse([fx + 26, fy + 13, fx + 30, fy + 19], fill=(225, 130, 155, 255))
        draw.point((fx + 28, fy + 15), fill=(160, 70, 95, 255))
        draw.point((fx + 28, fy + 17), fill=(160, 70, 95, 255))
        # Eye & Ear
        draw.point((fx + 22, fy + 12), fill=(40, 30, 35, 255))
        draw.polygon([(fx + 19, fy + 8), (fx + 23, fy + 6), (fx + 22, fy + 10)], fill=(225, 130, 155, 255))
        # Curly tail
        draw.line([fx + 6, fy + 16, fx + 3, fy + 14], fill=(225, 130, 155, 255), width=1)
        # Legs
        draw.rectangle([fx + 10 + trot, fy + 23, fx + 13 + trot, fy + 28], fill=(225, 140, 160, 255))
        draw.rectangle([fx + 20 - trot, fy + 23, fx + 23 - trot, fy + 28], fill=(225, 140, 160, 255))

    img.save(os.path.join(ASSETS_DIR, "animals.png"))
    print("Created animals.png")

def create_crops_and_items():
    # Crops & Items sheet (32 x 32 each, 128 x 128 sheet)
    # (0, 0): Seed packet
    # (1, 0): Small Sprout
    # (2, 0): Growing Plant
    # (3, 0): Mature Corn / Crop
    # (0, 1): Hoe (Cuốc)
    # (1, 1): Watering Can (Bình tưới)
    # (2, 1): Sickle (Liềm)
    # (3, 1): Animal Fodder (Bó rơm/thóc)
    # (0, 2): Egg (Trứng gà)
    # (1, 2): Harvested Watermelon / Corn (Nông sản)
    # (2, 2): Coin (Đồng xu)
    # (3, 2): Heart bubble
    W, H = 128, 128
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Seed Packet (0, 0)
    draw.rectangle([8, 6, 24, 26], fill=(220, 195, 140, 255))
    draw.rectangle([10, 8, 22, 14], fill=(160, 80, 45, 255))
    draw.ellipse([13, 17, 18, 22], fill=(60, 140, 50, 255))

    # 2. Sprout (1, 0)
    ox = 32
    draw.line([ox + 16, 26, ox + 16, 18], fill=(120, 185, 70, 255), width=2)
    draw.ellipse([ox + 12, 16, ox + 16, 20], fill=(95, 165, 55, 255))
    draw.ellipse([ox + 16, 16, ox + 20, 20], fill=(95, 165, 55, 255))

    # 3. Growing Plant (2, 0)
    ox = 64
    draw.line([ox + 16, 28, ox + 16, 12], fill=(85, 155, 55, 255), width=2)
    draw.ellipse([ox + 8, 14, ox + 16, 22], fill=(70, 145, 45, 255))
    draw.ellipse([ox + 16, 12, ox + 24, 20], fill=(70, 145, 45, 255))
    draw.ellipse([ox + 10, 20, ox + 18, 26], fill=(65, 135, 40, 255))

    # 4. Mature Crop (Corn / Vegetable) (3, 0)
    ox = 96
    draw.line([ox + 16, 28, ox + 16, 8], fill=(65, 135, 40, 255), width=3)
    draw.ellipse([ox + 6, 10, ox + 16, 22], fill=(55, 125, 35, 255))
    draw.ellipse([ox + 16, 8, ox + 26, 20], fill=(55, 125, 35, 255))
    # Golden corn cob
    draw.rectangle([ox + 13, 11, ox + 19, 21], fill=(245, 200, 45, 255))
    draw.rectangle([ox + 14, 12, ox + 18, 20], fill=(255, 225, 80, 255))

    # 5. Hoe (Cuốc) (0, 1)
    oy = 32
    draw.line([6, oy + 26, 22, oy + 8], fill=(145, 95, 50, 255), width=2) # handle
    draw.rectangle([18, oy + 6, 26, oy + 12], fill=(160, 165, 175, 255)) # iron blade

    # 6. Watering Can (Bình tưới) (1, 1)
    ox = 32
    oy = 32
    draw.rectangle([ox + 8, oy + 12, ox + 20, oy + 24], fill=(70, 140, 190, 255))
    draw.rectangle([ox + 9, oy + 13, ox + 19, oy + 15], fill=(120, 180, 225, 255))
    # handle & spout
    draw.line([ox + 6, oy + 14, ox + 6, oy + 22], fill=(50, 105, 150, 255), width=2)
    draw.line([ox + 20, oy + 18, ox + 27, oy + 12], fill=(70, 140, 190, 255), width=2)
    draw.ellipse([ox + 26, oy + 10, ox + 29, oy + 14], fill=(160, 165, 175, 255))

    # 7. Sickle (Liềm) (2, 1)
    ox = 64
    oy = 32
    draw.rectangle([ox + 8, oy + 20, ox + 12, oy + 26], fill=(145, 95, 50, 255)) # handle
    # Curved blade
    draw.arc([ox + 8, oy + 6, ox + 24, oy + 22], start=180, end=360, fill=(185, 190, 200, 255), width=3)

    # 8. Animal Fodder / Straw bundle (3, 1)
    ox = 96
    oy = 32
    draw.rectangle([ox + 8, oy + 10, ox + 24, oy + 22], fill=(225, 185, 60, 255))
    draw.line([ox + 16, oy + 10, ox + 16, oy + 22], fill=(160, 60, 40, 255), width=2) # binding cord
    draw.line([ox + 6, oy + 12, ox + 26, oy + 12], fill=(245, 215, 95, 255), width=1)

    # 9. Egg (Trứng gà) (0, 2)
    oy = 64
    draw.ellipse([10, oy + 10, 22, oy + 24], fill=(245, 230, 200, 255))
    draw.ellipse([12, oy + 12, 18, oy + 18], fill=(255, 248, 235, 255))

    # 10. Harvested Watermelon / Produce (1, 2)
    ox = 32
    oy = 64
    draw.ellipse([ox + 8, oy + 8, ox + 24, oy + 24], fill=(50, 125, 45, 255))
    draw.line([ox + 12, oy + 10, ox + 12, oy + 22], fill=(25, 75, 25, 255), width=2)
    draw.line([ox + 20, oy + 10, ox + 20, oy + 22], fill=(25, 75, 25, 255), width=2)

    # 11. Coin (Đồng tiền) (2, 2)
    ox = 64
    oy = 64
    draw.ellipse([ox + 8, oy + 8, ox + 24, oy + 24], fill=(245, 195, 40, 255))
    draw.ellipse([ox + 11, oy + 11, ox + 21, oy + 21], fill=(215, 160, 25, 255))

    # 12. Heart Emotion (3, 2)
    ox = 96
    oy = 64
    draw.polygon([(ox + 16, oy + 22), (ox + 8, oy + 13), (ox + 12, oy + 8), (ox + 16, oy + 12), (ox + 20, oy + 8), (ox + 24, oy + 13)], fill=(235, 50, 65, 255))

    img.save(os.path.join(ASSETS_DIR, "crops_and_items.png"))
    print("Created crops_and_items.png")

if __name__ == "__main__":
    create_tiles()
    create_house()
    create_barn()
    create_props()
    create_player()
    create_animals()
    create_crops_and_items()
    print("All assets successfully generated!")
