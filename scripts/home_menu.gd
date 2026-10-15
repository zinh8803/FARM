extends CanvasLayer
class_name HomeMenu

signal play_game_pressed()
signal new_game_pressed()
signal return_to_home_pressed()

@onready var main_container: Control = $MainContainer
@onready var settings_panel: PanelContainer = $SettingsPanel
@onready var update_panel: PanelContainer = $UpdatePanel

@onready var btn_play: Button = $MainContainer/ButtonsContainer/BtnPlay
@onready var btn_new_game: Button = $MainContainer/ButtonsContainer/BtnNewGame
@onready var btn_settings: Button = $MainContainer/ButtonsContainer/BtnSettings
@onready var btn_update: Button = $MainContainer/ButtonsContainer/BtnUpdate
@onready var btn_quit: Button = $MainContainer/ButtonsContainer/BtnQuit

# Settings controls
@onready var btn_weather_toggle: Button = $SettingsPanel/MarginContainer/VBoxContainer/WeatherRow/BtnWeatherToggle
@onready var btn_day_night_toggle: Button = $SettingsPanel/MarginContainer/VBoxContainer/DayNightRow/BtnDayNightToggle
@onready var btn_sound_toggle: Button = $SettingsPanel/MarginContainer/VBoxContainer/SoundRow/BtnSoundToggle
@onready var btn_close_settings: Button = $SettingsPanel/MarginContainer/VBoxContainer/BtnCloseSettings

# Update controls
@onready var update_status_badge: Label = $UpdatePanel/MarginContainer/VBoxContainer/StatusBadge
@onready var update_roadmap_label: Label = $UpdatePanel/MarginContainer/VBoxContainer/RoadmapLabel
@onready var update_feedback_label: Label = $UpdatePanel/MarginContainer/VBoxContainer/FeedbackLabel
@onready var btn_check_update: Button = $UpdatePanel/MarginContainer/VBoxContainer/ButtonsRow/BtnCheckUpdate
@onready var btn_pull_update: Button = $UpdatePanel/MarginContainer/VBoxContainer/ButtonsRow/BtnPullUpdate
@onready var btn_restart_game: Button = $UpdatePanel/MarginContainer/VBoxContainer/ButtonsRow/BtnRestartGame
@onready var btn_close_update: Button = $UpdatePanel/MarginContainer/VBoxContainer/ButtonsRow/BtnCloseUpdate

var game_settings: GameSettings = null
var audio_manager: AudioManagerClass = null
var has_save_data: bool = false
var local_version_info: Dictionary = {}

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	settings_panel.visible = false
	update_panel.visible = false
	
	btn_play.pressed.connect(_on_play_pressed)
	btn_new_game.pressed.connect(_on_new_game_pressed)
	btn_settings.pressed.connect(_on_settings_pressed)
	btn_update.pressed.connect(_on_update_pressed)
	btn_quit.pressed.connect(_on_quit_pressed)
	
	btn_weather_toggle.pressed.connect(_on_weather_toggle_pressed)
	btn_day_night_toggle.pressed.connect(_on_day_night_toggle_pressed)
	btn_sound_toggle.pressed.connect(_on_sound_toggle_pressed)
	btn_close_settings.pressed.connect(_on_close_settings_pressed)
	
	btn_check_update.pressed.connect(_on_check_update_pressed)
	btn_pull_update.pressed.connect(_on_pull_update_pressed)
	btn_restart_game.pressed.connect(_on_restart_game_pressed)
	btn_close_update.pressed.connect(_on_close_update_pressed)
	
	load_version_file()

func load_version_file() -> void:
	if FileAccess.file_exists("res://version.json"):
		var f = FileAccess.open("res://version.json", FileAccess.READ)
		if f:
			var text = f.get_as_text()
			f.close()
			var json = JSON.new()
			if json.parse(text) == OK and json.get_data() is Dictionary:
				local_version_info = json.get_data()
	
	if local_version_info.is_empty():
		local_version_info = {
			"version": "1.1.0",
			"release_date": "2026-10-15",
			"changelog": []
		}
	
	var ver = str(local_version_info.get("version", "1.1.0"))
	var rdate = str(local_version_info.get("release_date", ""))
	if update_status_badge:
		update_status_badge.text = "● Phiên bản hiện tại: v%s (%s)" % [ver, rdate]
	
	var changelog = local_version_info.get("changelog", [])
	if update_roadmap_label and not changelog.is_empty():
		var summary = "📜 Các tính năng trong bản v%s:\n" % ver
		for item in changelog:
			summary += "• " + str(item) + "\n"
		update_roadmap_label.text = summary.strip_edges()

func setup(settings: GameSettings, audio: AudioManagerClass, save_exists: bool) -> void:
	game_settings = settings
	audio_manager = audio
	has_save_data = save_exists
	
	if has_save_data:
		btn_play.text = "▶️ Tiếp tục chơi"
	else:
		btn_play.text = "▶️ Chơi"
	
	update_settings_ui()

func open_menu() -> void:
	visible = true
	main_container.visible = true
	settings_panel.visible = false
	update_panel.visible = false
	if has_save_data:
		btn_play.text = "▶️ Tiếp tục chơi"
	else:
		btn_play.text = "▶️ Chơi"

func close_menu() -> void:
	visible = false

func update_settings_ui() -> void:
	if not game_settings:
		return
	
	_style_toggle(btn_weather_toggle, game_settings.weather_enabled)
	_style_toggle(btn_day_night_toggle, game_settings.day_night_enabled)
	_style_toggle(btn_sound_toggle, game_settings.sound_enabled)

