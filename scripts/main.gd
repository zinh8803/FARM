extends Node2D

@onready var game_settings: GameSettings = $GameSettings
@onready var audio_manager: AudioManagerClass = $AudioManager
@onready var time_system: TimeSystem = $TimeSystem
@onready var inventory: InventoryData = $InventoryData
@onready var canvas_modulate: CanvasModulate = $DayNightLight
@onready var ui: UIController = $UI
@onready var home_menu: HomeMenu = $HomeMenu
@onready var map_container: Node2D = $MapContainer
@onready var transition_rect: ColorRect = $TransitionLayer/TransitionRect

var player_scene = preload("res://scenes/player.tscn")
var farm_plot_scene = preload("res://scenes/farm_plot.tscn")
var player_instance: Player = null
var current_map: BaseMap = null
var is_transitioning: bool = false
var is_in_home_menu: bool = true

const SAVE_PATH = "user://save_data.json"

# Lưu trạng thái 32 ô ruộng để giữ nguyên tiến độ trồng trọt khi di chuyển qua các map khác
var saved_plots_data: Array = []
var rain_particles: CPUParticles2D = null
var rain_timer: float = 0.0

func _ready() -> void:
	# 1. Kết nối hệ thống UI và Inventory
	ui.setup(inventory)
	ui.menu_button_pressed.connect(_on_menu_button_pressed)
	
	# 2. Tạo nhân vật người chơi
	player_instance = player_scene.instantiate()
	player_instance.setup(inventory, ui)
	
	# 3. Tạo hiệu ứng mưa rào thời tiết thực tế
	setup_rain_particles()
	
	# 4. Áp dụng cấu hình ban đầu
	if game_settings:
		game_settings.settings_changed.connect(_on_settings_changed)
		if audio_manager:
			audio_manager.set_sound_enabled(game_settings.sound_enabled)
		if time_system:
			time_system.set_weather_enabled(game_settings.weather_enabled)
			time_system.set_day_night_enabled(game_settings.day_night_enabled)
	
	# 5. Kết nối hệ thống thời gian & thời tiết thực tế
	time_system.time_changed.connect(ui.update_time_display)
	time_system.light_changed.connect(_on_light_changed)
	time_system.weather_changed.connect(_on_weather_changed)
	time_system.emit_time_signals()
	
	# 6. Kết nối Home Menu
	home_menu.play_game_pressed.connect(_on_play_game_pressed)
	home_menu.new_game_pressed.connect(_on_new_game_pressed)
	
	# 7. Khởi tạo map nền
	var direct_play = false
	if OS.get_cmdline_args().has("--city"):
		load_map("res://scenes/maps/modern_city.tscn", "spawn_from_bamboo", false)
		direct_play = true
	elif OS.get_cmdline_args().has("--sky"):
		load_map("res://scenes/maps/modern_city.tscn", "spawn_from_skyscraper", false)
		direct_play = true
	elif OS.get_cmdline_args().has("--bamboo"):
		load_map("res://scenes/maps/bamboo_forest.tscn", "spawn_south", false)
		direct_play = true
	elif OS.get_cmdline_args().has("--bank-interior"):
		load_map("res://scenes/maps/city_bank_interior.tscn", "spawn_entrance", false)
		direct_play = true
	elif OS.get_cmdline_args().has("--sky-interior"):
		load_map("res://scenes/maps/city_skyscraper_interior.tscn", "spawn_entrance", false)
		direct_play = true
	elif OS.get_cmdline_args().has("--mart-interior"):
		load_map("res://scenes/maps/city_mart_interior.tscn", "spawn_entrance", false)
		direct_play = true
	elif OS.get_cmdline_args().has("--villa-interior"):
		load_map("res://scenes/maps/city_villa_interior.tscn", "spawn_entrance", false)
		direct_play = true
	else:
		load_map("res://scenes/maps/farm_map.tscn", "spawn_default", false)
	
	# 8. Mặc định khởi động vào Màn hình Trang Chủ
	if direct_play and not OS.get_cmdline_args().has("--home"):
		is_in_home_menu = false
		home_menu.close_menu()
		ui.set_hud_visible(true)
		player_instance.input_blocked = false
	else:
		is_in_home_menu = true
		player_instance.input_blocked = true
		ui.set_hud_visible(false)
		home_menu.setup(game_settings, audio_manager, has_save_game())
		home_menu.open_menu()

	if OS.get_cmdline_args().has("--screenshot-settings"):
		home_menu.settings_panel.visible = true
		capture_screen()
	elif OS.get_cmdline_args().has("--screenshot-update"):
		home_menu.update_panel.visible = true
		capture_screen()
	elif OS.get_cmdline_args().has("--screenshot"):
		capture_screen()

