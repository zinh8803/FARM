extends CharacterBody2D
class_name FishingSpot

@export var spot_name: String = "Bãi câu"
@export var cast_direction: Vector2 = Vector2.LEFT
@export var cast_distance: float = 96.0

@onready var interact_label: Label = $InteractLabel

func _ready() -> void:
	if interact_label:
		interact_label.visible = false

func interact(_inventory: InventoryData, ui: Node) -> void:
	if ui and ui.has_method("start_fishing"):
		ui.start_fishing(global_position + cast_direction.normalized() * cast_distance)

func set_nearby(nearby: bool) -> void:
	if interact_label:
		interact_label.visible = nearby

func _draw() -> void:
	draw_circle(Vector2.ZERO, 11.0, Color(0.2, 0.56, 0.72, 0.85))
	draw_arc(Vector2.ZERO, 8.0, 0.0, TAU, 24, Color(0.7, 0.94, 1.0, 0.9), 1.5)
