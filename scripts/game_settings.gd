extends Node
class_name GameSettings

signal settings_changed()

const SETTINGS_FILE = "user://settings.cfg"

var weather_enabled: bool = true
var day_night_enabled: bool = true
var sound_enabled: bool = true

func _ready() -> void:
	load_settings()

func load_settings() -> void:
	var config = ConfigFile.new()
	var err = config.load(SETTINGS_FILE)
	if err == OK:
		weather_enabled = config.get_value("settings", "weather_enabled", true)
		day_night_enabled = config.get_value("settings", "day_night_enabled", true)
		sound_enabled = config.get_value("settings", "sound_enabled", true)
	else:
		weather_enabled = true
		day_night_enabled = true
		sound_enabled = true
		save_settings()

func save_settings() -> void:
	var config = ConfigFile.new()
	config.set_value("settings", "weather_enabled", weather_enabled)
	config.set_value("settings", "day_night_enabled", day_night_enabled)
	config.set_value("settings", "sound_enabled", sound_enabled)
	config.save(SETTINGS_FILE)
	settings_changed.emit()

func set_weather(enabled: bool) -> void:
	if weather_enabled != enabled:
		weather_enabled = enabled
		save_settings()

func set_day_night(enabled: bool) -> void:
	if day_night_enabled != enabled:
		day_night_enabled = enabled
		save_settings()

func set_sound(enabled: bool) -> void:
	if sound_enabled != enabled:
		sound_enabled = enabled
		save_settings()