func _process(delta: float) -> void:
	# Nếu tính năng thời tiết bật và trời đang mưa thực tế thì tự động tưới nước
	if game_settings and game_settings.weather_enabled and time_system and time_system.is_raining:
		rain_timer += delta
		if rain_timer >= 4.0:
			rain_timer = 0.0
			auto_water_farm_plots()

# -------------------------------------------------------------
# QUẢN LÝ HOME MENU & TRẠNG THÁI GAME
# -------------------------------------------------------------
func _on_play_game_pressed() -> void:
	is_in_home_menu = false
	
	if has_save_game():
		load_saved_game()
	
	home_menu.close_menu()
	ui.set_hud_visible(true)
	if player_instance:
		player_instance.input_blocked = false
	ui.show_toast("🌾 Chào mừng bạn đến với Nông Trại Little DaNang!")

func _on_new_game_pressed() -> void:
	is_in_home_menu = false
	reset_to_new_game()
	home_menu.close_menu()
	ui.set_hud_visible(true)
	if player_instance:
		player_instance.input_blocked = false
	ui.show_toast("🌱 Bắt đầu hành trình khởi nghiệp nhà nông mới!")

func _on_menu_button_pressed() -> void:
	if not is_in_home_menu:
		save_game()
		is_in_home_menu = true
		if player_instance:
			player_instance.input_blocked = true
		ui.set_hud_visible(false)
		home_menu.setup(game_settings, audio_manager, true)
		home_menu.open_menu()

func _on_settings_changed() -> void:
	if not game_settings:
		return
	if audio_manager:
		audio_manager.set_sound_enabled(game_settings.sound_enabled)
	if time_system:
		time_system.set_weather_enabled(game_settings.weather_enabled)
		time_system.set_day_night_enabled(game_settings.day_night_enabled)
	update_indoor_outdoor_environment()

func sleep_and_save() -> void:
	if is_transitioning:
		return
	is_transitioning = true
	if player_instance:
		player_instance.input_blocked = true
	
	if transition_rect:
		var tween = create_tween()
		tween.tween_property(transition_rect, "color:a", 1.0, 0.4)
		await tween.finished
	
	# Tua thời gian sang 06:00 sáng ngày hôm sau
	if time_system:
		time_system.current_hour = 6
		time_system.current_minute = 0
		time_system.current_day_num += 1
		time_system.emit_time_signals()
	
	# Ruộng đất khô được tưới hoặc hoa màu lớn lên
	if current_map and current_map.name == "FarmMap":
		save_farm_plots_state()
	for p_data in saved_plots_data:
		if p_data is Dictionary:
			var st = int(p_data.get("state", 0))
			if st == 3: # SEEDED -> GROWING
				p_data["state"] = 4
				p_data["growth_time"] = 15.0
			elif st == 4: # GROWING -> MATURE
				p_data["state"] = 5
				p_data["growth_time"] = 30.0
	
	# Tự động lưu game
	save_game(true)
	
	if audio_manager and time_system:
		audio_manager.update_ambient(6, false)
	
	await get_tree().create_timer(0.6).timeout
	
	if transition_rect:
		var tween_out = create_tween()
		tween_out.tween_property(transition_rect, "color:a", 0.0, 0.4)
		await tween_out.finished
	
	is_transitioning = false
	if player_instance:
		player_instance.input_blocked = false
	if ui:
		ui.show_toast("🌅 Chào buổi sáng ngày mới! Nông sản đã phát triển thêm.")

# -------------------------------------------------------------
# LƯU TRỮ VÀ TẢI TIẾN TRÌNH CHƠI (SAVE / LOAD)
# -------------------------------------------------------------
func has_save_game() -> bool:
	return FileAccess.file_exists(SAVE_PATH)

