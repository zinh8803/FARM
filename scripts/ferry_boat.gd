extends Node2D
class_name FerryBoat

@export var boat_name: String = "Thuyền"
@export var boat_color: Color = Color(0.88, 0.3, 0.18, 1)
@export var travel_speed: float = 42.0
@export var left_limit: float = -70.0
@export var right_limit: float = 1470.0

func _process(delta: float) -> void:
	position.x += travel_speed * delta
	if travel_speed >= 0.0 and position.x > right_limit:
		position.x = left_limit
	elif travel_speed < 0.0 and position.x < left_limit:
		position.x = right_limit
	queue_redraw()

func _draw() -> void:
	var direction: float = 1.0 if travel_speed >= 0.0 else -1.0
	var hull: PackedVector2Array
	if direction > 0.0:
		hull = PackedVector2Array([
			Vector2(-24.0, -2.0), Vector2(23.0, -2.0),
			Vector2(16.0, 10.0), Vector2(-15.0, 10.0)
		])
	else:
		hull = PackedVector2Array([
			Vector2(24.0, -2.0), Vector2(-23.0, -2.0),
			Vector2(-16.0, 10.0), Vector2(15.0, 10.0)
		])
	draw_colored_polygon(hull, boat_color)
	draw_rect(Rect2(-8.0 * direction, -13.0, 17.0, 11.0), Color(0.92, 0.88, 0.72, 1))
	draw_rect(Rect2(-4.0 * direction, -12.0, 7.0, 5.0), Color(0.28, 0.72, 0.88, 1))
	draw_line(Vector2(-31.0 * direction, 14.0), Vector2(29.0 * direction, 14.0), Color(0.78, 0.94, 1.0, 0.72), 2.0)
	draw_line(Vector2(-25.0 * direction, 18.0), Vector2(21.0 * direction, 18.0), Color(0.78, 0.94, 1.0, 0.45), 1.5)
