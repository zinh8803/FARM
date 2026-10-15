extends BaseMap
class_name RiceFieldMap

const FARM_PLOT_SCENE: PackedScene = preload("res://scenes/farm_plot.tscn")

func _ready() -> void:
	super._ready()
	var plots_root := get_node_or_null("FarmPlots") as Node2D
	if plots_root == null:
		return

	# Ruộng lúa chín sẵn để người chơi có thể thu hoạch và trồng lại.
	for row in range(5):
		for col in range(9):
			var plot := FARM_PLOT_SCENE.instantiate() as FarmPlot
			plot.position = Vector2(94 + col * 36, 76 + row * 36)
			plot.grid_x = col
			plot.grid_y = row
			plot.crop_type = FarmPlot.CropType.RICE
			plot.state = FarmPlot.State.MATURE
			plots_root.add_child(plot)