func save_game(is_sleep_save: bool = false) -> void:
	if current_map and current_map.name == "FarmMap":
		save_farm_plots_state()
	
	var data = {
		"version": 2,
		"coins": inventory.coins if inventory else 150,
		"seeds": inventory.seeds if inventory else 10,
		"crops_harvested": inventory.crops_harvested if inventory else 0,
		"eggs_collected": inventory.eggs_collected if inventory else 0,
		"fish_caught": inventory.fish_caught if inventory else 0,
		"hay_bundles": inventory.hay_bundles if inventory else 5,
		"active_tool": inventory.active_tool if inventory else 1,
		"current_quest_id": inventory.current_quest_id if inventory else 1,
		"quest_progress": inventory.quest_progress if inventory else 0,
		"quest_target": inventory.quest_target if inventory else 4,
		"current_outfit": player_instance.current_outfit if player_instance else 0,
		"current_map_path": current_map.scene_file_path if (current_map and current_map.scene_file_path != "") else "res://scenes/maps/farm_map.tscn",
		"player_pos_x": player_instance.global_position.x if player_instance else 240.0,
		"player_pos_y": player_instance.global_position.y if player_instance else 220.0,
		"plots_data": saved_plots_data
	}
	
	var f = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(data, "  "))
		f.close()
	if is_sleep_save and ui:
		ui.show_toast("💾 Đã tự động lưu dữ liệu nông trại sau khi ngủ qua đêm!")

func load_saved_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	
	var f = FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not f:
		return false
	var text = f.get_as_text()
	f.close()
	
	var json = JSON.new()
	if json.parse(text) != OK:
		return false
	var data = json.get_data()
	if not data is Dictionary:
		return false
	
	if inventory:
		inventory.coins = int(data.get("coins", 150))
		inventory.seeds = int(data.get("seeds", 10))
		inventory.crops_harvested = int(data.get("crops_harvested", 0))
		inventory.eggs_collected = int(data.get("eggs_collected", 0))
		inventory.fish_caught = int(data.get("fish_caught", 0))
		inventory.hay_bundles = int(data.get("hay_bundles", 5))
		inventory.active_tool = int(data.get("active_tool", 1))
		inventory.current_quest_id = int(data.get("current_quest_id", 1))
		inventory.quest_progress = int(data.get("quest_progress", 0))
		inventory.quest_target = int(data.get("quest_target", 4))
		inventory.inventory_changed.emit()
	
	saved_plots_data = data.get("plots_data", [])
	
	var saved_outfit = int(data.get("current_outfit", 0))
	if player_instance:
		player_instance.set_outfit(saved_outfit)
	
	var target_map = str(data.get("current_map_path", "res://scenes/maps/farm_map.tscn"))
	var px = float(data.get("player_pos_x", 240.0))
	var py = float(data.get("player_pos_y", 220.0))
	
	load_map(target_map, "spawn_default", false)
	if player_instance:
		player_instance.global_position = Vector2(px, py)
	
	return true

func reset_to_new_game() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.remove_absolute(SAVE_PATH)
	
	if inventory:
		inventory.coins = 150
		inventory.seeds = 10
		inventory.crops_harvested = 0
		inventory.eggs_collected = 0
		inventory.fish_caught = 0
		inventory.hay_bundles = 5
		inventory.active_tool = 1
		inventory.current_quest_id = 1
		inventory.quest_progress = 0
		inventory.quest_target = 4
		inventory.inventory_changed.emit()
	
	saved_plots_data.clear()
	load_map("res://scenes/maps/farm_map.tscn", "spawn_default", true)
	save_game()

# -------------------------------------------------------------
# THỜI TIẾT & HIỆU ỨNG MƯA
# -------------------------------------------------------------
func setup_rain_particles() -> void:
	var rain_canvas = CanvasLayer.new()
	rain_canvas.layer = 5
	add_child(rain_canvas)
	
	rain_particles = CPUParticles2D.new()
	rain_particles.amount = 180
	rain_particles.lifetime = 1.0
	rain_particles.preprocess = 0.5
	rain_particles.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	rain_particles.emission_rect_extents = Vector2(400, 10)
	rain_particles.position = Vector2(320, -10)
	rain_particles.direction = Vector2(0.2, 1.0)
	rain_particles.spread = 4.0
	rain_particles.initial_velocity_min = 380.0
	rain_particles.initial_velocity_max = 480.0
	rain_particles.scale_amount_min = 1.2
	rain_particles.scale_amount_max = 2.0
	rain_particles.color = Color(0.85, 0.92, 1.0, 0.65)
	rain_particles.emitting = false
	rain_canvas.add_child(rain_particles)

