extends CharacterBody2D
class_name NPCMarket

@export var npc_name: String = "Cô Út (Chợ Quê)"

@onready var interact_label: Label = $InteractLabel

func _ready() -> void:
	if interact_label:
		interact_label.visible = false

func interact(_inventory: InventoryData, ui: Node) -> void:
	if ui and ui.has_method("open_shop"):
		ui.open_shop()
	elif ui and ui.has_method("open_dialogue"):
		ui.open_dialogue(npc_name, "Chào cháu! Ghé tiệm Cô Út mua hạt giống và bán nông sản tươi ngon nhé!")

func set_nearby(nearby: bool) -> void:
	if interact_label:
		interact_label.visible = nearby
