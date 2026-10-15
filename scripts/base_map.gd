extends Node2D
class_name BaseMap

signal change_map_requested(target_map_path: String, spawn_point_name: String)

@export var map_title: String = "Bản đồ"
@export var default_spawn_name: String = "spawn_default"
@export var map_width: float = 640.0
@export var map_height: float = 360.0

func _ready() -> void:
	# Tự động tìm và kết nối tất cả các MapPortal trong map
	connect_portals_recursive(self)

func connect_portals_recursive(node: Node) -> void:
	for child in node.get_children():
		if child is MapPortal:
			child.portal_triggered.connect(_on_portal_triggered)
		connect_portals_recursive(child)

func _on_portal_triggered(target_map: String, spawn_name: String) -> void:
	change_map_requested.emit(target_map, spawn_name)

func get_spawn_position(spawn_name: String) -> Vector2:
	var spawn_node = find_child(spawn_name, true, false)
	if spawn_node and spawn_node is Marker2D:
		return spawn_node.global_position
	var default_node = find_child(default_spawn_name, true, false)
	if default_node and default_node is Marker2D:
		return default_node.global_position
	return Vector2(240, 160)