func _style_toggle(btn: Button, is_on: bool) -> void:
	if is_on:
		btn.text = "🟢 [ BẬT ]"
		btn.modulate = Color(0.7, 1.2, 0.7, 1.0)
	else:
		btn.text = "🔴 [ TẮT ]"
		btn.modulate = Color(1.2, 0.7, 0.7, 1.0)

func _on_play_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	play_game_pressed.emit()

func _on_new_game_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	new_game_pressed.emit()

func _on_settings_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	update_settings_ui()
	settings_panel.visible = true

func _on_close_settings_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	settings_panel.visible = false

func _on_weather_toggle_pressed() -> void:
	if not game_settings:
		return
	var new_state = not game_settings.weather_enabled
	game_settings.set_weather(new_state)
	if audio_manager:
		audio_manager.play_toggle()
	update_settings_ui()

func _on_day_night_toggle_pressed() -> void:
	if not game_settings:
		return
	var new_state = not game_settings.day_night_enabled
	game_settings.set_day_night(new_state)
	if audio_manager:
		audio_manager.play_toggle()
	update_settings_ui()

func _on_sound_toggle_pressed() -> void:
	if not game_settings:
		return
	var new_state = not game_settings.sound_enabled
	game_settings.set_sound(new_state)
	if audio_manager:
		audio_manager.set_sound_enabled(new_state)
		if new_state:
			audio_manager.play_toggle()
	update_settings_ui()

func _on_update_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	load_version_file()
	
	# Mở panel và bắt đầu cập nhật ngay lập tức
	btn_restart_game.visible = false
	btn_check_update.visible = false
	btn_pull_update.visible = false
	btn_close_update.disabled = true
	update_panel.visible = true
	
	# Chạy toàn bộ quy trình: fetch → pull tự động
	await _do_auto_update()

func _on_close_update_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	update_panel.visible = false

# Lấy thư mục gốc của game (nơi chứa .git, version.json, run_game.bat)
# - Khi chạy từ Editor: dùng đường dẫn project res://
# - Khi export: dùng thư mục chứa file .exe
func get_game_dir() -> String:
	if OS.has_feature("editor"):
		return ProjectSettings.globalize_path("res://")
	else:
		return OS.get_executable_path().get_base_dir()

# Chạy lệnh git trong đúng thư mục game (cd /d <thư mục> && git ...)
func git_execute(git_args: String, output: Array) -> int:
	var game_dir = get_game_dir()
	var cmd = "cd /d \"%s\" && git %s" % [game_dir, git_args]
	return OS.execute("cmd.exe", ["/c", cmd], output, true)

# Quy trình cập nhật tự động: fetch + pull trong 1 bước
func _do_auto_update() -> void:
	var game_dir = get_game_dir()
	
	# Bước 1: Kiểm tra Git có tồn tại không
	update_feedback_label.text = "⏳ [1/3] Đang kiểm tra kết nối Git...\n📂 " + game_dir
	await get_tree().create_timer(0.2).timeout
	
	var remote_out = []
	var remote_code = git_execute("remote -v", remote_out)
	
	if remote_code != 0 or remote_out.is_empty() or str(remote_out[0]).strip_edges() == "":
		update_feedback_label.text = "⚠️ Thư mục game chưa có kho Git!\n📂 " + game_dir + "\n\n💡 Giải pháp:\n1. Đặt file game (.exe) vào cùng thư mục dự án chứa .git\n2. Hoặc chạy 'git_setup_and_push.bat'"
		btn_close_update.disabled = false
		return
	
	# Bước 2: Git fetch
	update_feedback_label.text = "⏳ [2/3] Đang đồng bộ với GitHub (git fetch)..."
	await get_tree().create_timer(0.2).timeout
	
	var fetch_out = []
	git_execute("fetch origin", fetch_out)
	
	# Bước 3: Git pull
	update_feedback_label.text = "⏳ [3/3] Đang kéo mã nguồn mới nhất (git pull)..."
	await get_tree().create_timer(0.2).timeout
	
	var pull_out = []
	var code = git_execute("pull origin main", pull_out)
	if code != 0:
		code = git_execute("pull origin master", pull_out)
	
	var result_msg = str(pull_out[0]).strip_edges() if not pull_out.is_empty() else ""
	
	btn_close_update.disabled = false
	
	if code == 0:
		load_version_file()
		var ver = str(local_version_info.get("version", "1.1.0"))
		
		if "Already up to date" in result_msg or "Already up-to-date" in result_msg:
			update_feedback_label.text = "✅ Game đã ở phiên bản mới nhất: v%s!\n\nKhông có bản cập nhật mới." % ver
		else:
			update_feedback_label.text = "🎉 Cập nhật thành công!\n📦 Phiên bản: v%s\n\n%s\n\n👉 Nhấn 'Khởi động lại' để áp dụng bản cập nhật." % [ver, result_msg]
			btn_restart_game.visible = true
	else:
		update_feedback_label.text = "❌ Cập nhật thất bại:\n" + result_msg + "\n\n💡 Thử chạy file 'update_game.bat' trong thư mục game."

# Giữ lại handler cho các nút cũ (phòng trường hợp scene vẫn tham chiếu)
func _on_check_update_pressed() -> void:
	pass

func _on_pull_update_pressed() -> void:
	pass

func _on_restart_game_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	
	# Khởi động lại game
	var game_dir = get_game_dir()
	var exe_path = OS.get_executable_path()
	if OS.has_feature("editor"):
		OS.create_process("cmd.exe", ["/c", "cd /d \"" + game_dir + "\" && start \"\" run_game.bat"])
	else:
		OS.create_process(exe_path, [])
	get_tree().quit()

func _on_quit_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	get_tree().quit()

