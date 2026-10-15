extends Area2D
class_name FarmPlot

enum State {
	UNTILLED,    # Đất hoang cỏ mọc
	TILLED_DRY,  # Đất luống đã cuốc, khô
	TILLED_WET,  # Đất luống đã tưới nước
	SEEDED,      # Đã gieo hạt
	GROWING,     # Cây non đang lớn
	MATURE       # Cây chín rộ có thể thu hoạch
}

enum CropType {
	CORN,   # Bắp ngô
	RICE,   # Lúa gạo
	VEGGIE  # Rau thơm
}

@export var state: State = State.UNTILLED
@export var crop_type: CropType = CropType.CORN
@export var grid_x: int = 0
@export var grid_y: int = 0

var growth_time: float = 0.0
var growth_needed: float = 15.0 # Giây để cây lớn hoàn toàn
var _last_visual_state: int = -1

@onready var ground_sprite: Sprite2D = $GroundSprite
@onready var crop_sprite: Sprite2D = $CropSprite
@onready var highlight: Control = $Highlight

var is_hovered_by_player: bool = false

func _ready() -> void:
	_last_visual_state = -1
	update_visuals()
	if highlight:
		highlight.visible = false

func _process(delta: float) -> void:
	if state == State.SEEDED or state == State.GROWING:
		growth_time += delta
		if growth_time >= growth_needed:
			state = State.MATURE
			update_visuals()
		elif growth_time >= growth_needed * 0.5 and state == State.SEEDED:
			state = State.GROWING
			update_visuals()

func _play_sfx(action: String) -> void:
	if not is_inside_tree():
		return
	var audio = get_tree().root.get_node_or_null("Main/AudioManager")
	if audio:
		match action:
			"tool": audio.play_tool()
			"water": audio.play_water()
			"plant": audio.play_plant()
			"harvest": audio.play_harvest()

func interact(tool_id: int, inventory: InventoryData, ui: Node = null) -> bool:
	match tool_id:
		1: # Cuốc (Hoe) — cuốc đất hoang hoặc cuốc lại đất sau thu hoạch
			if state == State.UNTILLED:
				state = State.TILLED_DRY
				update_visuals()
				_play_sfx("tool")
				if inventory.current_quest_id == 1:
					inventory.quest_progress += 1
					inventory.inventory_changed.emit()
				if ui and ui.has_method("show_toast"):
					ui.show_toast("🪓 Đã cuốc thành luống đất!")
				return true
		2: # Bình tưới (Watering can)
			if state == State.TILLED_DRY:
				state = State.TILLED_WET
				update_visuals()
				_play_sfx("water")
				if ui and ui.has_method("show_toast"):
					ui.show_toast("💧 Đã tưới nước cho đất!")
				return true
			elif state == State.SEEDED or state == State.GROWING:
				# Tưới nước cho cây đang lớn → tăng tốc độ sinh trưởng
				growth_time += 3.0
				_play_sfx("water")
				if ui and ui.has_method("show_toast"):
					ui.show_toast("💧 Tưới nước, cây lớn nhanh hơn!")
				return true
		3: # Hạt giống (Seeds)
			if (state == State.TILLED_DRY or state == State.TILLED_WET) and inventory.seeds > 0:
				if inventory.use_seed():
					state = State.SEEDED
					growth_time = 0.0
					# Chọn loại cây ngẫu nhiên 
					crop_type = [CropType.CORN, CropType.RICE, CropType.VEGGIE].pick_random()
					update_visuals()
					_play_sfx("plant")
					var crop_name = _get_crop_name()
					if ui and ui.has_method("show_toast"):
						ui.show_toast("🌱 Đã gieo hạt " + crop_name + "!")
					return true
		4: # Liềm (Sickle) / Thu hoạch
			if state == State.MATURE:
				var crop_name = _get_crop_name()
				state = State.TILLED_DRY
				growth_time = 0.0
				inventory.add_crop(1)
				update_visuals()
				_play_sfx("harvest")
				if ui and ui.has_method("show_toast"):
					ui.show_toast("🌾 +1 " + crop_name + " thu hoạch!")
				return true
	
	# Thông báo nếu dùng sai công cụ
	if ui and ui.has_method("show_toast"):
		match tool_id:
			1:
				if state != State.UNTILLED:
					ui.show_toast("Đất này đã cuốc rồi!")
			3:
				if inventory.seeds <= 0:
					ui.show_toast("Hết hạt giống! Mua thêm ở chợ quê.")
				elif state == State.UNTILLED:
					ui.show_toast("Cuốc đất trước rồi mới gieo hạt!")
			4:
				if state != State.MATURE:
					ui.show_toast("Cây chưa chín, chờ thêm chút nữa!")
	return false

func _get_crop_name() -> String:
	match crop_type:
		CropType.CORN: return "Bắp ngô"
		CropType.RICE: return "Lúa gạo"
		CropType.VEGGIE: return "Rau thơm"
	return "Nông sản"

func update_visuals() -> void:
	if not ground_sprite or not crop_sprite:
		return
	
	# Tránh cập nhật không cần thiết
	var visual_key = state * 10 + crop_type
	if visual_key == _last_visual_state:
		return
	_last_visual_state = visual_key
	
	crop_sprite.visible = false
	
	match state:
		State.UNTILLED:
			ground_sprite.region_rect = Rect2(160, 0, 32, 32)
		State.TILLED_DRY:
			ground_sprite.region_rect = Rect2(96, 0, 32, 32)
		State.TILLED_WET:
			ground_sprite.region_rect = Rect2(128, 0, 32, 32)
		State.SEEDED:
			ground_sprite.region_rect = Rect2(128, 0, 32, 32)
			crop_sprite.visible = true
			crop_sprite.region_rect = Rect2(32, 0, 32, 32)
		State.GROWING:
			ground_sprite.region_rect = Rect2(128, 0, 32, 32)
			crop_sprite.visible = true
			crop_sprite.region_rect = Rect2(64, 0, 32, 32)
		State.MATURE:
			ground_sprite.region_rect = Rect2(128, 0, 32, 32)
			crop_sprite.visible = true
			crop_sprite.region_rect = Rect2(96, 0, 32, 32)

func set_highlight(val: bool) -> void:
	is_hovered_by_player = val
	if highlight:
		highlight.visible = val
