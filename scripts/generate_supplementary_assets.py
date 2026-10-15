"""
Script bổ sung tài nguyên pixel art cho các map mới:
- Nội thất nhà cổ (House Interior)
- Chợ quê & Làng dân cư (Village Market)
- Rừng trúc & Cổng làng (Bamboo Forest & Gate)
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_interior_assets():
    # 128 x 128 interior furniture and flooring
    W, H = 128, 128
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Antique Red/Ochre Floor Tile (0, 0) - 32x32
    draw.rectangle([0, 0, 31, 31], fill=(185, 95, 65, 255))
    draw.rectangle([1, 1, 30, 30], fill=(210, 115, 80, 255))
    draw.line([0, 0, 31, 31], fill=(160, 80, 50, 255), width=1)
    draw.line([0, 31, 31, 0], fill=(160, 80, 50, 255), width=1)
    draw.rectangle([12, 12, 19, 19], fill=(235, 150, 110, 255))

    # 2. Wood Plank Wall (1, 0) - 32x32
    draw.rectangle([32, 0, 63, 31], fill=(135, 85, 45, 255))
    for x in range(32, 64, 8):
        draw.line([x, 0, x, 31], fill=(95, 55, 28, 255), width=1)
        draw.line([x + 1, 0, x + 1, 31], fill=(160, 105, 58, 255), width=1)

    # 3. Wooden Daybed / Sập Gụ (64x32 at 64, 0)
    sx, sy = 64, 0
    draw.rectangle([sx + 2, sy + 4, sx + 61, sy + 28], fill=(110, 60, 30, 255))
    draw.rectangle([sx + 4, sy + 6, sx + 59, sy + 26], fill=(150, 85, 45, 255))
    # Mat / Chiếu cói
    draw.rectangle([sx + 8, sy + 8, sx + 55, sy + 24], fill=(220, 200, 140, 255))
    for y in range(sy + 10, sy + 24, 4):
        draw.line([sx + 8, y, sx + 55, y], fill=(195, 175, 115, 255), width=1)
    # Pillow / gối mây
    draw.rectangle([sx + 10, sy + 10, sx + 18, sy + 22], fill=(190, 70, 70, 255))

    # 4. Ancestral Altar / Bàn thờ gia tiên (64x48 at 0, 32)
    ax, ay = 0, 32
    # Altar table (deep mahogany / gỗ gụ)
    draw.rectangle([ax + 6, ay + 14, ax + 58, ay + 44], fill=(90, 40, 20, 255))
    draw.rectangle([ax + 8, ay + 16, ax + 56, ay + 42], fill=(125, 58, 30, 255))
    draw.rectangle([ax + 4, ay + 12, ax + 60, ay + 16], fill=(70, 30, 15, 255)) # top lip
    # Incense burner / Bát hương vàng đồng
    draw.ellipse([ax + 27, ay + 6, ax + 37, ay + 14], fill=(215, 175, 45, 255))
    # Red incense sticks / Chân nhang đỏ
    for ix in [ax + 30, ax + 32, ax + 34]:
        draw.line([ix, ay + 8, ix, ay + 1], fill=(220, 40, 40, 255), width=1)
        draw.point((ix, ay), fill=(255, 180, 50, 255)) # glowing tip
    # Candle stands / Chân đèn hai bên
    draw.rectangle([ax + 12, ay + 4, ax + 16, ay + 14], fill=(215, 175, 45, 255))
    draw.point((ax + 14, ay + 2), fill=(255, 100, 40, 255))
    draw.rectangle([ax + 48, ay + 4, ax + 52, ay + 14], fill=(215, 175, 45, 255))
    draw.point((ax + 50, ay + 2), fill=(255, 100, 40, 255))

    # 5. Tea Table & Stools / Bộ bàn trà ấm tích (64x48 at 64, 32)
    tx, ty = 64, 32
    # Round table
    draw.ellipse([tx + 16, ty + 10, tx + 48, ty + 36], fill=(115, 65, 35, 255))
    draw.ellipse([tx + 18, ty + 12, tx + 46, ty + 34], fill=(155, 95, 55, 255))
    # Teapot (Ấm tích ủ trong giỏ mây)
    draw.ellipse([tx + 28, ty + 18, tx + 36, ty + 26], fill=(220, 190, 130, 255))
    draw.point((tx + 32, ty + 20), fill=(240, 240, 240, 255))
    # Teacups
    draw.point((tx + 24, ty + 24), fill=(245, 245, 245, 255))
    draw.point((tx + 40, ty + 24), fill=(245, 245, 245, 255))
    # 2 Wooden stools
    draw.ellipse([tx + 4, ty + 18, tx + 14, ty + 28], fill=(100, 55, 30, 255))
    draw.ellipse([tx + 50, ty + 18, tx + 60, ty + 28], fill=(100, 55, 30, 255))

    # 6. Exit Mat / Door Threshold (32x16 at 0, 80)
    draw.rectangle([0, 80, 31, 95], fill=(160, 120, 70, 255))
    draw.line([0, 80, 31, 80], fill=(240, 210, 120, 255), width=2)
    draw.line([0, 95, 31, 95], fill=(100, 70, 40, 255), width=1)

    img.save(os.path.join(ASSETS_DIR, "interior_tiles.png"))
    print("Created interior_tiles.png")

def create_market_assets():
    # 128 x 128 Market stalls, lanterns, village gate
    W, H = 128, 128
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Vegetable Market Stall / Sạp rau củ Cô Út (64x48 at 0, 0)
    sx, sy = 0, 0
    # Canopy (Striped bamboo & cloth awning)
    draw.polygon([(sx + 4, sy + 16), (sx + 32, sy + 4), (sx + 60, sy + 16)], fill=(215, 60, 60, 255))
    # White stripes
    for px in [sx + 16, sx + 32, sx + 48]:
        draw.line([px, sy + 8, px, sy + 16], fill=(245, 245, 245, 255), width=2)
    # Wooden counter
    draw.rectangle([sx + 8, sy + 16, sx + 56, sy + 42], fill=(135, 85, 45, 255))
    draw.rectangle([sx + 10, sy + 18, sx + 54, sy + 38], fill=(170, 110, 60, 255))
    # Produce baskets (Cà chua, dưa hấu, rau thơm)
    # Tomatoes basket
    draw.ellipse([sx + 12, sy + 22, sx + 22, sy + 30], fill=(225, 55, 45, 255))
    # Greens basket
    draw.ellipse([sx + 26, sy + 20, sx + 38, sy + 30], fill=(60, 155, 60, 255))
    # Corn basket
    draw.ellipse([sx + 42, sy + 22, sx + 52, sy + 30], fill=(245, 200, 45, 255))

    # 2. Hoi An Lanterns / Đèn lồng treo (32x32 at 64, 0)
    lx, ly = 64, 0
    # Rope
    draw.line([lx, ly + 6, lx + 31, ly + 6], fill=(100, 80, 60, 255), width=1)
    # Red lantern
    draw.ellipse([lx + 6, ly + 8, lx + 16, ly + 22], fill=(225, 45, 45, 255))
    draw.ellipse([lx + 8, ly + 10, lx + 14, ly + 20], fill=(255, 100, 100, 255))
    draw.line([lx + 11, ly + 22, lx + 11, ly + 26], fill=(245, 195, 40, 255), width=1) # tassel
    # Yellow lantern
    draw.ellipse([lx + 18, ly + 8, lx + 28, ly + 22], fill=(245, 195, 40, 255))
    draw.ellipse([lx + 20, ly + 10, lx + 26, ly + 20], fill=(255, 225, 90, 255))
    draw.line([lx + 23, ly + 22, lx + 23, ly + 26], fill=(225, 45, 45, 255), width=1)

    # 3. Traditional Village Stone Arch / Cổng Làng Đá (64x64 at 0, 48)
    gx, gy = 0, 48
    # Left & right pillars
    draw.rectangle([gx + 6, gy + 16, gx + 18, gy + 62], fill=(190, 195, 190, 255))
    draw.rectangle([gx + 8, gy + 18, gx + 16, gy + 60], fill=(220, 225, 220, 255))
    draw.rectangle([gx + 46, gy + 16, gx + 58, gy + 62], fill=(190, 195, 190, 255))
    draw.rectangle([gx + 48, gy + 18, gx + 56, gy + 60], fill=(220, 225, 220, 255))
    # Curved stone arch roof
    draw.polygon([(gx + 2, gy + 16), (gx + 32, gy + 4), (gx + 62, gy + 16)], fill=(160, 60, 45, 255))
    draw.polygon([(gx + 4, gy + 14), (gx + 32, gy + 6), (gx + 60, gy + 14)], fill=(195, 75, 55, 255))
    # Arch lintel banner: "LÀNG QUÊ"
    draw.rectangle([gx + 18, gy + 16, gx + 46, gy + 26], fill=(175, 180, 175, 255))
    draw.rectangle([gx + 20, gy + 18, gx + 44, gy + 24], fill=(210, 40, 40, 255))

    # 4. Stream / Water Tile (32x32 at 64, 48)
    wx, wy = 64, 48
    draw.rectangle([wx, wy, wx + 31, wy + 31], fill=(55, 135, 195, 255))
    draw.line([wx + 4, wy + 8, wx + 24, wy + 8], fill=(95, 175, 235, 255), width=1)
    draw.line([wx + 10, wy + 18, wx + 28, wy + 18], fill=(140, 205, 255, 255), width=1)
    draw.line([wx + 2, wy + 26, wx + 18, wy + 26], fill=(95, 175, 235, 255), width=1)

    # 5. Wooden Bridge (32x32 at 96, 48)
    bx, by = 96, 48
    draw.rectangle([bx + 4, by, bx + 28, by + 31], fill=(140, 90, 50, 255))
    for y in range(by + 2, by + 31, 6):
        draw.line([bx + 4, y, bx + 28, y], fill=(180, 125, 75, 255), width=2)
        draw.line([bx + 4, y + 2, bx + 28, y + 2], fill=(100, 60, 30, 255), width=1)
    # Railings
    draw.line([bx + 4, by, bx + 4, by + 31], fill=(90, 50, 25, 255), width=2)
    draw.line([bx + 28, by, bx + 28, by + 31], fill=(90, 50, 25, 255), width=2)

    img.save(os.path.join(ASSETS_DIR, "market_tiles.png"))
    print("Created market_tiles.png")

if __name__ == "__main__":
    create_interior_assets()
    create_market_assets()
    print("All supplementary map assets generated successfully!")
