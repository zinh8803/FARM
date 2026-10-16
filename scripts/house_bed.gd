extends StaticBody2D
class_name HouseBed

@export var prompt_message: String = "Đi ngủ qua đêm (Tự động lưu game) [E]"

func interact(_inv: InventoryData, ui: Node) -> void:
	var tree = get_tree()
	if not tree:
		return
	var main_node = tree.root.find_child("Main", true, false)
	if not main_node:
		main_node = tree.current_scene
		
	if main_node and main_node.has_method("sleep_and_save"):
		main_node.call("sleep_and_save")
	elif ui and ui.has_method("show_toast"):
		ui.show_toast("😴 Bạn đã ngủ một giấc say sưa đến sáng mai!")

func _on_area_2d_body_entered(body: Node2D) -> void:
	if body is Player and not body.nearby_interactables.has(self):
		body.nearby_interactables.append(self)
		if body.ui_node and body.ui_node.has_method("show_toast"):
			body.ui_node.show_toast("🛏️ Nhấn [E] hoặc [Space] để đi ngủ & Lưu tiến độ ngày!")

func _on_area_2d_body_exited(body: Node2D) -> void:
	if body is Player:
		body.nearby_interactables.erase(self)
