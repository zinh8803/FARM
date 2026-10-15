extends Node2D
class_name RaceHorse

@export var horse_name: String = "Ngựa đua"
@export var coat_color: Color = Color(0.55, 0.3, 0.16, 1)
@export var jockey_color: Color = Color(0.8, 0.2, 0.16, 1)
@export var track_center: Vector2 = Vector2(500, 300)
@export var track_radius: Vector2 = Vector2(330, 170)
@export var race_speed: float = 0.6
@export var phase_offset: float = 0.0

var phase: float = 0.0
var animation_time: float = 0.0

func _ready() -> void:
	phase = phase_offset
	_update_race_position()

func _process(delta: float) -> void:
	phase = fposmod(phase + race_speed * delta, TAU)
	animation_time += delta
	_update_race_position()
	queue_redraw()

func _update_race_position() -> void:
	position = track_center + Vector2(
		cos(phase) * track_radius.x,
		sin(phase) * track_radius.y
	)
	var tangent := Vector2(
		-sin(phase) * track_radius.x,
		cos(phase) * track_radius.y
	)
	rotation = tangent.angle()

func _draw() -> void:
	var gallop := sin(animation_time * 15.0)
	var leg_color := coat_color.darkened(0.35)
	draw_colored_polygon(PackedVector2Array([
		Vector2(-16, -5), Vector2(-10, -10), Vector2(5, -9),
		Vector2(15, -3), Vector2(13, 6), Vector2(-10, 7)
	]), coat_color)
	draw_colored_polygon(PackedVector2Array([
		Vector2(5, -7), Vector2(11, -15), Vector2(17, -18),
		Vector2(21, -15), Vector2(15, -10), Vector2(12, -2)
	]), coat_color)
	draw_circle(Vector2(20, -16), 4.0, coat_color.lightened(0.1))
	draw_line(Vector2(-15, -4), Vector2(-23, -10 + gallop * 2.0), leg_color, 2.5)
	for leg in [-1.0, 1.0]:
		var stride: float = gallop * 4.0 * float(leg)
		draw_line(Vector2(-8, 5), Vector2(-9 + stride, 15), leg_color, 2.5)
		draw_line(Vector2(8, 5), Vector2(9 - stride, 15), leg_color, 2.5)
	draw_circle(Vector2(-1, -12), 5.0, jockey_color)
	draw_line(Vector2(-1, -8), Vector2(3, -3), jockey_color, 4.0)
