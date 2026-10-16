extends Control

var status_text: String = ""
var marker_position: float = 0.0
var target_start: float = 0.4
var target_width: float = 0.2

func set_gauge(status: String, marker: float, target: float, width: float) -> void:
	status_text = status
	marker_position = clampf(marker, 0.0, 1.0)
	target_start = clampf(target, 0.0, 1.0)
	target_width = clampf(width, 0.05, 0.5)
	queue_redraw()

func _draw() -> void:
	var panel_rect := Rect2(Vector2.ZERO, size)
	draw_rect(panel_rect, Color(0.08, 0.16, 0.2, 0.94), true)
	draw_rect(panel_rect, Color(0.86, 0.73, 0.42, 1), false, 3.0)
	var font := get_theme_default_font()
	if font == null:
		return
	draw_string(font, Vector2(12, 15), "🎣 CÂU CÁ", HORIZONTAL_ALIGNMENT_LEFT, size.x - 24, 9, Color(1.0, 0.86, 0.45, 1))
	draw_string(font, Vector2(12, 29), status_text, HORIZONTAL_ALIGNMENT_LEFT, size.x - 24, 8, Color(0.94, 0.96, 0.9, 1))
	var bar := Rect2(12.0, 35.0, size.x - 24.0, 16.0)
	draw_rect(bar, Color(0.08, 0.1, 0.12, 1), true)
	if status_text.begins_with("CÁ CẮN"):
		var zone_x: float = bar.position.x + target_start * bar.size.x
		var zone_w: float = target_width * bar.size.x
		draw_rect(Rect2(zone_x, bar.position.y + 1.0, zone_w, bar.size.y - 2.0), Color(0.27, 0.78, 0.42, 1), true)
		var marker_x: float = bar.position.x + marker_position * bar.size.x
		draw_rect(Rect2(marker_x - 2.0, bar.position.y - 3.0, 4.0, bar.size.y + 6.0), Color(1.0, 0.88, 0.32, 1), true)
	else:
		draw_rect(Rect2(bar.position.x + 3.0, bar.position.y + 3.0, bar.size.x - 6.0, bar.size.y - 6.0), Color(0.2, 0.58, 0.76, 1), true)
	draw_string(font, Vector2(12, 67), "SPACE / E khi kim vào vùng xanh", HORIZONTAL_ALIGNMENT_CENTER, size.x - 24, 7, Color(0.84, 0.9, 0.92, 1))
