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
	update_feedback_label.text = ""
	btn_pull_update.visible = false
	btn_restart_game.visible = false
	btn_check_update.disabled = false
	update_panel.visible = true

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

func _on_check_update_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	
	var game_dir = get_game_dir()
	update_feedback_label.text = "⏳ Đang kết nối Git repository kiểm tra phiên bản...\n📂 Thư mục: " + game_dir
	btn_check_update.disabled = true
	
	# Kiểm tra trạng thái Git local và remote qua command line
	var output = []
	var exit_code = git_execute("remote -v", output)
	
	if exit_code != 0 or output.is_empty() or str(output[0]).strip_edges() == "":
		update_feedback_label.text = "⚠️ Thư mục game chưa có kho Git!\n📂 Đường dẫn: " + game_dir + "\n\n💡 Giải pháp:\n1. Hãy đặt file game (.exe) vào cùng thư mục dự án có chứa thư mục .git\n2. Hoặc chạy file 'git_setup_and_push.bat' để cấu hình kho Git."
		btn_check_update.disabled = false
		return
	
	# Thực hiện git fetch để kiểm tra commit mới
	update_feedback_label.text = "⏳ Đang kiểm tra commit mới nhất từ Git (git fetch)..."
	await get_tree().create_timer(0.3).timeout
	
	var fetch_out = []
	git_execute("fetch origin", fetch_out)
	
	# So sánh commit local và remote
	var status_out = []
	git_execute("status -uno", status_out)
	var status_text = status_out[0] if not status_out.is_empty() else ""
	
	var ver = str(local_version_info.get("version", "1.1.0"))
	
	if "behind" in status_text or "can be fast-forwarded" in status_text:
		update_feedback_label.text = "🔔 Phát hiện mã nguồn phiên bản mới trên Git!\nNhấn nút 'Cập Nhật Git' bên dưới để đồng bộ về máy."
		btn_pull_update.text = "⬇️ Cập Nhật Git (Pull)"
		btn_pull_update.visible = true
	else:
		update_feedback_label.text = "✅ Bạn đang ở phiên bản mới nhất: v%s!\n(Nếu vừa push commit mới, bạn có thể bấm 'Đồng Bộ Lại' bên dưới)." % ver
		btn_pull_update.text = "🔄 Đồng Bộ Lại (Git Pull)"
		btn_pull_update.visible = true
	
	btn_check_update.disabled = false

func _on_pull_update_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	
	btn_pull_update.disabled = true
	btn_check_update.disabled = true
	update_feedback_label.text = "⏳ Đang kéo mã nguồn và tài nguyên mới nhất (git pull)..."
	
	await get_tree().create_timer(0.2).timeout
	
	var pull_out = []
	var code = git_execute("pull origin main", pull_out)
	if code != 0:
		code = git_execute("pull origin master", pull_out)
	
	var result_msg = pull_out[0] if not pull_out.is_empty() else ""
	
	if code == 0:
		load_version_file()
		update_feedback_label.text = "🎉 Cập nhật thành công từ Git!\n" + result_msg.strip_edges()
		btn_pull_update.visible = false
		btn_restart_game.visible = true
	else:
		update_feedback_label.text = "❌ Quá trình Git pull gặp lỗi:\n" + result_msg.strip_edges() + "\n💡 Bạn có thể chạy file 'update_game.bat' trong thư mục để kiểm tra."
		btn_pull_update.disabled = false
	
	btn_check_update.disabled = false

func _on_restart_game_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	
	# Khởi động lại game — tìm file exe trong thư mục game
	var game_dir = get_game_dir()
	var exe_path = OS.get_executable_path()
	if OS.has_feature("editor"):
		# Từ editor: chạy run_game.bat
		OS.create_process("cmd.exe", ["/c", "cd /d \"" + game_dir + "\" && start \"\" run_game.bat"])
	else:
		# Từ bản export: chạy lại chính file .exe
		OS.create_process(exe_path, [])
	get_tree().quit()

func _on_quit_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	get_tree().quit()