func is_indoor_map() -> bool:
	if not current_map:
		return false
	var map_n = current_map.name.to_lower()
	return map_n.ends_with("interior") or map_n.contains("interior") or map_n.contains("house")

func update_indoor_outdoor_environment() -> void:
	var weather_on = game_settings.weather_enabled if game_settings else true
	var day_night_on = game_settings.day_night_enabled if game_settings else true
	
	if is_indoor_map():
		# Trong nhà: KHÔNG CÓ MƯA
		if rain_particles:
			rain_particles.emitting = false
		# Ánh sáng trong nhà luôn có đèn điện sáng sủa ấm cúng
		if canvas_modulate:
			canvas_modulate.color = Color(1.0, 0.98, 0.94, 1.0)
	else:
		# Ngoài trời: Cập nhật mưa và ánh sáng thực tế nếu bật cài đặt
		if rain_particles and time_system:
			rain_particles.emitting = weather_on and time_system.is_raining
		if canvas_modulate and time_system:
			if day_night_on:
				canvas_modulate.color = time_system.get_ambient_light()
			else:
				canvas_modulate.color = Color(1.0, 1.0, 1.0, 1.0)

func _on_weather_changed(is_raining: bool, weather_name: String, _weather_icon: String, temp_c: float) -> void:
	var weather_on = game_settings.weather_enabled if game_settings else true
	
	if rain_particles:
		if is_indoor_map() or not weather_on:
			rain_particles.emitting = false
		else:
			rain_particles.emitting = is_raining
	
	if is_raining and not is_indoor_map() and weather_on:
		if not is_in_home_menu:
			ui.show_toast("🌧️ Trời có " + weather_name + " (%.1f°C)! Mưa đang tưới mát các luống ruộng." % temp_c)
		auto_water_farm_plots()

func auto_water_farm_plots() -> void:
	if not current_map or current_map.name != "FarmMap":
		return
	var plots_node = current_map.find_child("FarmPlots", true, false)
	if not plots_node:
		return
	for child in plots_node.get_children():
		if child is FarmPlot:
			if child.state == FarmPlot.State.TILLED_DRY:
				child.state = FarmPlot.State.TILLED_WET
				child.update_visuals()
			elif child.state == FarmPlot.State.SEEDED or child.state == FarmPlot.State.GROWING:
				child.growth_time += 1.5

func _on_light_changed(col: Color) -> void:
	if canvas_modulate:
		if is_indoor_map():
			canvas_modulate.color = Color(1.0, 0.98, 0.94, 1.0)
		else:
			var day_night_on = game_settings.day_night_enabled if game_settings else true
			if day_night_on:
				canvas_modulate.color = col
			else:
				canvas_modulate.color = Color(1.0, 1.0, 1.0, 1.0)

