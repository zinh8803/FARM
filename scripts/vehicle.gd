extends StaticBody2D
class_name Vehicle

enum VehicleType {
	BICYCLE,   # Xe đạp phượng hoàng
	MOTORBIKE  # Xe máy Super Cub 50
}

@export var vehicle_type: VehicleType = VehicleType.BICYCLE

@onready var sprite: Sprite2D = $Sprite2D
@onready var prompt_label: Label = $PromptLabel
@onready var interact_area: Area2D = $InteractArea

var is_mounted: bool = false

func _ready() -> void:
	update_visuals()
	if prompt_label:
		prompt_label.visible = false

func update_visuals() -> void:
	if not sprite:
		return
	if vehicle_type == VehicleType.BICYCLE:
		sprite.region_rect = Rect2(96, 64, 32, 32)
		if prompt_label:
			prompt_label.text = "[E] Lên xe đạp 🚲"
	else:
		sprite.region_rect = Rect2(96, 192, 32, 32)
		if prompt_label:
			prompt_label.text = "[E] Lên xe máy 🏍️"

func get_vehicle_name() -> String:
	return "Xe đạp phượng hoàng" if vehicle_type == VehicleType.BICYCLE else "Xe máy Super Cub"

func get_speed() -> float:
	return 185.0 if vehicle_type == VehicleType.BICYCLE else 285.0

func interact(player: Node) -> void:
	if is_mounted or not is_instance_valid(player):
		return
	if player.has_method("mount_vehicle"):
		player.mount_vehicle(vehicle_type, self)

func on_mounted() -> void:
	is_mounted = true
	visible = false
	collision_layer = 0
	if prompt_label:
		prompt_label.visible = false

func on_dismounted(spawn_pos: Vector2) -> void:
	is_mounted = false
	global_position = spawn_pos
	visible = true
	collision_layer = 1
	if prompt_label:
		prompt_label.visible = false

func _on_interact_area_body_entered(body: Node2D) -> void:
	if is_mounted:
		return
	if body is Player:
		if prompt_label:
			prompt_label.visible = true
		body.set_nearby_vehicle(self)

func _on_interact_area_body_exited(body: Node2D) -> void:
	if body is Player:
		if prompt_label:
			prompt_label.visible = false
		body.clear_nearby_vehicle(self)
