extends CharacterBody2D
class_name Player

enum VehicleMode { NONE, BICYCLE, MOTORBIKE }

@export var base_speed: float = 110.0

var speed: float = 110.0
var current_direction: Vector2 = Vector2.DOWN
var is_moving: bool = false
var anim_frame: int = 0
var anim_timer: float = 0.0
var _last_sprite_region: Rect2 = Rect2()

var vehicle_mode: VehicleMode = VehicleMode.NONE
var mounted_vehicle: Vehicle = null
var nearby_vehicle: Vehicle = null

var nearby_interactable: Node = null
var nearby_interactables: Array[Node2D] = []
var nearby_plots: Array[FarmPlot] = []
var current_target_plot: FarmPlot = null

var inventory: InventoryData
var ui_node: Node
var input_blocked: bool = false

var tex_player = preload("res://assets/sprites/player.png")
var tex_vehicles = preload("res://assets/sprites/vehicles.png")

var speed_buff_multiplier: float = 1.0
var speed_buff_timer: float = 0.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var interact_ray: RayCast2D = $InteractRay

func _ready() -> void:
	add_to_group("player")
	speed = base_speed
	update_sprite()

func setup(inv: InventoryData, ui: Node) -> void:
	inventory = inv
	ui_node = ui

func apply_speed_buff(multiplier: float, duration: float) -> void:
	speed_buff_multiplier = multiplier
	speed_buff_timer = duration

func _physics_process(delta: float) -> void:
	# Update speed buff timer
	if speed_buff_timer > 0.0:
		speed_buff_timer -= delta
		if speed_buff_timer <= 0.0:
			speed_buff_multiplier = 1.0

	# Không cho di chuyển khi hội thoại, tiệm hạt giống hoặc menu túi đồ đang mở
	if input_blocked or (ui_node and ui_node is UIController and (ui_node.is_dialogue_open or ui_node.is_shop_open or ui_node.is_inventory_menu_open)):
		velocity = Vector2.ZERO
		is_moving = false
		anim_frame = 0
		update_sprite()
		return
	
	# 1. Input di chuyển
	var input_vec = Vector2.ZERO
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		input_vec.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		input_vec.x += 1.0
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		input_vec.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		input_vec.y += 1.0

	if input_vec != Vector2.ZERO:
		input_vec = input_vec.normalized()
		velocity = input_vec * (speed * speed_buff_multiplier)
		current_direction = input_vec
		is_moving = true
		
		# Cập nhật hướng tương tác Raycast
		if interact_ray:
			interact_ray.target_position = current_direction * 26.0
	else:
		velocity = Vector2.ZERO
		is_moving = false

	move_and_slide()

	# 2. Xử lý animation di chuyển
	var step_duration = 0.16
	if vehicle_mode == VehicleMode.BICYCLE:
		step_duration = 0.12
	elif vehicle_mode == VehicleMode.MOTORBIKE:
		step_duration = 0.08

	if is_moving:
		anim_timer += delta
		if anim_timer >= step_duration:
			anim_timer = 0.0
			anim_frame = (anim_frame + 1) % 3
	else:
		anim_frame = 0
		anim_timer = 0.0
	
	update_sprite()
	
	# 3. Cập nhật ngắm chuẩn xác ô ruộng theo hướng nhìn (Chỉ khi không lái xe)
	if vehicle_mode == VehicleMode.NONE:
		update_target_plot()
	else:
		clear_target_plot()

