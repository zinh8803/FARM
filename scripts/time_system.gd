extends Node
class_name TimeSystem

signal time_changed(hour: int, minute: int, day_name: String, day_num: int, period: String, weather_icon: String, weather_text: String, temp_str: String)
signal light_changed(light_color: Color)
signal weather_changed(is_raining: bool, weather_name: String, weather_icon: String, temp_c: float)

var current_hour: int = 12
var current_minute: int = 0
var current_second: int = 0
var current_day_num: int = 1
var current_month: int = 1
var current_weekday: int = 1

var day_names = ["Chủ nhật", "Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy"]

# Trạng thái thời tiết thực tế
var is_raining: bool = false
var weather_name: String = "Nắng ấm"
var weather_icon: String = "☀️"
var temperature_c: float = 30.0

var weather_enabled: bool = true
var day_night_enabled: bool = true

var http_req: HTTPRequest = null
var weather_refresh_timer: float = 0.0
var weather_fetched: bool = false

func _ready() -> void:
	# 1. Đọc thời gian thực tế từ hệ điều hành ngay lập tức
	sync_with_system_time()
	
	# 2. Khởi tạo HTTPRequest để lấy thời tiết thực tế qua Open-Meteo API
	http_req = HTTPRequest.new()
	http_req.timeout = 6.0
	add_child(http_req)
	http_req.request_completed.connect(_on_weather_request_completed)
	
	fetch_real_weather()
	emit_time_signals()

func _process(delta: float) -> void:
	# Cập nhật thời gian thực tế mỗi giây
	var now = Time.get_datetime_dict_from_system()
	if now["minute"] != current_minute or now["hour"] != current_hour:
		current_minute = now["minute"]
		current_hour = now["hour"]
		current_day_num = now["day"]
		current_month = now["month"]
		current_weekday = now["weekday"]
		emit_time_signals()
	
	# Cập nhật thời tiết định kỳ (10 phút 1 lần)
	weather_refresh_timer += delta
	if weather_refresh_timer >= 600.0:
		weather_refresh_timer = 0.0
		fetch_real_weather()

func sync_with_system_time() -> void:
	var now = Time.get_datetime_dict_from_system()
	current_hour = now["hour"]
	current_minute = now["minute"]
	current_second = now["second"]
	current_day_num = now["day"]
	current_month = now["month"]
	current_weekday = now["weekday"]
	
	# Mặc định thời tiết theo buổi nếu chưa có dữ liệu mạng
	update_default_weather()

func update_default_weather() -> void:
	if weather_fetched:
		return
	if current_hour >= 6 and current_hour < 18:
		weather_icon = "☀️"
		weather_name = "Nắng ấm"
		temperature_c = 31.0
		is_raining = false
	else:
		weather_icon = "🌙"
		weather_name = "Trời đêm mát"
		temperature_c = 26.5
		is_raining = false

func fetch_real_weather() -> void:
	if not http_req:
		return
	if http_req.get_http_client_status() != HTTPClient.STATUS_DISCONNECTED:
		return
	# Sử dụng tọa độ Việt Nam (Mặc định 10.82, 106.63) qua Open-Meteo hoàn toàn miễn phí
	var url = "https://api.open-meteo.com/v1/forecast?latitude=10.822&longitude=106.6257&current_weather=true"
	var err = http_req.request(url)
	if err != OK:
		print("Không thể gửi request thời tiết, dùng thời tiết mặc định")

