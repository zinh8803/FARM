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
@onready var update_progress_bar: ProgressBar = $UpdatePanel/MarginContainer/VBoxContainer/UpdateProgressBar
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
			"version": "1.4.0",
			"release_date": "2026-10-16",
			"changelog": []
		}
	
	var ver = str(local_version_info.get("version", "1.4.0"))
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
	if update_progress_bar:
		update_progress_bar.visible = false
		update_progress_bar.value = 0
	update_panel.visible = true
	
	await _do_auto_update()

func _on_close_update_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	update_panel.visible = false

# Query GitHub's latest release. The release must contain LittleDaNang.exe or LittleDaNang.zip
func _do_auto_update() -> void:
	if OS.has_feature("editor"):
		update_feedback_label.text = "ℹ️ Tính năng cập nhật file thực thi chỉ hoạt động khi chạy bản game đã xuất bản (.exe)."
		btn_close_update.disabled = false
		return

	var http := $UpdateHttpReq as HTTPRequest
	http.timeout = 15.0
	http.body_size_limit = -1
	update_feedback_label.text = "🔍 Đang kiểm tra bản cập nhật mới trên GitHub..."
	if update_progress_bar:
		update_progress_bar.visible = true
		update_progress_bar.value = 10
	
	var api_url := "https://api.github.com/repos/zinh8803/FARM/releases/latest"
	var err := http.request(api_url, ["User-Agent: LittleDaNang-Updater", "Accept: application/vnd.github+json"])
	if err != OK:
		_update_failed("Không thể kết nối máy chủ GitHub (mã lỗi %d)." % err)
		return
	var response: Array = await http.request_completed
	if response[0] != HTTPRequest.RESULT_SUCCESS or response[1] != 200:
		_update_failed("GitHub không trả về bản phát hành (HTTP %d). Hãy đảm bảo đã tạo Release trên GitHub." % response[1])
		return
	var parsed = JSON.parse_string((response[3] as PackedByteArray).get_string_from_utf8())
	if not parsed is Dictionary:
		_update_failed("Dữ liệu bản phát hành không hợp lệ.")
		return
	var release: Dictionary = parsed
	var asset_url := ""
	var asset_name := ""
	var asset_size: int = 0
	for asset in release.get("assets", []):
		if asset is Dictionary:
			var aname := str(asset.get("name", "")).to_lower()
			if aname in ["littledanang.exe", "littledanang.zip"]:
				asset_url = str(asset.get("browser_download_url", ""))
				asset_name = str(asset.get("name", ""))
				asset_size = int(asset.get("size", 0))
				break
	if asset_url.is_empty():
		_update_failed("Release mới nhất chưa có file LittleDaNang.exe hoặc LittleDaNang.zip.")
		return

	var tag := str(release.get("tag_name", "")).trim_prefix("v")
	var current := str(local_version_info.get("version", "0.0.0")).trim_prefix("v")
	if tag == current:
		if update_progress_bar:
			update_progress_bar.value = 100
		update_feedback_label.text = "✅ Game đã ở phiên bản mới nhất: v%s. Không cần cập nhật." % current
		btn_close_update.disabled = false
		return

	# Cần cập nhật: Bắt đầu tải bản mới kèm loading tiến độ
	update_feedback_label.text = "⬇️ Tìm thấy bản v%s! Bắt đầu tải..." % tag
	if update_progress_bar:
		update_progress_bar.value = 0

	http.timeout = 0 # Không giới hạn timeout khi tải file lớn
	err = http.request(asset_url, ["User-Agent: LittleDaNang-Updater", "Accept: application/octet-stream"])
	if err != OK:
		_update_failed("Không thể bắt đầu tải file cập nhật (mã lỗi %d)." % err)
		return

	# Vòng lặp cập nhật tiến độ (Progress Bar) theo thời gian thực
	var download_finished := false
	var download_res: Array = []
	
	var on_completed = func(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray):
		download_finished = true
		download_res = [result, response_code, headers, body]
	
	http.request_completed.connect(on_completed, CONNECT_ONE_SHOT)

	while not download_finished:
		var downloaded := http.get_downloaded_bytes()
		var body_len := http.get_body_size()
		if body_len <= 0 and asset_size > 0:
			body_len = asset_size
		
		if body_len > 0 and downloaded > 0:
			var pct := clampf(float(downloaded) / float(body_len) * 100.0, 0.0, 100.0)
			if update_progress_bar:
				update_progress_bar.value = pct
			var mb_dl := float(downloaded) / 1048576.0
			var mb_total := float(body_len) / 1048576.0
			update_feedback_label.text = "⏳ Đang tải bản v%s: %.1f MB / %.1f MB (%.0f%%)..." % [tag, mb_dl, mb_total, pct]
		elif downloaded > 0:
			var mb_dl := float(downloaded) / 1048576.0
			update_feedback_label.text = "⏳ Đang tải bản v%s: %.1f MB..." % [tag, mb_dl]
		
		await get_tree().create_timer(0.1).timeout

	if download_res.is_empty() or download_res[0] != HTTPRequest.RESULT_SUCCESS or download_res[1] != 200 or (download_res[3] as PackedByteArray).is_empty():
		var code: int = download_res[1] if download_res.size() > 1 else -1
		_update_failed("Tải bản cập nhật thất bại (mã phản hồi HTTP %d)." % code)
		return

	if update_progress_bar:
		update_progress_bar.value = 100

	update_feedback_label.text = "📦 Đang chuẩn bị áp dụng bản cập nhật..."
	await get_tree().create_timer(0.2).timeout

	var exe_path := OS.get_executable_path()
	var update_bytes: PackedByteArray = download_res[3]
	if asset_name.to_lower().ends_with(".zip"):
		var zip_path := exe_path + ".download.zip"
		var zip_file := FileAccess.open(zip_path, FileAccess.WRITE)
		if zip_file == null:
			_update_failed("Không ghi được file ZIP tạm.")
			return
		zip_file.store_buffer(update_bytes)
		zip_file.close()
		var zip_reader := ZIPReader.new()
		var zip_err := zip_reader.open(zip_path)
		if zip_err != OK:
			DirAccess.remove_absolute(zip_path)
			_update_failed("File tải về không phải ZIP hợp lệ.")
			return
		var exe_entry := ""
		for entry in zip_reader.get_files():
			if entry.get_file().to_lower() == "littledanang.exe":
				exe_entry = entry
				break
		if exe_entry.is_empty():
			zip_reader.close()
			DirAccess.remove_absolute(zip_path)
			_update_failed("Trong ZIP không tìm thấy LittleDaNang.exe.")
			return
		update_bytes = zip_reader.read_file(exe_entry)
		zip_reader.close()
		DirAccess.remove_absolute(zip_path)

	# Ghi file mới ra đĩa
	var temp_path := exe_path + ".update"
	var file := FileAccess.open(temp_path, FileAccess.WRITE)
	if file == null:
		_update_failed("Không ghi được file cập nhật mới vào thư mục game. Vui lòng kiểm tra quyền ghi.")
		return
	file.store_buffer(update_bytes)
	file.close()

	# Tạo helper script để xóa file thực thi cũ và khởi chạy file mới
	var helper_path := exe_path.get_base_dir().path_join("apply_game_update.bat")
	var helper := FileAccess.open(helper_path, FileAccess.WRITE)
	if helper == null:
		DirAccess.remove_absolute(temp_path)
		_update_failed("Không thể tạo script cập nhật.")
		return
	
	# Script bat:
	# 1. Đợi game cũ tắt hoàn toàn
	# 2. Xóa file game cũ
	# 3. Đổi tên file mới (.update) thành file game chính
	# 4. Chạy game mới
	# 5. Xóa file bat này
	var bat_script := "@echo off\r\n"
	bat_script += "setlocal\r\n"
	bat_script += "set \"GAME=%~1\"\r\n"
	bat_script += "set \"NEW=%GAME%.update\"\r\n"
	bat_script += ":wait_game\r\n"
	bat_script += "tasklist /FI \"IMAGENAME eq %~nx1\" 2>nul | find /I \"%~nx1\" >nul\r\n"
	bat_script += "if not errorlevel 1 (\r\n"
	bat_script += "    timeout /t 1 /nobreak >nul\r\n"
	bat_script += "    goto wait_game\r\n"
	bat_script += ")\r\n"
	bat_script += ":delete_old\r\n"
	bat_script += "del /F /Q \"%GAME%\" >nul 2>&1\r\n"
	bat_script += "if exist \"%GAME%\" (\r\n"
	bat_script += "    timeout /t 1 /nobreak >nul\r\n"
	bat_script += "    goto delete_old\r\n"
	bat_script += ")\r\n"
	bat_script += "move /Y \"%NEW%\" \"%GAME%\" >nul 2>&1\r\n"
	bat_script += "start \"\" \"%GAME%\"\r\n"
	bat_script += "(goto) 2>nul & del \"%~f0\"\r\n"

	helper.store_string(bat_script)
	helper.close()

	OS.create_process("cmd.exe", ["/c", "start", "", helper_path, exe_path])
	update_feedback_label.text = "🎉 Đã cập nhật lên v%s!\nĐang khởi động lại game mới..." % tag
	await get_tree().create_timer(0.6).timeout
	get_tree().quit()

func _update_failed(message: String) -> void:
	update_feedback_label.text = "❌ Cập nhật thất bại:\n" + message
	if update_progress_bar:
		update_progress_bar.visible = false
	btn_close_update.disabled = false

# Giữ lại handler cho các nút cũ (phòng trường hợp scene vẫn tham chiếu)
func _on_check_update_pressed() -> void:
	pass

func _on_pull_update_pressed() -> void:
	pass

func _on_restart_game_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	
	get_tree().quit()

func _on_quit_pressed() -> void:
	if audio_manager:
		audio_manager.play_click()
	get_tree().quit()

