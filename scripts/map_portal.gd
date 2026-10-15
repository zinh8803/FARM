extends Area2D
class_name MapPortal

signal portal_triggered(target_map: String, spawn_point_name: String)

@export_file("*.tscn") var target_map_path: String = ""
@export var target_spawn_name: String = "spawn_default"
@export var portal_prompt: String = "Đi tiếp"
@export var requires_interaction_key: bool = false # Nếu true thì nhấn E, nếu false thì chỉ cần bước vào

var is_player_inside: bool = false
@onready var prompt_label: Label = $PromptLabel

func _ready() -> void:
	if prompt_label:
		prompt_label.text = "[E] " + portal_prompt
		prompt_label.visible = false
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

func _unhandled_input(event: InputEvent) -> void:
	if is_player_inside and requires_interaction_key:
		if event is InputEventKey and event.pressed and not event.echo:
			if event.keycode == KEY_E or event.keycode == KEY_SPACE:
				trigger_portal()

func _on_body_entered(body: Node2D) -> void:
	if body is Player or body.name == "Player":
		is_player_inside = true
		if requires_interaction_key:
			if prompt_label:
				prompt_label.visible = true
		else:
			trigger_portal()

func _on_body_exited(body: Node2D) -> void:
	if body is Player or body.name == "Player":
		is_player_inside = false
		if prompt_label:
			prompt_label.visible = false

func trigger_portal() -> void:
	if target_map_path != "":
		portal_triggered.emit(target_map_path, target_spawn_name)