func _unhandled_input(event: InputEvent) -> void:
	if input_blocked or (ui_node and ui_node is UIController and (ui_node.is_dialogue_open or ui_node.is_shop_open or ui_node.is_inventory_menu_open)):
		return
	
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: select_tool(1)
			KEY_2: select_tool(2)
			KEY_3: select_tool(3)
			KEY_4: select_tool(4)
			KEY_5: select_tool(5)
			KEY_6: select_tool(6)
			KEY_7: select_tool(7)
			KEY_TAB, KEY_I, KEY_B:
				if ui_node and ui_node.has_method("toggle_inventory_menu"):
					ui_node.toggle_inventory_menu()
			KEY_H, KEY_F:
				honk_vehicle()
			KEY_E, KEY_SPACE:
				if vehicle_mode != VehicleMode.NONE:
					dismount_vehicle()
				elif nearby_vehicle and is_instance_valid(nearby_vehicle):
					nearby_vehicle.interact(self)
				else:
					do_interact()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if vehicle_mode != VehicleMode.NONE:
			return
		do_mouse_interact()

func select_tool(idx: int) -> void:
	if inventory:
		inventory.set_active_tool(idx)

func update_sprite() -> void:
	if not sprite:
		return
	
	var row = 0 # Down
	if abs(current_direction.x) > abs(current_direction.y):
		if current_direction.x < 0:
			row = 2 # Left
		else:
			row = 3 # Right
	else:
		if current_direction.y < 0:
			row = 1 # Up
		else:
			row = 0 # Down
	
	var target_tex = tex_player
	var base_row = row
	
	if vehicle_mode == VehicleMode.BICYCLE:
		target_tex = tex_vehicles
		base_row = row
	elif vehicle_mode == VehicleMode.MOTORBIKE:
		target_tex = tex_vehicles
		base_row = 4 + row
	
	if sprite.texture != target_tex:
		sprite.texture = target_tex
		_last_sprite_region = Rect2()
	
	var new_rect = Rect2(anim_frame * 32, base_row * 32, 32, 32)
	if new_rect != _last_sprite_region:
		sprite.region_rect = new_rect
		_last_sprite_region = new_rect

# -------------------------------------------------------------
# HỆ THỐNG NGẮM & TƯƠNG TÁC CHUẨN XÁC VỚI Ô RUỘNG (KHÔNG LỆCH)
# -------------------------------------------------------------
func update_target_plot() -> void:
	# Lọc bỏ các ô đã bị hủy
	nearby_plots = nearby_plots.filter(func(p): return is_instance_valid(p))
	
	if nearby_plots.is_empty():
		clear_target_plot()
		return
	
	var best_plot: FarmPlot = null
	var min_dist: float = 99999.0
	# Điểm trọng tâm mục tiêu trực tiếp trước mặt theo hướng nhân vật nhìn
	var target_point = global_position + current_direction * 20.0
	
	for plot in nearby_plots:
		var plot_rect = Rect2(plot.global_position, Vector2(32, 32))
		if plot_rect.has_point(target_point):
			best_plot = plot
			break
		var center = plot.global_position + Vector2(16, 16)
		var d = center.distance_to(target_point)
		if d < min_dist and d <= 38.0:
			min_dist = d
			best_plot = plot
	
	if best_plot != current_target_plot:
		if current_target_plot and is_instance_valid(current_target_plot):
			current_target_plot.set_highlight(false)
		current_target_plot = best_plot
		if current_target_plot and is_instance_valid(current_target_plot):
			current_target_plot.set_highlight(true)

func clear_target_plot() -> void:
	if current_target_plot and is_instance_valid(current_target_plot):
		current_target_plot.set_highlight(false)
	current_target_plot = null

func get_best_interactable() -> Node2D:
	var valid_list: Array[Node2D] = []
	for node in nearby_interactables:
		if is_instance_valid(node):
			valid_list.append(node)
	nearby_interactables = valid_list
	
	if nearby_interactables.is_empty():
		return null
	
	# Ưu tiên 1: Gà mái có trứng sẵn để nhặt
	for node in nearby_interactables:
		if node is Animal and node.animal_type == Animal.AnimalType.HEN and node.has_egg:
			return node
	
	# Ưu tiên 2: Con vật hoặc NPC mà người chơi đang nhìn về hướng đó nhất
	var best_node: Node2D = null
	var min_dist: float = 9999.0
	for node in nearby_interactables:
		var d = global_position.distance_to(node.global_position)
		if d < min_dist:
			min_dist = d
			best_node = node
	return best_node

