extends CharacterBody2D
class_name Animal

enum AnimalType {
	ROOSTER, # Gà trống
	HEN,     # Gà mái
	DUCK,    # Vịt
	PIG      # Lợn
}

@export var animal_type: AnimalType = AnimalType.ROOSTER
@export var min_x: float = 40.0
@export var max_x: float = 190.0
@export var min_y: float = 245.0
@export var max_y: float = 330.0

var move_speed: float = 18.0
var move_direction: Vector2 = Vector2.ZERO
var move_timer: float = 0.0
var anim_timer: float = 0.0
var anim_frame: int = 0

var has_egg: bool = false
var egg_timer: float = 0.0
var is_fed: bool = false
var hunger_timer: float = 0.0
var is_player_nearby: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var emotion: Sprite2D = $EmotionSprite
@onready var egg_bubble: Sprite2D = $EggBubble
@onready var interact_label: Label = $InteractLabel

func _ready() -> void:
	pick_new_direction()
	if emotion:
		emotion.visible = false
	if interact_label:
		interact_label.visible = false
	if animal_type == AnimalType.HEN:
		has_egg = true
		if egg_bubble:
			egg_bubble.visible = true

func _physics_process(delta: float) -> void:
	move_timer -= delta
	if move_timer <= 0:
		pick_new_direction()
	
	if move_direction != Vector2.ZERO:
		velocity = move_direction * move_speed
	else:
		velocity = Vector2.ZERO
	
	move_and_slide()
	
	global_position.x = clamp(global_position.x, min_x, max_x)
	global_position.y = clamp(global_position.y, min_y, max_y)
	
	if sprite and move_direction.x != 0:
		sprite.flip_h = move_direction.x < 0

func _process(delta: float) -> void:
	anim_timer += delta
	if anim_timer >= 0.3:
		anim_timer = 0.0
		anim_frame = (anim_frame + 1) % 3
		update_sprite_region()
	
	# Xử lý đẻ trứng của gà mái (đẻ mỗi 8-10 giây, hoặc 4 giây nếu được cho ăn rơm)
	if animal_type == AnimalType.HEN:
		if has_egg:
			if egg_bubble:
				egg_bubble.visible = true
				egg_bubble.position.y = -20.0 + sin(Time.get_ticks_msec() * 0.007) * 2.0
		else:
			if egg_bubble:
				egg_bubble.visible = false
			var egg_speed = 2.2 if is_fed else 1.0
			egg_timer += delta * egg_speed
			if egg_timer >= 9.0:
				has_egg = true
				egg_timer = 0.0
				if egg_bubble:
					egg_bubble.visible = true
				update_label_text()
	
	if is_fed:
		hunger_timer += delta
		if hunger_timer >= 25.0:
			is_fed = false
			hunger_timer = 0.0

func pick_new_direction() -> void:
	move_timer = randf_range(2.0, 5.0)
	if randf() < 0.45:
		move_direction = Vector2.ZERO
	else:
		var angle = randf() * TAU
		move_direction = Vector2(cos(angle), sin(angle)).normalized()

func update_sprite_region() -> void:
	if not sprite:
		return
	var row = 0
	match animal_type:
		AnimalType.ROOSTER, AnimalType.HEN:
			row = 0
		AnimalType.DUCK:
			row = 1
		AnimalType.PIG:
			row = 2
	sprite.region_rect = Rect2(anim_frame * 32, row * 32, 32, 32)

func interact(tool_id: int, inventory: InventoryData, ui: Node = null) -> bool:
	# 1. Luôn ưu tiên NHẶT TRỨNG trước nếu gà mái đang có trứng
	if animal_type == AnimalType.HEN and has_egg:
		has_egg = false
		if egg_bubble:
			egg_bubble.visible = false
		inventory.add_egg(1)
		show_heart()
		update_label_text()
		if ui and ui.has_method("show_toast"):
			ui.show_toast("🥚 +1 Trứng gà tươi! (Nhiệm vụ: %d/%d)" % [inventory.quest_progress, inventory.quest_target])
		return true
	
	# 2. Cho ăn rơm
	if tool_id == 5:
		if inventory.use_hay():
			is_fed = true
			hunger_timer = 0.0
			egg_timer = 5.0 # Tăng tốc đẻ trứng chỉ trong 4 giây tiếp theo
			show_heart()
			var name_str = _get_name()
			if ui and ui.has_method("show_toast"):
				ui.show_toast("🌿 Đã cho " + name_str + " ăn no rơm! ❤️ (Sẽ mau đẻ trứng)")
			update_label_text()
			return true
		else:
			if ui and ui.has_method("show_toast"):
				ui.show_toast("Hết rơm! Hãy ghé Chợ Quê mua thêm rơm nhé.")
			return false
	
	# 3. Vuốt ve / Thông báo chờ đẻ trứng
	show_heart()
	var name_str = _get_name()
	if ui and ui.has_method("show_toast"):
		if animal_type == AnimalType.HEN:
			ui.show_toast("Gà mái đang ấp, hãy đợi vài giây nữa hoặc cho ăn rơm để đẻ trứng nhé!")
		else:
			ui.show_toast("Vuốt ve " + name_str + " dễ thương! ❤️")
	return true

func _get_name() -> String:
	match animal_type:
		AnimalType.ROOSTER: return "Gà trống"
		AnimalType.HEN: return "Gà mái"
		AnimalType.DUCK: return "Đàn vịt"
		AnimalType.PIG: return "Chú heo"
	return "Vật nuôi"

func show_heart() -> void:
	if not emotion or not is_instance_valid(emotion):
		return
	emotion.visible = true
	emotion.modulate.a = 1.0
	emotion.position = Vector2(0, -18)
	var tween = create_tween()
	tween.tween_property(emotion, "position:y", -28.0, 0.6)
	tween.parallel().tween_property(emotion, "modulate:a", 0.0, 0.6)
	tween.tween_callback(func():
		if is_instance_valid(emotion):
			emotion.visible = false
			emotion.modulate.a = 1.0
			emotion.position = Vector2(0, -18)
	)

func set_nearby(nearby: bool) -> void:
	is_player_nearby = nearby
	if not interact_label:
		return
	interact_label.visible = nearby
	if nearby:
		update_label_text()

func update_label_text() -> void:
	if not interact_label:
		return
	if animal_type == AnimalType.HEN:
		if has_egg:
			interact_label.text = "[E] Nhặt trứng 🥚"
		else:
			interact_label.text = "[E] Cho ăn rơm / Chờ đẻ"
	else:
		interact_label.text = "[E] Cho ăn (Phím 5)"
