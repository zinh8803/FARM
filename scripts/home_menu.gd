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
			"version": "1.4.1",
			"release_date": "2026-10-16",
			"changelog": []
		}
	
	var ver = str(local_version_info.get("version", "1.4.1"))
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

# Loads a release manifest, follows the version patch chain, verifies each PCK, and restarts.
func _do_auto_update() -> void:
	if OS.has_feature("editor"):
		_update_failed("Cập nhật PCK chỉ hoạt động trong bản game đã export.")
		return
	var http := $UpdateHttpReq as HTTPRequest
	http.timeout = 20.0
	http.body_size_limit = -1
	var manifest_url := "https://github.com/zinh8803/FARM/releases/latest/download/update_manifest.json"
	var response := await _fetch_update_response(http, manifest_url, "Đang tải manifest cập nhật...", 0)
	if not _http_response_ok(response):
		_update_failed("Không tải được update_manifest.json (HTTP %d). Hãy phát hành manifest lên GitHub Release mới nhất." % _http_code(response))
		return
	var manifest_data = JSON.parse_string((response[3] as PackedByteArray).get_string_from_utf8())
	if not manifest_data is Dictionary or not manifest_data.get("patches", []) is Array:
		_update_failed("Manifest cập nhật không đúng định dạng JSON.")
		return
	var latest_version := str(manifest_data.get("latest_version", "")).trim_prefix("v")
	if latest_version.is_empty():
		_update_failed("Manifest thiếu latest_version.")
		return

	var patch_index_path := "user://patches/installed_patches.json"
	var patch_index: Dictionary = {"version": str(local_version_info.get("version", "0.0.0")).trim_prefix("v"), "files": []}
	if FileAccess.file_exists(patch_index_path):
		var index_file := FileAccess.open(patch_index_path, FileAccess.READ)
		if index_file:
			var parsed_index = JSON.parse_string(index_file.get_as_text())
			index_file.close()
			if parsed_index is Dictionary:
				patch_index = parsed_index
	var current_version := str(patch_index.get("version", local_version_info.get("version", "0.0.0"))).trim_prefix("v")
	var installed_files: Array = patch_index.get("files", [])
	if current_version == latest_version:
		if update_progress_bar:
			update_progress_bar.value = 100
		update_feedback_label.text = "✅ Game đã ở phiên bản mới nhất: v%s." % latest_version
		btn_close_update.disabled = false
		return

	# Resolve ordered transitions until the manifest's latest_version is reached.
	var route: Array[Dictionary] = []
	var cursor := current_version
	for _step in range(64):
		if cursor == latest_version:
			break
		var next_patch: Dictionary = {}
		for patch_item in manifest_data["patches"]:
			if patch_item is Dictionary and str(patch_item.get("from", "")).trim_prefix("v") == cursor:
				next_patch = patch_item
				break
		if next_patch.is_empty():
			_update_failed("Không tìm thấy patch từ v%s đến v%s trong manifest." % [cursor, latest_version])
			return
		var next_version := str(next_patch.get("to", "")).trim_prefix("v")
		if next_version.is_empty() or next_version == cursor:
			_update_failed("Manifest có patch version không hợp lệ tại v%s." % cursor)
			return
		route.append(next_patch)
		cursor = next_version
	if cursor != latest_version:
		_update_failed("Chuỗi patch không dẫn tới phiên bản mới nhất v%s." % latest_version)
		return

	var patch_dir := ProjectSettings.globalize_path("user://patches")
	var dir_err := DirAccess.make_dir_recursive_absolute(patch_dir)
	if dir_err != OK and dir_err != ERR_ALREADY_EXISTS:
		_update_failed("Không thể tạo thư mục lưu patch: %s" % patch_dir)
		return
	var new_files: Array = []
	for patch_info in route:
		var patch_name := str(patch_info.get("file", ""))
		var patch_url := str(patch_info.get("url", ""))
		var expected_hash := str(patch_info.get("sha256", "")).to_lower()
		if patch_name.get_file() != patch_name or not patch_name.to_lower().ends_with(".pck") or not patch_url.begins_with("https://") or expected_hash.length() != 64:
			_update_failed("Một patch trong manifest thiếu tên, URL HTTPS hoặc SHA-256 hợp lệ.")
			return
		var patch_response := await _fetch_update_response(http, patch_url, "Đang tải patch %s..." % patch_name, 0)
		if not _http_response_ok(patch_response):
			_update_failed("Tải %s thất bại (HTTP %d)." % [patch_name, _http_code(patch_response)])
			return
		var patch_bytes: PackedByteArray = patch_response[3]
		var hasher := HashingContext.new()
		if hasher.start(HashingContext.HASH_SHA256) != OK:
			_update_failed("Không khởi tạo được bộ kiểm tra SHA-256.")
			return
		hasher.update(patch_bytes)
		if hasher.finish().hex_encode().to_lower() != expected_hash:
			_update_failed("SHA-256 của %s không khớp; patch bị từ chối." % patch_name)
			return
		var patch_path := "user://patches/" + patch_name
		var patch_file := FileAccess.open(patch_path, FileAccess.WRITE)
		if patch_file == null:
			_update_failed("Không thể lưu patch %s." % patch_name)
			return
		patch_file.store_buffer(patch_bytes)
		patch_file.close()
		new_files.append(patch_name)

	var all_files: Array = installed_files.duplicate()
	for patch_name in new_files:
		if not all_files.has(patch_name):
			all_files.append(patch_name)
	var index_out := FileAccess.open(patch_index_path, FileAccess.WRITE)
	if index_out == null:
		_update_failed("Không lưu được danh sách patch đã tải.")
		return
	index_out.store_string(JSON.stringify({"version": latest_version, "files": all_files}, "  "))
	index_out.close()
	update_feedback_label.text = "✅ Đã tải và kiểm tra %d patch. Đang khởi động lại để áp dụng v%s..." % [new_files.size(), latest_version]
	if update_progress_bar:
		update_progress_bar.value = 100
	await get_tree().create_timer(0.6).timeout
	var launch_error := OS.create_process(OS.get_executable_path(), [])
	if launch_error <= 0:
		_update_failed("Patch đã tải nhưng không tự mở lại được game. Hãy đóng rồi mở lại LittleDaNang.exe.")
		return
	get_tree().quit()

