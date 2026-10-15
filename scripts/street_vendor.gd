extends CharacterBody2D
class_name StreetVendor

enum VendorType {
	SUGARCANE = 0, # Chị Ba (Nước mía & Dừa tươi)
	STREET_HAWKER = 1, # Bác Tư (Gánh bánh mì & Trái cây)
	SNACK_CART = 2, # Anh Bảy (Cá viên chiên & Bắp xào)
	DRINK_STALL = 3 # Cô Năm (Cà phê muối & Trà đá)
}

@export var vendor_type: VendorType = VendorType.SUGARCANE
@export var vendor_name: String = "Người Bán Hàng Rong"

@onready var sprite: Sprite2D = $Sprite2D
@onready var interact_label: Label = $InteractLabel

func _ready() -> void:
	if interact_label:
		interact_label.visible = false
	update_appearance()

func update_appearance() -> void:
	if not sprite:
		return
	var col = int(vendor_type) % 4
	sprite.region_rect = Rect2(col * 64, 0, 64, 48)

func interact(inventory: InventoryData, ui: Node) -> void:
	var text = ""
	var item_cost = 10
	
	match vendor_type:
		VendorType.SUGARCANE:
			vendor_name = "Chị Ba (Nước Mía & Dừa Xiêm)"
			item_cost = 10
			if inventory.coins >= item_cost:
				inventory.coins -= item_cost
				inventory.inventory_changed.emit()
				# Buff speed
				buff_player_speed(ui, 1.35, 45.0)
				text = "Chị Ba ép liền cho em một ly Nước Mía Siêu Sạch mát rượi (-10 xu)!\n🥤 Uống xong cảm giác sảng khoái, tốc độ di chuyển tăng +35% trong 45 giây nhé!"
			else:
				text = "Nước mía siêu sạch 10 xu một ly, dừa xiêm ngọt lịm em ơi!\nCứ ra biển hóng mát đi, khi nào có tiền quay lại ủng hộ chị nghen!"
				
		VendorType.STREET_HAWKER:
			vendor_name = "Bác Tư (Gánh Bánh Mì & Trái Cây)"
			item_cost = 15
			if inventory.coins >= item_cost:
				inventory.coins -= item_cost
				inventory.seeds += 3
				inventory.inventory_changed.emit()
				buff_player_speed(ui, 1.25, 30.0)
				text = "Bác lấy cho cháu ổ Bánh Mì Sài Gòn giòn rụm mới ra lò (-15 xu)!\n🥖 Bác tặng kèm cháu 3 gói hạt giống rau sạch quê mình để đem về nông trại gieo trồng nhé!"
			else:
				text = "Bánh mì đặc ruột nóng hổi 15 xu/ổ đây cháu ơi!\nĂn một ổ bánh mì kẹp chả giòn rụm lấy sức chăm sóc ruộng đồng nào!"
				
		VendorType.SNACK_CART:
			vendor_name = "Anh Bảy (Cá Viên Chiên & Bắp Xào)"
			item_cost = 12
			if inventory.coins >= item_cost:
				inventory.coins -= item_cost
				inventory.inventory_changed.emit()
				buff_player_speed(ui, 1.3, 35.0)
				text = "Xiên Cá Viên Chiên và Bắp Xào Bơ thơm nức mũi của em đây (-12 xu)!\n🍢 Ăn nóng cho giòn nha! Tốc độ chạy tăng +30%!"
			else:
				text = "Cá viên chiên, bò viên, xúc xích bắp xào bơ tép khô thơm phức đây!\nMỗi phần 12 xu thôi em ơi, dạo đại lộ ngắm xe chạy là phải có xiên que nhâm nhi!"
				
		VendorType.DRINK_STALL:
			vendor_name = "Cô Năm (Cà Phê Muối & Trà Đá)"
			item_cost = 10
			if inventory.coins >= item_cost:
				inventory.coins -= item_cost
				inventory.inventory_changed.emit()
				buff_player_speed(ui, 1.4, 50.0)
				text = "Cô pha cho con ly Cà Phê Muối béo ngậy thơm lừng (-10 xu)!\n☕ Uống vào tỉnh táo cả người, tốc độ tăng +40% trong 50 giây, tha hồ lái xe đạp ngắm biển!"
			else:
				text = "Ghé ngồi ghế nhựa làm ly cà phê muối hoặc trà đá ngắm xe chạy đi con!\nĐại lộ ven biển này chiều tối gió thổi mát rười rượi luôn đó!"

	if ui and ui.has_method("open_dialogue"):
		ui.open_dialogue(vendor_name, text)

func buff_player_speed(ui: Node, multiplier: float, duration: float) -> void:
	if not ui:
		return
	var main_scene = ui.get_tree().root.get_node_or_null("Main")
	if main_scene and main_scene.get("player_instance"):
		var p = main_scene.player_instance
		if p and p.has_method("apply_speed_buff"):
			p.apply_speed_buff(multiplier, duration)

func set_nearby(nearby: bool) -> void:
	if interact_label:
		interact_label.visible = nearby