func _on_weather_request_completed(_result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		update_default_weather()
		emit_time_signals()
		return
	
	var json_str = body.get_string_from_utf8()
	var json = JSON.new()
	var parse_err = json.parse(json_str)
	if parse_err != OK:
		update_default_weather()
		emit_time_signals()
		return
	
	var data = json.get_data()
	if not data is Dictionary or not data.has("current_weather"):
		update_default_weather()
		emit_time_signals()
		return
	
	var cw = data["current_weather"]
	temperature_c = cw.get("temperature", 30.0)
	var code = int(cw.get("weathercode", 0))
	var is_day = int(cw.get("is_day", 1))
	
	weather_fetched = true
	
	# Bảng mã thời tiết chuẩn WMO:
	# 51..67, 80..82, 95..99: Mưa rào, mưa phùn hoặc dông sét
	if code in [51, 53, 55]:
		is_raining = true
		weather_icon = "🌦️"
		weather_name = "Mưa phùn"
	elif code in [61, 63, 65, 80, 81, 82]:
		is_raining = true
		weather_icon = "🌧️"
		weather_name = "Mưa rào"
	elif code in [95, 96, 99]:
		is_raining = true
		weather_icon = "⛈️"
		weather_name = "Mưa dông"
	elif code in [1, 2, 3]:
		is_raining = false
		weather_icon = "⛅"
		weather_name = "Nhiều mây"
	elif code in [45, 48]:
		is_raining = false
		weather_icon = "🌫️"
		weather_name = "Sương mù"
	else:
		is_raining = false
		if is_day == 1:
			weather_icon = "☀️"
			weather_name = "Nắng ấm"
		else:
			weather_icon = "🌙"
			weather_name = "Trời quang"
	
	emit_time_signals()
	weather_changed.emit(is_raining, weather_name, weather_icon, temperature_c)

func set_weather_enabled(enabled: bool) -> void:
	weather_enabled = enabled
	if not weather_enabled:
		is_raining = false
		weather_name = "Nắng ấm"
		weather_icon = "☀️"
		weather_changed.emit(false, "Nắng ấm", "☀️", temperature_c)
	else:
		fetch_real_weather()
	emit_time_signals()

func set_day_night_enabled(enabled: bool) -> void:
	day_night_enabled = enabled
	light_changed.emit(get_ambient_light())

func emit_time_signals() -> void:
	var period = get_period_name()
	var safe_idx = clamp(current_weekday, 0, day_names.size() - 1)
	var day_name = day_names[safe_idx]
	var temp_str = "%.1f°C" % temperature_c
	
	var icon = weather_icon if weather_enabled else "☀️"
	var w_text = weather_name if weather_enabled else "Nắng ráo"
	
	time_changed.emit(current_hour, current_minute, day_name, current_day_num, period, icon, w_text, temp_str)
	light_changed.emit(get_ambient_light())

func get_period_name() -> String:
	if current_hour >= 5 and current_hour < 11:
		return "Buổi sáng"
	elif current_hour >= 11 and current_hour < 14:
		return "Buổi trưa"
	elif current_hour >= 14 and current_hour < 18:
		return "Buổi chiều"
	elif current_hour >= 18 and current_hour < 22:
		return "Buổi tối"
	else:
		return "Đêm khuya"

func get_ambient_light() -> Color:
	# Nếu tính năng sáng/tối bị tắt thì luôn giữ ánh sáng ban ngày tự nhiên sáng rõ
	if not day_night_enabled:
		return Color(1.0, 1.0, 1.0, 1.0)
	
	# Tính toán ánh sáng môi trường theo giờ thực tế trong ngày:
	# Sáng thì sáng, tối thì tối, chiều hoàng hôn cam ấm, đêm trăng xanh dịu
	var t_float = float(current_hour) + float(current_minute) / 60.0
	var base_col: Color
	
	if t_float >= 7.0 and t_float < 16.5:
		# 07:00 - 16:30: Ban ngày sáng rực rỡ tự nhiên
		base_col = Color(1.0, 1.0, 1.0, 1.0)
	elif t_float >= 16.5 and t_float < 18.0:
		# 16:30 - 18:00: Chiều tà vàng cam ấm
		var progress = (t_float - 16.5) / 1.5
		base_col = Color(1.0, 1.0, 1.0).lerp(Color(1.0, 0.78, 0.52), progress)
	elif t_float >= 18.0 and t_float < 19.5:
		# 18:00 - 19:30: Hoàng hôn chuyển tối
		var progress = (t_float - 18.0) / 1.5
		base_col = Color(1.0, 0.78, 0.52).lerp(Color(0.38, 0.40, 0.62), progress)
	elif t_float >= 19.5 or t_float < 5.0:
		# 19:30 - 05:00: Đêm tối rõ rệt có ánh trăng sao
		base_col = Color(0.32, 0.35, 0.55, 1.0)
	elif t_float >= 5.0 and t_float < 6.0:
		# 05:00 - 06:00: Bình minh rạng đông ửng hồng
		var progress = (t_float - 5.0) / 1.0
		base_col = Color(0.32, 0.35, 0.55).lerp(Color(0.85, 0.68, 0.55), progress)
	else: # 06:00 - 07:00:
		# Sáng sớm nắng lên
		var progress = (t_float - 6.0) / 1.0
		base_col = Color(0.85, 0.68, 0.55).lerp(Color(1.0, 1.0, 1.0), progress)
	
	# Nếu trời mưa thì bầu trời âm u, mờ xám (chỉ khi bật thời tiết)
	if weather_enabled and is_raining:
		base_col = base_col * Color(0.72, 0.76, 0.82, 1.0)
	
	return base_col