func _fetch_update_response(http: HTTPRequest, url: String, status_text: String, expected_size: int) -> Array:
	http.timeout = 0 # PCK files can be large; do not abort due to a fixed request timeout.
	http.body_size_limit = -1
	var finished := false
	var result_data: Array = []
	var callback := func(result: int, code: int, headers: PackedStringArray, body: PackedByteArray):
		finished = true
		result_data = [result, code, headers, body]
	http.request_completed.connect(callback, CONNECT_ONE_SHOT)
	var request_error := http.request(url, ["User-Agent: LittleDaNang-Updater", "Accept: application/json, application/octet-stream"])
	if request_error != OK:
		http.request_completed.disconnect(callback)
		return [HTTPRequest.RESULT_CANT_CONNECT, request_error, PackedStringArray(), PackedByteArray()]
	while not finished:
		var downloaded := http.get_downloaded_bytes()
		var total := http.get_body_size()
		if total <= 0:
			total = expected_size
		if downloaded > 0 and total > 0:
			var pct := clampf(float(downloaded) * 100.0 / float(total), 0.0, 100.0)
			if update_progress_bar:
				update_progress_bar.visible = true
				update_progress_bar.value = pct
			update_feedback_label.text = "%s %.1f / %.1f MB (%.0f%%)" % [status_text, float(downloaded) / 1048576.0, float(total) / 1048576.0, pct]
		else:
			update_feedback_label.text = status_text
		await get_tree().create_timer(0.1).timeout
	return result_data

func _http_response_ok(response: Array) -> bool:
	return response.size() >= 4 and response[0] == HTTPRequest.RESULT_SUCCESS and response[1] == 200 and not (response[3] as PackedByteArray).is_empty()

func _http_code(response: Array) -> int:
	return int(response[1]) if response.size() > 1 else -1

