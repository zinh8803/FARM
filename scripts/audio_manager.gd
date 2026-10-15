extends Node
class_name AudioManagerClass

var sound_enabled: bool = true

var sfx_click: AudioStream
var sfx_toggle: AudioStream
var sfx_tool: AudioStream
var sfx_water: AudioStream
var sfx_plant: AudioStream
var sfx_harvest: AudioStream
var bgm_stream: AudioStream

var bgm_player: AudioStreamPlayer
var sfx_player: AudioStreamPlayer

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
	if ResourceLoader.exists("res://assets/audio/bgm_farm.wav"):
		bgm_stream = load("res://assets/audio/bgm_farm.wav")

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	
	bgm_player = AudioStreamPlayer.new()
	bgm_player.stream = bgm_stream
	bgm_player.volume_db = -8.0
	bgm_player.bus = "Master"
	add_child(bgm_player)
	
	sfx_player = AudioStreamPlayer.new()
	sfx_player.volume_db = -2.0
	sfx_player.bus = "Master"
	add_child(sfx_player)
	
	bgm_player.finished.connect(_on_bgm_finished)
	
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
