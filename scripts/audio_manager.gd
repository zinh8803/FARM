extends Node
class_name AudioManagerClass

var sound_enabled: bool = true

var sfx_click: AudioStream
var sfx_toggle: AudioStream
var sfx_tool: AudioStream
var sfx_water: AudioStream
var sfx_plant: AudioStream
var sfx_harvest: AudioStream

# 1.4 Nhạc nền & Âm thanh môi trường Ambient
var bgm_stream: AudioStream
var bgm_chillhop: AudioStream

var ambient_rooster: AudioStream
var ambient_cicada: AudioStream
var ambient_cricket: AudioStream
var ambient_waves: AudioStream

var bgm_player: AudioStreamPlayer
var ambient_player: AudioStreamPlayer
var sfx_player: AudioStreamPlayer

var current_ambient_mode: String = ""

func _init() -> void:
	if ResourceLoader.exists("res://assets/audio/click.wav"):
		sfx_click = load("res://assets/audio/click.wav")
	if ResourceLoader.exists("res://assets/audio/toggle.wav"):
		sfx_toggle = load("res://assets/audio/toggle.wav")
	if ResourceLoader.exists("res://assets/audio/tool.wav"):
		sfx_tool = load("res://assets/audio/tool.wav")
	if ResourceLoader.exists("res://assets/audio/water.wav"):
		sfx_water = load("res://assets/audio/water.wav")
	if ResourceLoader.exists("res://assets/audio/plant.wav"):
		sfx_plant = load("res://assets/audio/plant.wav")
	if ResourceLoader.exists("res://assets/audio/harvest.wav"):
		sfx_harvest = load("res://assets/audio/harvest.wav")
	
	if ResourceLoader.exists("res://assets/audio/bgm_chillhop_vietnam.wav"):
		bgm_chillhop = load("res://assets/audio/bgm_chillhop_vietnam.wav")
		bgm_stream = bgm_chillhop
	elif ResourceLoader.exists("res://assets/audio/bgm_farm.wav"):
		bgm_stream = load("res://assets/audio/bgm_farm.wav")
		
	if ResourceLoader.exists("res://assets/audio/rooster_morning.wav"):
		ambient_rooster = load("res://assets/audio/rooster_morning.wav")
	if ResourceLoader.exists("res://assets/audio/cicada_noon.wav"):
		ambient_cicada = load("res://assets/audio/cicada_noon.wav")
	if ResourceLoader.exists("res://assets/audio/cricket_night.wav"):
		ambient_cricket = load("res://assets/audio/cricket_night.wav")
	if ResourceLoader.exists("res://assets/audio/sea_waves.wav"):
		ambient_waves = load("res://assets/audio/sea_waves.wav")

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	
	bgm_player = AudioStreamPlayer.new()
	bgm_player.stream = bgm_stream
	bgm_player.volume_db = -9.0
	bgm_player.bus = "Master"
	add_child(bgm_player)
	
	ambient_player = AudioStreamPlayer.new()
	ambient_player.volume_db = -12.0
	ambient_player.bus = "Master"
	add_child(ambient_player)
	
	sfx_player = AudioStreamPlayer.new()
	sfx_player.volume_db = -2.0
	sfx_player.bus = "Master"
	add_child(sfx_player)
	
	bgm_player.finished.connect(_on_bgm_finished)
	ambient_player.finished.connect(_on_ambient_finished)
	
	if sound_enabled and bgm_stream:
		bgm_player.play()

func _on_bgm_finished() -> void:
	if sound_enabled and is_instance_valid(bgm_player):
		bgm_player.play()

func set_sound_enabled(enabled: bool) -> void:
	sound_enabled = enabled
	AudioServer.set_bus_mute(0, not enabled)
	if enabled:
		if bgm_player and not bgm_player.playing and bgm_stream:
			bgm_player.play()
	else:
		if bgm_player:
			bgm_player.stop()

func play_click() -> void:
	if sound_enabled and sfx_click:
		_play_sfx(sfx_click)

func play_toggle() -> void:
	if sound_enabled and sfx_toggle:
		_play_sfx(sfx_toggle)

func play_tool() -> void:
	if sound_enabled and sfx_tool:
		_play_sfx(sfx_tool)

func play_water() -> void:
	if sound_enabled and sfx_water:
		_play_sfx(sfx_water)

func play_plant() -> void:
	if sound_enabled and sfx_plant:
		_play_sfx(sfx_plant)

func play_harvest() -> void:
	if sound_enabled and sfx_harvest:
		_play_sfx(sfx_harvest)

func update_ambient(hour: int, is_near_sea: bool = false) -> void:
	if not sound_enabled:
		if ambient_player and ambient_player.playing:
			ambient_player.stop()
		return
		
	var target_stream: AudioStream = null
	var mode_name = ""
	
	if is_near_sea and ambient_waves:
		target_stream = ambient_waves
		mode_name = "waves"
	elif hour >= 5 and hour < 9 and ambient_rooster:
		target_stream = ambient_rooster
		mode_name = "rooster"
	elif hour >= 11 and hour < 14 and ambient_cicada:
		target_stream = ambient_cicada
		mode_name = "cicada"
	elif (hour >= 18 or hour < 5) and ambient_cricket:
		target_stream = ambient_cricket
		mode_name = "cricket"
		
	if mode_name != current_ambient_mode:
		current_ambient_mode = mode_name
		if target_stream and ambient_player:
			ambient_player.stream = target_stream
			ambient_player.play()
		elif ambient_player:
			ambient_player.stop()

func _on_ambient_finished() -> void:
	if sound_enabled and ambient_player and ambient_player.stream:
		# Lặp lại âm thanh ambient một cách tự nhiên
		get_tree().create_timer(1.5).timeout.connect(func():
			if sound_enabled and ambient_player and ambient_player.stream:
				ambient_player.play()
		)

func _play_sfx(stream: AudioStream) -> void:
	if not stream:
		return
	var p = AudioStreamPlayer.new()
	p.stream = stream
	p.volume_db = -2.0
	p.bus = "Master"
	add_child(p)
	p.finished.connect(p.queue_free)
	p.play()

