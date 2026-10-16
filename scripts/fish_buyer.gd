extends NPCVillager
class_name FishBuyer

func interact(_inventory: InventoryData, ui: Node) -> void:
	if ui and ui.has_method("open_fish_shop"):
		ui.open_fish_shop()
