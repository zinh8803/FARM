extends Node2D
class_name TrafficManager

@export var car_scene: PackedScene = preload("res://scenes/traffic_car.tscn")
@export var max_active_cars: int = 7

var timer_west: float = 1.0
var timer_east: float = 2.0

@onready var ysort_node: Node2D = get_parent().get_node_or_null("YSort")

func _ready() -> void:
	# Spawn initial cars scattered on the road
	call_deferred("spawn_initial_cars")

func spawn_initial_cars() -> void:
	if not ysort_node or not car_scene:
		return
	
	# Initial Westbound cars (Lane 1, y = 166, direction = -1)
	var west_positions = [350.0, 750.0, 1150.0]
	for x_pos in west_positions:
		spawn_car(-1, 166.0, x_pos + randf_range(-60.0, 60.0))
		
	# Initial Eastbound cars (Lane 2, y = 226, direction = 1)
	var east_positions = [200.0, 600.0, 1000.0]
	for x_pos in east_positions:
		spawn_car(1, 226.0, x_pos + randf_range(-60.0, 60.0))

func _process(delta: float) -> void:
	if not ysort_node or not car_scene:
		return
		
	var valid_cars = 0
	var cars = get_tree().get_nodes_in_group("traffic_car")
	for c in cars:
		if is_instance_valid(c) and not c.is_queued_for_deletion():
			valid_cars += 1
	if valid_cars >= max_active_cars:
		return
		
	# Timer Lane 1 (Westbound - xe chạy sang trái)
	timer_west -= delta
	if timer_west <= 0.0:
		timer_west = randf_range(1.8, 3.8)
		if can_spawn_at(1450.0, 166.0):
			spawn_car(-1, 166.0, 1450.0)
			
	# Timer Lane 2 (Eastbound - xe chạy sang phải)
	timer_east -= delta
	if timer_east <= 0.0:
		timer_east = randf_range(1.8, 3.8)
		if can_spawn_at(-50.0, 226.0):
			spawn_car(1, 226.0, -50.0)

func can_spawn_at(check_x: float, check_y: float) -> bool:
	var cars = get_tree().get_nodes_in_group("traffic_car")
	for c in cars:
		if is_instance_valid(c) and not c.is_queued_for_deletion():
			if abs(c.global_position.y - check_y) < 20.0 and abs(c.global_position.x - check_x) < 110.0:
				return false
	return true

func spawn_car(dir: int, y_pos: float, x_pos: float) -> void:
	if not car_scene or not ysort_node:
		return
	var car = car_scene.instantiate() as TrafficCar
	car.direction = dir
	car.car_type = randi() % 5 # Ngẫu nhiên hoàn toàn 5 loại xe (Taxi xanh, sedan đỏ, van trắng, taxi lục, xe vàng)
	car.speed = randf_range(115.0, 165.0) # Tốc độ ngẫu nhiên
	car.min_x = -70.0
	car.max_x = 1470.0
	car.global_position = Vector2(x_pos, y_pos)
	ysort_node.add_child(car)
