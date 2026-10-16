extends Node2D
class_name FishingAnimation

var animation_state: String = "hidden"
var target_local_position: Vector2 = Vector2.ZERO
var animation_time: float = 0.0
var fish_biting: bool = false

func start_cast(target_global_position: Vector2) -> void:
	target_local_position = get_parent().to_local(target_global_position)
	animation_state = "cast"
	animation_time = 0.0
	fish_biting = false
	visible = true
	queue_redraw()

func set_bite(active: bool) -> void:
	fish_biting = active
	queue_redraw()

func finish_cast(caught: bool, cancelled: bool = false) -> void:
	if cancelled:
		animation_state = "hidden"
		visible = false
		queue_redraw()
		return
	animation_state = "catch" if caught else "reel"
	animation_time = 0.0
	fish_biting = false
	queue_redraw()

func _process(delta: float) -> void:
	if animation_state == "hidden":
		return
	animation_time += delta
	if animation_state == "cast" and animation_time >= 0.48:
		animation_state = "wait"
		animation_time = 0.0
	elif (animation_state == "catch" or animation_state == "reel") and animation_time >= 0.72:
		animation_state = "hidden"
		visible = false
	queue_redraw()

func _draw() -> void:
	if animation_state == "hidden":
		return
	var player := get_parent()
	var facing: Vector2 = Vector2.DOWN
	var parent_direction = player.get("current_direction")
	if parent_direction is Vector2:
		facing = parent_direction.normalized()
	if facing == Vector2.ZERO:
		facing = Vector2.DOWN
	var side := Vector2(-facing.y, facing.x)
	var hand: Vector2 = facing * 3.0 + Vector2(0.0, -4.0)
	var rod_tip: Vector2 = hand + facing * 23.0 + side * 7.0
	var bobber_position: Vector2 = target_local_position

	if animation_state == "cast":
		var cast_progress: float = clampf(animation_time / 0.48, 0.0, 1.0)
		var eased_progress: float = 1.0 - pow(1.0 - cast_progress, 2.0)
		bobber_position = rod_tip.lerp(target_local_position, eased_progress)
		bobber_position.y -= sin(cast_progress * PI) * 36.0
	elif animation_state == "reel":
		var reel_progress: float = clampf(animation_time / 0.72, 0.0, 1.0)
		bobber_position = target_local_position.lerp(rod_tip, reel_progress)
	elif animation_state == "catch":
		var catch_progress: float = clampf(animation_time / 0.72, 0.0, 1.0)
		var fish_position: Vector2 = target_local_position.lerp(hand, catch_progress)
		fish_position.y -= sin(catch_progress * PI) * 52.0
		bobber_position = fish_position
		_draw_fish(fish_position, side)

	var rod_color := Color(0.37, 0.2, 0.1, 1)
	draw_line(hand - side * 5.0, rod_tip, rod_color, 3.0, true)
	draw_line(rod_tip, bobber_position, Color(0.96, 0.94, 0.82, 0.88), 1.2, true)

	if animation_state != "catch":
		var bobber_bob: float = sin(animation_time * 4.0) * 2.0
		if fish_biting:
			bobber_bob += sin(animation_time * 26.0) * 5.0
		var bobber_draw_position: Vector2 = bobber_position + Vector2(0.0, bobber_bob)
		draw_circle(bobber_draw_position, 4.5, Color(0.96, 0.9, 0.75, 1))
		draw_circle(bobber_draw_position + Vector2(0.0, -1.0), 2.2, Color(0.92, 0.2, 0.16, 1))
		if animation_state == "wait" and not fish_biting:
			var ripple_size: float = 7.0 + fposmod(animation_time * 8.0, 8.0)
			draw_arc(bobber_draw_position + Vector2(0.0, 3.0), ripple_size, 0.0, TAU, 24, Color(0.75, 0.94, 1.0, 0.55), 1.0, true)
		elif fish_biting:
			draw_arc(bobber_draw_position, 10.0, 0.0, TAU, 24, Color(1.0, 0.88, 0.34, 0.9), 2.0, true)

func _draw_fish(fish_position: Vector2, side: Vector2) -> void:
	var body := PackedVector2Array([
		fish_position + side * -8.0,
		fish_position + Vector2(0.0, -4.0),
		fish_position + side * 8.0,
		fish_position + Vector2(0.0, 4.0)
	])
	draw_colored_polygon(body, Color(0.83, 0.68, 0.34, 1))
	draw_circle(fish_position + side * 4.0, 1.2, Color(0.08, 0.13, 0.16, 1))
