extends Node
class_name InventoryData

signal inventory_changed()

# Công cụ hiện tại: 1 = Cuốc, 2 = Bình tưới, 3 = Hạt giống, 4 = Liềm, 5 = Rơm, 6 = Bắp ngô, 7 = Trứng gà
var active_tool: int = 1

# Tài nguyên
var coins: int = 150
var seeds: int = 10
var crops_harvested: int = 0
var eggs_collected: int = 0
var hay_bundles: int = 5

# Quests
var current_quest_id: int = 1 # 1: Khai hoang, 2: Tiếng gà ban mai, 3: Chợ phiên
var quest_progress: int = 0 # Tiến độ nhiệm vụ hiện tại
var quest_target: int = 4

func set_active_tool(tool_id: int) -> void:
	if tool_id >= 1 and tool_id <= 7:
		active_tool = tool_id
		inventory_changed.emit()

func consume_crop() -> bool:
	if crops_harvested > 0:
		crops_harvested -= 1
		inventory_changed.emit()
		return true
	return false

func consume_egg() -> bool:
	if eggs_collected > 0:
		eggs_collected -= 1
		inventory_changed.emit()
		return true
	return false

func add_crop(amount: int = 1) -> void:
	crops_harvested += amount
	if current_quest_id == 3:
		quest_progress += amount
	inventory_changed.emit()

func add_egg(amount: int = 1) -> void:
	eggs_collected += amount
	if current_quest_id == 2:
		quest_progress += amount
	inventory_changed.emit()

func use_seed() -> bool:
	if seeds > 0:
		seeds -= 1
		inventory_changed.emit()
		return true
	return false

func use_hay() -> bool:
	if hay_bundles > 0:
		hay_bundles -= 1
		inventory_changed.emit()
		return true
	return false

func add_coins(amount: int) -> void:
	coins += amount
	inventory_changed.emit()
