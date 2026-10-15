extends CharacterBody2D
class_name NPCVillager

@export var npc_name: String = "Bác Ba (Trưởng Thôn)"
@export_multiline var dialogue_line: String = ""
@export var custom_texture: Texture2D = null
@export var sprite_region: Rect2 = Rect2(0, 0, 32, 32)

@onready var sprite: Sprite2D = $Sprite2D
@onready var interact_label: Label = $InteractLabel

var dialogue_lines = [
	"Chào cháu! Mảnh đất nông trại làng quê này màu mỡ lắm, ráng chăm sóc nhé!",
	"Hãy lấy cuốc ra xới mấy luống đất hoang rồi gieo hạt tưới nước.",
	"Dưới góc kia có chuồng gà chuồng heo, nhớ chăm sóc đàn gà đẻ trứng nghen!"
]

func _ready() -> void:
	if interact_label:
		interact_label.visible = false
	if custom_texture and sprite:
		sprite.texture = custom_texture
		sprite.region_enabled = true
		sprite.region_rect = sprite_region

func interact(inventory: InventoryData, ui: Node) -> void:
	if ui and ui.has_method("open_dialogue"):
		var text = get_current_dialogue(inventory)
		ui.open_dialogue(npc_name, text)

func get_current_dialogue(inventory: InventoryData) -> String:
	if dialogue_line != "":
		return dialogue_line
	match inventory.current_quest_id:
		1:
			if inventory.quest_progress >= inventory.quest_target:
				inventory.current_quest_id = 2
				inventory.quest_progress = 0
				inventory.quest_target = 2
				inventory.add_coins(50)
				inventory.seeds += 6
				inventory.inventory_changed.emit()
				return "Giỏi lắm cháu! 4 luống đất đã cày xới rất đẹp. Bác thưởng cho cháu 50 xu và thêm hạt giống.\nBây giờ hãy xuống góc chuồng chăm sóc đàn gà và nhặt 2 quả trứng nhé!"
			else:
				return "Chào mừng cháu đến với Game Nông Trại!\nHãy chọn Cuốc (Phím 1) và cuốc sạch 4 ô đất hoang ở ruộng nhé! (Tiến độ: " + str(inventory.quest_progress) + "/" + str(inventory.quest_target) + ")"
		2:
			if inventory.quest_progress >= inventory.quest_target:
				inventory.current_quest_id = 3
				inventory.quest_progress = 0
				inventory.quest_target = 2
				inventory.add_coins(100)
				inventory.inventory_changed.emit()
				return "Tuyệt vời! Trứng gà quê ta to tròn và bổ dưỡng lắm. Thưởng cho cháu 100 xu!\nNhiệm vụ tiếp theo: Hãy tưới nước và thu hoạch 2 bắp ngô đầu mùa mang về đây nhé!"
			else:
				return "Cháu hãy xuống chuồng gà ở góc Tây Nam (dưới nhà kho), lại gần con Gà Mái có biểu tượng quả trứng 🥚 và bấm phím [E] để nhặt trứng nhé!\n💡 Mẹo: Chọn Rơm (Phím 5) bấm [E] cho gà ăn thì gà sẽ đẻ trứng nhanh gấp đôi! (Tiến độ: " + str(inventory.quest_progress) + "/" + str(inventory.quest_target) + ")"
		3:
			if inventory.quest_progress >= inventory.quest_target:
				inventory.current_quest_id = 4
				inventory.add_coins(200)
				inventory.inventory_changed.emit()
				return "Nông sản mùa này bội thu rồi! Cháu đã chứng minh mình là một nông dân thực thụ của làng quê.\nCơ ngơi này từ nay giao trọn cho cháu phát triển!"
			else:
				return "Những luống ngô sau khi gieo hạt và tưới nước sẽ lớn rất nhanh. Hãy thu hoạch 2 bắp ngô nào! (Tiến độ: " + str(inventory.quest_progress) + "/" + str(inventory.quest_target) + ")"
		_:
			return "Cảm ơn cháu đã cần cù chăm sóc nông trại quê mình thật ấm no và xanh tươi!"

func set_nearby(nearby: bool) -> void:
	if interact_label:
		interact_label.visible = nearby