# Legacy full-executable updater retained for older references; the UI uses the PCK updater above.
func _do_auto_update_exe_legacy() -> void:
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
	var asset_updated_at := ""
	for asset in release.get("assets", []):
		if asset is Dictionary:
			var aname := str(asset.get("name", "")).to_lower()
			if aname in ["littledanang.exe", "littledanang.zip"]:
				asset_url = str(asset.get("browser_download_url", ""))
				asset_name = str(asset.get("name", ""))
				asset_size = int(asset.get("size", 0))
				asset_updated_at = str(asset.get("updated_at", ""))
				break
	if asset_url.is_empty():
		_update_failed("Release mới nhất chưa có file LittleDaNang.exe hoặc LittleDaNang.zip.")
		return

	var tag := str(release.get("tag_name", "")).trim_prefix("v")
	var current := str(local_version_info.get("version", "0.0.0")).trim_prefix("v")
	var exe_path := OS.get_executable_path()
	var marker_path := exe_path + ".release"
	var release_stamp := "%s|%s" % [tag, asset_updated_at]
	var installed_stamp := ""
	if FileAccess.file_exists(marker_path):
		var marker := FileAccess.open(marker_path, FileAccess.READ)
		if marker:
			installed_stamp = marker.get_as_text().strip_edges()
			marker.close()
	if tag == current and not asset_updated_at.is_empty() and installed_stamp == release_stamp:
		if update_progress_bar:
			update_progress_bar.value = 100
		update_feedback_label.text = "✅ Game đã ở phiên bản mới nhất: v%s. Không cần cập nhật." % current
		btn_close_update.disabled = false
		return

	# Cần cập nhật: Bắt đầu tải bản mới kèm loading tiến độ
	update_feedback_label.text = "⬇️ Tìm thấy bản v%s! Bắt đầu tải..." % tag
	if update_progress_bar:
		update_progress_bar.value = 0

	# Kết nối trước khi request để không bỏ lỡ trường hợp tải xong rất nhanh.
	var download_finished := false
	var download_res: Array = []
	var on_completed = func(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray):
		download_finished = true
		download_res = [result, response_code, headers, body]
	http.request_completed.connect(on_completed, CONNECT_ONE_SHOT)

	http.timeout = 0 # Không giới hạn timeout khi tải file lớn
	err = http.request(asset_url, ["User-Agent: LittleDaNang-Updater", "Accept: application/octet-stream"])
	if err != OK:
		http.request_completed.disconnect(on_completed)
		_update_failed("Không thể bắt đầu tải file cập nhật (mã lỗi %d)." % err)
		return

	# Vòng lặp cập nhật tiến độ (Progress Bar) theo thời gian thực
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

	var update_bytes: PackedByteArray = download_res[3]
	if asset_size > 0 and asset_name.to_lower().ends_with(".exe") and update_bytes.size() != asset_size:
		_update_failed("File tải về chưa đủ hoặc bị hỏng (%d / %d byte)." % [update_bytes.size(), asset_size])
		return
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
	if update_bytes.is_empty() or not FileAccess.file_exists(temp_path):
		_update_failed("Không tạo được file thực thi cập nhật.")
		return
	var marker_temp_path := marker_path + ".update"
	var marker_file := FileAccess.open(marker_temp_path, FileAccess.WRITE)
	if marker_file == null:
		_update_failed("Không ghi được thông tin phiên bản đã tải.")
		return
	marker_file.store_string(release_stamp)
	marker_file.close()

	# Tạo helper script để xóa file thực thi cũ và khởi chạy file mới
	var helper_path := exe_path.get_base_dir().path_join("apply_game_update.ps1")
	var helper := FileAccess.open(helper_path, FileAccess.WRITE)
	if helper == null:
		DirAccess.remove_absolute(temp_path)
		_update_failed("Không thể tạo script cập nhật.")
		return
	
	var ps_script := "param([string]$GamePath, [int]$GamePid)\n"
	ps_script += "$ErrorActionPreference = 'Stop'\n"
	ps_script += "$NewPath = $GamePath + '.update'\n"
	ps_script += "$MarkerPath = $GamePath + '.release'\n"
	ps_script += "$MarkerTemp = $MarkerPath + '.update'\n"
	ps_script += "$BackupPath = $GamePath + '.previous'\n"
	ps_script += "$LogPath = Join-Path $env:TEMP 'LittleDaNang_update.log'\n"
	ps_script += "try {\n"
	ps_script += "  while (Get-Process -Id $GamePid -ErrorAction SilentlyContinue) { Start-Sleep -Milliseconds 400 }\n"
	ps_script += "  if (!(Test-Path -LiteralPath $NewPath)) { throw 'Downloaded executable is missing.' }\n"
	ps_script += "  if (Test-Path -LiteralPath $BackupPath) { Remove-Item -LiteralPath $BackupPath -Force }\n"
	ps_script += "  if (Test-Path -LiteralPath $GamePath) { Move-Item -LiteralPath $GamePath -Destination $BackupPath -Force }\n"
	ps_script += "  try { Move-Item -LiteralPath $NewPath -Destination $GamePath -Force } catch { if (Test-Path -LiteralPath $BackupPath) { Move-Item -LiteralPath $BackupPath -Destination $GamePath -Force }; throw }\n"
	ps_script += "  if (Test-Path -LiteralPath $MarkerTemp) { Move-Item -LiteralPath $MarkerTemp -Destination $MarkerPath -Force }\n"
	ps_script += "  Start-Process -FilePath $GamePath -WorkingDirectory (Split-Path -Parent $GamePath)\n"
	ps_script += "  if (Test-Path -LiteralPath $BackupPath) { Remove-Item -LiteralPath $BackupPath -Force }\n"
	ps_script += "  'Update applied successfully.' | Set-Content -LiteralPath $LogPath\n"
	ps_script += "} catch {\n"
	ps_script += "  if (!(Test-Path -LiteralPath $GamePath) -and (Test-Path -LiteralPath $BackupPath)) { Move-Item -LiteralPath $BackupPath -Destination $GamePath -Force }\n"
	ps_script += "  ('Update failed: ' + $_.Exception.Message) | Set-Content -LiteralPath $LogPath\n"
	ps_script += "}\n"
	ps_script += "Remove-Item -LiteralPath $PSCommandPath -Force -ErrorAction SilentlyContinue\n"
	helper.store_string(ps_script)
	helper.close()

	var helper_pid := OS.create_process("powershell.exe", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", helper_path, exe_path, str(OS.get_process_id())])
	if helper_pid <= 0:
		DirAccess.remove_absolute(temp_path)
		DirAccess.remove_absolute(marker_temp_path)
		_update_failed("Windows không khởi chạy được tiến trình thay file. Hãy xem log tại %s." % OS.get_environment("TEMP").path_join("LittleDaNang_update.log"))
		return
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

