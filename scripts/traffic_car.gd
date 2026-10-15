extends CharacterBody2D
class_name TrafficCar

@export var direction: int = 1 # 1: Eastbound (Right), -1: Westbound (Left)
@export var speed: float = 130.0
@export var car_type: int = 0 # 0..4 (Blue Taxi, Red Sedan, White Van, Green Taxi, Yellow)
@export var min_x: float = -70.0
@export var max_x: float = 1470.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var horn_label: Label = $HornLabel
@onready var front_detector: Area2D = $FrontDetector

var base_speed: float = 130.0
var current_speed: float = 130.0
var honk_timer: float = 0.0
var is_blocked: bool = false
var bob_time: float = 0.0
var life_timer: float = 0.0
var lane_y: float = 0.0
var min_front_dist: float = 999.0

func _ready() -> void:
	lane_y = global_position.y
	base_speed = speed + randf_range(-15.0, 20.0)
	current_speed = base_speed
	update_appearance()
	if horn_label:
		horn_label.visible = false

func update_appearance() -> void:
	if not sprite:
		return
	# Row 0 = Facing East (Right), Row 1 = Facing West (Left)
	var row = 0 if direction > 0 else 1
	var col = car_type % 5
	sprite.region_rect = Rect2(col * 72, row * 36, 72, 36)
	
	# Adjust FrontDetector orientation to point ahead in driving direction
	if front_detector:
		front_detector.position.x = 45.0 * direction

func _physics_process(delta: float) -> void:
	life_timer += delta
	# Failsafe: nếu xe chạy quá 35s (ví dụ bị kẹt kéo dài), tự động giải phóng
	if life_timer > 35.0:
		queue_free()
		return

	# Kiểm tra vật cản phía trước trên cùng làn đường
	check_front_obstacles()
	
	if is_blocked:
		# Khoảng cách an toàn giữa 2 xe:
		# Chiều dài xe khoảng 72px (tâm-tâm = 72px khi chạm sát nhau).
		# Khi khoảng cách <= 84px (còn hở ~12px giữa 2 đầu xe): DỪNG HẲN (speed = 0) để không bao giờ đè lên nhau!
		if min_front_dist <= 84.0:
			current_speed = move_toward(current_speed, 0.0, 500.0 * delta)
			if current_speed < 8.0:
				current_speed = 0.0
		elif min_front_dist <= 120.0:
			var ratio = (min_front_dist - 84.0) / (120.0 - 84.0)
			var safe_speed = base_speed * ratio * 0.35
			current_speed = move_toward(current_speed, safe_speed, 350.0 * delta)
		else:
			current_speed = move_toward(current_speed, base_speed * 0.5, 200.0 * delta)
		
		honk_timer -= delta
		if honk_timer <= 0.0:
			trigger_honk()
			honk_timer = 2.5
	else:
		current_speed = move_toward(current_speed, base_speed, 110.0 * delta)
	
	velocity = Vector2(direction * current_speed, 0.0)
	move_and_slide()
	
	# Khóa cứng tọa độ Y theo đúng làn đường để xe không bao giờ bị lệch hay trượt làn
	if lane_y != 0.0:
		global_position.y = lane_y
	
	# Subtle chassis vibration when driving
	if current_speed > 5.0:
		bob_time += delta * 12.0
		if sprite:
			sprite.position.y = -18.0 + sin(bob_time) * 0.4
	
	# Khi xe đi hết map thì tự động biến mất và giải phóng bộ nhớ
	if direction > 0 and global_position.x >= max_x:
		queue_free()
	elif direction < 0 and global_position.x <= min_x:
		queue_free()

func check_front_obstacles() -> void:
	if not front_detector:
		return
	var bodies = front_detector.get_overlapping_bodies()
	is_blocked = false
	min_front_dist = 999.0
	
	for body in bodies:
		if body == self:
			continue
		# Chỉ xét vật cản cùng làn (độ lệch trục Y <= 26px)
		if abs(body.global_position.y - global_position.y) > 26.0:
			continue
		
		# Khoảng cách phía trước theo hướng xe chạy
		var forward_dist = (body.global_position.x - global_position.x) * direction
		if forward_dist > 0.0 and forward_dist < min_front_dist:
			if body.is_in_group("player") or body.is_in_group("vehicle") or body is TrafficCar:
				is_blocked = true
				min_front_dist = forward_dist

func trigger_honk() -> void:
	if not horn_label:
		return
	horn_label.text = "📢 BÍP BÍP!" if randf() > 0.3 else "🚗 Nhường đường nghen!"
	horn_label.visible = true
	var tw = create_tween()
	horn_label.scale = Vector2(0.5, 0.5)
	horn_label.modulate.a = 1.0
	tw.tween_property(horn_label, "scale", Vector2(1.0, 1.0), 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_interval(1.2)
	tw.tween_property(horn_label, "modulate:a", 0.0, 0.3)
	tw.tween_callback(func(): horn_label.visible = false)

func respawn_west() -> void:
	global_position.x = min_x - randf_range(40.0, 180.0)
	car_type = randi() % 5
	base_speed = randf_range(110.0, 160.0)
	current_speed = base_speed
	update_appearance()

func respawn_east() -> void:
	global_position.x = max_x + randf_range(40.0, 180.0)
	car_type = randi() % 5
	base_speed = randf_range(110.0, 160.0)
	current_speed = base_speed
	update_appearance()
