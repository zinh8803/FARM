extends NPCVillager
class_name WanderingNPC

@export var wander_radius: Vector2 = Vector2(48, 28)
@export var move_speed: float = 24.0
@export var pause_min: float = 0.6
@export var pause_max: float = 2.0

var home_position: Vector2
var destination: Vector2
var pause_timer: float = 0.0

func _ready() -> void:
	super._ready()
	home_position = position
	_choose_destination()

func _physics_process(delta: float) -> void:
	if pause_timer > 0.0:
		pause_timer -= delta
		velocity = Vector2.ZERO
		return

	var offset := destination - position
	if offset.length() < 4.0:
		_pause_and_turn()
		return

	velocity = offset.normalized() * move_speed
	if sprite:
		sprite.flip_h = velocity.x < 0.0
	move_and_slide()
	if get_slide_collision_count() > 0:
		_pause_and_turn()

func _pause_and_turn() -> void:
	velocity = Vector2.ZERO
	pause_timer = randf_range(pause_min, pause_max)
	_choose_destination()

func _choose_destination() -> void:
	destination = home_position + Vector2(
		randf_range(-wander_radius.x, wander_radius.x),
		randf_range(-wander_radius.y, wander_radius.y)
	)