func do_interact() -> void:
	if not inventory:
		return
	
	# 1. Ưu tiên NPC hoặc Thú nuôi trong tầm với (tự động ưu tiên gà có trứng)
	var target_body = get_best_interactable()
	if target_body and is_instance_valid(target_body):
		if target_body is Animal:
			target_body.interact(inventory.active_tool, inventory, ui_node)
			return
		elif not (target_body is FarmPlot) and target_body.has_method("interact"):
			target_body.interact(inventory, ui_node)
			return
	
	if interact_ray and interact_ray.is_colliding():
		var col = interact_ray.get_collider()
		if col and is_instance_valid(col):
			if col is Animal:
				col.interact(inventory.active_tool, inventory, ui_node)
				return
			elif not (col is FarmPlot) and col.has_method("interact"):
				col.interact(inventory, ui_node)
				return

	# 2. Thao tác chính xác trên ô ruộng đang ngắm thẳng mặt (current_target_plot)
	if current_target_plot and is_instance_valid(current_target_plot):
		current_target_plot.interact(inventory.active_tool, inventory, ui_node)
		return
	
	# 3. Sử dụng vật phẩm tiêu thụ (Bắp ngô / Trứng gà) khi đang chọn ô 6 hoặc 7
	if inventory.active_tool == 6:
		if inventory.consume_crop():
			apply_speed_buff(1.3, 30.0)
			if ui_node and ui_node.has_method("show_toast"):
				ui_node.show_toast("🌽 Đã ăn bắp ngô luộc thơm ngon! Tốc độ chạy +30% trong 30s!")
		else:
			if ui_node and ui_node.has_method("show_toast"):
				ui_node.show_toast("Đã hết bắp ngô! Hãy thu hoạch thêm ở ruộng nhé.")
		return
	elif inventory.active_tool == 7:
		if inventory.consume_egg():
			apply_speed_buff(1.25, 25.0)
			if ui_node and ui_node.has_method("show_toast"):
				ui_node.show_toast("🥚 Đã ăn trứng gà bổ dưỡng! Tốc độ chạy +25% trong 25s!")
		else:
			if ui_node and ui_node.has_method("show_toast"):
				ui_node.show_toast("Đã hết trứng gà! Hãy xuống chuồng gà nhặt thêm nhé.")
		return

	# Nếu đứng lệch không quay mặt vào ô đất nào
	if nearby_plots.size() > 0 and ui_node and ui_node.has_method("show_toast"):
		ui_node.show_toast("Hãy quay mặt vào ô đất cần thao tác!")

func do_mouse_interact() -> void:
	if not inventory:
		return
	var mouse_pos = get_global_mouse_position()
	
	# 1. Kiểm tra chuột click trực tiếp vào con vật hoặc NPC trong tầm với (<= 65px)
	for body in nearby_interactables:
		if is_instance_valid(body):
			var b_pos = body.global_position
			if b_pos.distance_to(mouse_pos) <= 24.0 and global_position.distance_to(b_pos) <= 65.0:
				if body is Animal:
					body.interact(inventory.active_tool, inventory, ui_node)
					return
				elif body.has_method("interact"):
					body.interact(inventory, ui_node)
					return
	
	# 2. Kiểm tra xem chuột click vào ô đất nào trong tầm với (<= 52 px)
	for plot in nearby_plots:
		if not is_instance_valid(plot):
			continue
		var plot_rect = Rect2(plot.global_position, Vector2(32, 32))
		if plot_rect.has_point(mouse_pos) and global_position.distance_to(plot.global_position + Vector2(16, 16)) <= 52.0:
			plot.interact(inventory.active_tool, inventory, ui_node)
			return
	
	# Nếu click không vào ô đất thì tương tác theo hướng nhìn
	do_interact()