# -------------------------------------------------------------
# CHUYỂN BẢN ĐỒ & TẢI Ô RUỘNG
# -------------------------------------------------------------
func load_map(map_path: String, spawn_name: String, animate: bool = true) -> void:
	if is_transitioning:
		return
	is_transitioning = true
	
	# Khóa input người chơi trong khi chuyển cảnh
	if player_instance:
		player_instance.input_blocked = true
	
	if animate and transition_rect:
		var tween = create_tween()
		tween.tween_property(transition_rect, "color:a", 1.0, 0.18)
		await tween.finished
	
	# Lưu trạng thái ruộng nếu rời farm_map
	if current_map and current_map.name == "FarmMap":
		save_farm_plots_state()
	
	# Gỡ bỏ map cũ
	if current_map:
		if player_instance and player_instance.get_parent():
			player_instance.get_parent().remove_child(player_instance)
		current_map.queue_free()
		await get_tree().process_frame
	
	# Tạo map mới
	var map_resource = load(map_path)
	if not map_resource:
		is_transitioning = false
		if player_instance:
			player_instance.input_blocked = is_in_home_menu
		return
		
	current_map = map_resource.instantiate()
	map_container.add_child(current_map)
	current_map.change_map_requested.connect(_on_change_map_requested)
	update_indoor_outdoor_environment()
	
	# Đưa Player vào YSort của map mới
	var ysort_node = current_map.find_child("YSort", true, false)
	if ysort_node:
		ysort_node.add_child(player_instance)
	else:
		current_map.add_child(player_instance)
	
	# Đặt vị trí xuất hiện cho người chơi
	var spawn_pos = current_map.get_spawn_position(spawn_name)
	player_instance.global_position = spawn_pos
	
	# Thiết lập camera theo kích thước map và loại bỏ viền xám / khựng hình
	var cam: Camera2D = player_instance.get_node_or_null("Camera2D")
	if cam:
		cam.limit_left = 0
		cam.limit_top = 0
		cam.limit_right = int(current_map.map_width)
		cam.limit_bottom = int(current_map.map_height)
		if current_map.name.ends_with("Interior"):
			cam.zoom = Vector2(1.25, 1.25)
		else:
			cam.zoom = Vector2(1.0, 1.0)
		cam.reset_smoothing()
	
	# Cập nhật nhãn vị trí trên UI
	ui.update_location(current_map.map_title)
	
	# Cập nhật Ambient Sound theo map và thời gian
	if audio_manager and time_system:
		var is_sea = current_map.name.to_lower().contains("highway") or current_map.name.to_lower().contains("island")
		audio_manager.update_ambient(time_system.current_hour, is_sea)
	
	# Nếu là FarmMap thì thiết lập / khôi phục các ô ruộng
	if current_map.name == "FarmMap":
		restore_farm_plots()
	
	# Mở màn hình mờ dần
	if animate and transition_rect:
		var tween_in = create_tween()
		tween_in.tween_property(transition_rect, "color:a", 0.0, 0.22)
		await tween_in.finished
		if not is_in_home_menu:
			ui.show_toast("📍 " + current_map.map_title)
	
	# Mở khóa input nếu không ở Home Menu
	if player_instance:
		player_instance.input_blocked = is_in_home_menu
	is_transitioning = false

func _on_change_map_requested(target_map_path: String, spawn_name: String) -> void:
	load_map(target_map_path, spawn_name, true)

func save_farm_plots_state() -> void:
	var plots_node = current_map.find_child("FarmPlots", true, false)
	if not plots_node:
		return
	saved_plots_data.clear()
	for child in plots_node.get_children():
		if child is FarmPlot:
			saved_plots_data.append({
				"x": child.grid_x,
				"y": child.grid_y,
				"state": child.state,
				"crop_type": child.crop_type,
				"growth": child.growth_time
			})

func restore_farm_plots() -> void:
	var plots_node = current_map.find_child("FarmPlots", true, false)
	if not plots_node:
		return
	
	# Xóa các ô cũ nếu có
	for child in plots_node.get_children():
		child.queue_free()
	await get_tree().process_frame
	
	var start_x = 300.0
	var start_y = 110.0
	var tile_size = 36.0
	
	if saved_plots_data.is_empty():
		# Khởi tạo mặc định
		for row in range(4):
			for col in range(8):
				var plot = farm_plot_scene.instantiate()
				plot.position = Vector2(start_x + col * tile_size, start_y + row * tile_size)
				plot.grid_x = col
				plot.grid_y = row
				if row < 2:
					plot.state = FarmPlot.State.TILLED_DRY
				else:
					plot.state = FarmPlot.State.UNTILLED
				plots_node.add_child(plot)
	else:
		# Khôi phục trạng thái đã lưu
		for data in saved_plots_data:
			var plot = farm_plot_scene.instantiate()
			plot.position = Vector2(start_x + data["x"] * tile_size, start_y + data["y"] * tile_size)
			plot.grid_x = data["x"]
			plot.grid_y = data["y"]
			plot.state = data["state"]
			plot.crop_type = data.get("crop_type", FarmPlot.CropType.CORN)
			plot.growth_time = data["growth"]
			plots_node.add_child(plot)

func capture_screen() -> void:
	await get_tree().create_timer(0.5).timeout
	var vp = get_viewport()
	if vp:
		var img = vp.get_texture().get_image()
		if img:
			img.save_png("res://screenshot_game.png")
	get_tree().quit()