# -------------------------------------------------------------
# HỆ THỐNG PHƯƠNG TIỆN (XE ĐẠP & XE MÁY)
# -------------------------------------------------------------
func set_nearby_vehicle(veh: Vehicle) -> void:
	nearby_vehicle = veh

func clear_nearby_vehicle(veh: Vehicle) -> void:
	if nearby_vehicle == veh:
		nearby_vehicle = null

func mount_vehicle(type: Vehicle.VehicleType, veh: Vehicle) -> void:
	mounted_vehicle = veh
	if mounted_vehicle.get_parent():
		mounted_vehicle.get_parent().remove_child(mounted_vehicle)
	add_child(mounted_vehicle) # Giữ xe cùng Player khi chuyển map
	
	if type == Vehicle.VehicleType.BICYCLE:
		vehicle_mode = VehicleMode.BICYCLE
		speed = 185.0
		if ui_node and ui_node.has_method("show_toast"):
			ui_node.show_toast("🚲 Đã lên xe đạp! [E: Xuống xe | H: Kính coong]")
	else:
		vehicle_mode = VehicleMode.MOTORBIKE
		speed = 285.0
		if ui_node and ui_node.has_method("show_toast"):
			ui_node.show_toast("🏍️ Đã nổ máy xe Super Cub! [E: Xuống xe | H: Bấm còi]")
	
	veh.on_mounted()
	clear_target_plot()
	update_sprite()

func dismount_vehicle() -> void:
	if vehicle_mode == VehicleMode.NONE:
		return
	
	var drop_pos = global_position
	if mounted_vehicle and is_instance_valid(mounted_vehicle):
		remove_child(mounted_vehicle)
		var map_parent = get_parent()
		if map_parent:
			map_parent.add_child(mounted_vehicle)
		mounted_vehicle.on_dismounted(drop_pos)
		mounted_vehicle = null
	
	vehicle_mode = VehicleMode.NONE
	speed = base_speed
	update_sprite()
	if ui_node and ui_node.has_method("show_toast"):
		ui_node.show_toast("🚶 Đã xuống xe, tiếp tục đi bộ!")

func honk_vehicle() -> void:
	if vehicle_mode == VehicleMode.BICYCLE:
		if ui_node and ui_node.has_method("show_toast"):
			ui_node.show_toast("🔔 Kính coong! Kính coong! Xe đạp xin đường!")
	elif vehicle_mode == VehicleMode.MOTORBIKE:
		if ui_node and ui_node.has_method("show_toast"):
			ui_node.show_toast("🏍️ Bíp bíp! Xe máy bon bon vi vu khắp đường làng quê!")

# -------------------------------------------------------------
# TƯƠNG TÁC KHU VỰC AREA & BODY
# -------------------------------------------------------------
func _on_interaction_area_entered(area: Area2D) -> void:
	if area is FarmPlot:
		if not nearby_plots.has(area):
			nearby_plots.append(area)

func _on_interaction_area_exited(area: Area2D) -> void:
	if area is FarmPlot:
		if area == current_target_plot:
			area.set_highlight(false)
			current_target_plot = null
		nearby_plots.erase(area)

func _on_body_interaction_entered(body: Node2D) -> void:
	if input_blocked:
		return
	if body is Animal or body.has_method("interact"):
		if not nearby_interactables.has(body):
			nearby_interactables.append(body)
		nearby_interactable = get_best_interactable()
		if body.has_method("set_nearby"):
			body.set_nearby(true)

func _on_body_interaction_exited(body: Node2D) -> void:
	if nearby_interactables.has(body):
		nearby_interactables.erase(body)
	if body.has_method("set_nearby"):
		body.set_nearby(false)
	nearby_interactable = get_best_interactable()
	if nearby_interactable and nearby_interactable.has_method("set_nearby"):
		nearby_interactable.set_nearby(true)
