extends CanvasLayer
class_name UIController

signal menu_button_pressed()

@onready var time_label: Label = $TopBar/TimeLabel
@onready var location_label: Label = $LocationBadge/LocationLabel
@onready var btn_menu: Button = get_node_or_null("BtnMenu")
@onready var quest_label: Label = $QuestPanel/QuestLabel
@onready var resource_label: Label = $ResourcePanel/ResourceLabel
@onready var toast_panel: PanelContainer = $ToastPanel
@onready var toast_label: Label = $ToastPanel/ToastLabel
@onready var dialogue_panel: PanelContainer = $DialoguePanel
@onready var dialogue_name: Label = $DialoguePanel/VBoxContainer/SpeakerName
@onready var dialogue_text: Label = $DialoguePanel/VBoxContainer/DialogueText
@onready var hotbar_container: HBoxContainer = $HotbarContainer

@onready var shop_panel: PanelContainer = $ShopPanel
@onready var shop_coins_label: Label = $ShopPanel/MarginContainer/VBoxContainer/ShopCoinsLabel
@onready var shop_produce_label: Label = $ShopPanel/MarginContainer/VBoxContainer/ShopProduceLabel

@onready var inventory_panel: PanelContainer = $InventoryPanel
@onready var fishing_gauge = $FishingGauge
@onready var inv_coins_label: Label = $InventoryPanel/MarginContainer/VBoxContainer/InvCoinsLabel
@onready var label_seeds_inv: Label = $InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot3/LabelSeedsInv
@onready var label_hay_inv: Label = $InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot5/LabelHayInv
@onready var label_crop_inv: Label = $InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot6/LabelCropInv
@onready var label_egg_inv: Label = $InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot7/LabelEggInv

var toast_tween: Tween
var is_dialogue_open: bool = false
var is_shop_open: bool = false
var is_inventory_menu_open: bool = false
var inventory: InventoryData
var fishing_active: bool = false
var fishing_bite: bool = false
var fishing_wait_timer: float = 0.0
var fishing_marker: float = 0.0
var fishing_marker_direction: float = 1.0
var fishing_target_start: float = 0.4
var fishing_target_width: float = 0.18
var fish_market_open: bool = false

# Hàng đợi toast để không mất thông báo khi có nhiều hành động cùng lúc
var _toast_queue: Array[String] = []
var _is_showing_toast: bool = false

func _ensure_nodes() -> void:
	if not time_label: time_label = get_node_or_null("TopBar/TimeLabel")
	if not location_label: location_label = get_node_or_null("LocationBadge/LocationLabel")
	if not btn_menu: btn_menu = get_node_or_null("BtnMenu")
	if not quest_label: quest_label = get_node_or_null("QuestPanel/QuestLabel")
	if not resource_label: resource_label = get_node_or_null("ResourcePanel/ResourceLabel")
	if not toast_panel: toast_panel = get_node_or_null("ToastPanel")
	if not toast_label: toast_label = get_node_or_null("ToastPanel/ToastLabel")
	if not dialogue_panel: dialogue_panel = get_node_or_null("DialoguePanel")
	if not dialogue_name: dialogue_name = get_node_or_null("DialoguePanel/VBoxContainer/SpeakerName")
	if not dialogue_text: dialogue_text = get_node_or_null("DialoguePanel/VBoxContainer/DialogueText")
	if not hotbar_container: hotbar_container = get_node_or_null("HotbarContainer")
	if not shop_panel: shop_panel = get_node_or_null("ShopPanel")
	if not shop_coins_label: shop_coins_label = get_node_or_null("ShopPanel/MarginContainer/VBoxContainer/ShopCoinsLabel")
	if not shop_produce_label: shop_produce_label = get_node_or_null("ShopPanel/MarginContainer/VBoxContainer/ShopProduceLabel")
	if not inventory_panel: inventory_panel = get_node_or_null("InventoryPanel")
	if not inv_coins_label: inv_coins_label = get_node_or_null("InventoryPanel/MarginContainer/VBoxContainer/InvCoinsLabel")
	if not label_seeds_inv: label_seeds_inv = get_node_or_null("InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot3/LabelSeedsInv")
	if not label_hay_inv: label_hay_inv = get_node_or_null("InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot5/LabelHayInv")
	if not label_crop_inv: label_crop_inv = get_node_or_null("InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot6/LabelCropInv")
	if not label_egg_inv: label_egg_inv = get_node_or_null("InventoryPanel/MarginContainer/VBoxContainer/ScrollContainer/ItemsList/Slot7/LabelEggInv")

func set_hud_visible(show_hud: bool) -> void:
	_ensure_nodes()
	if time_label and time_label.get_parent():
		time_label.get_parent().visible = show_hud
	if location_label and location_label.get_parent():
		location_label.get_parent().visible = show_hud
	if resource_label and resource_label.get_parent():
		resource_label.get_parent().visible = show_hud
	if quest_label and quest_label.get_parent():
		quest_label.get_parent().visible = show_hud
	if hotbar_container:
		hotbar_container.visible = show_hud
	if btn_menu:
		btn_menu.visible = show_hud

func _on_btn_menu_pressed() -> void:
	_play_ui_sound("click")
	menu_button_pressed.emit()

func setup(inv: InventoryData) -> void:
	_ensure_nodes()
	inventory = inv
	inventory.inventory_changed.connect(update_inventory_display)
	update_inventory_display()
	if toast_panel:
		toast_panel.visible = false
	if dialogue_panel:
		dialogue_panel.visible = false
	if shop_panel:
		shop_panel.visible = false
	if inventory_panel:
		inventory_panel.visible = false

func _unhandled_input(event: InputEvent) -> void:
	if fishing_active:
		if event is InputEventKey and event.pressed and not event.echo:
			if event.keycode == KEY_ESCAPE:
				_finish_fishing(false, true)
			elif fishing_bite and (event.keycode == KEY_E or event.keycode == KEY_SPACE or event.keycode == KEY_ENTER):
				_resolve_fishing()
			get_viewport().set_input_as_handled()
			return
		if fishing_bite and event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			_resolve_fishing()
			get_viewport().set_input_as_handled()
			return

	if is_inventory_menu_open:
		if event is InputEventKey and event.pressed and not event.echo:
			if event.keycode == KEY_TAB or event.keycode == KEY_ESCAPE or event.keycode == KEY_E or event.keycode == KEY_I or event.keycode == KEY_B:
				close_inventory_menu()
				get_viewport().set_input_as_handled()
				return

	if is_shop_open:
		if event is InputEventKey and event.pressed and not event.echo:
			if event.keycode == KEY_E or event.keycode == KEY_ESCAPE or event.keycode == KEY_SPACE:
				close_shop()
				get_viewport().set_input_as_handled()
				return

	if is_dialogue_open:
		if event is InputEventKey and event.pressed and not event.echo:
			if event.keycode == KEY_E or event.keycode == KEY_SPACE or event.keycode == KEY_ENTER:
				close_dialogue()
				get_viewport().set_input_as_handled()
				return

	# ESC khi không mở menu con thì phát tín hiệu mở Màn hình chính / Cài đặt
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE:
			menu_button_pressed.emit()
			get_viewport().set_input_as_handled()

func update_location(title: String) -> void:
	if location_label:
		location_label.text = title

func update_time_display(hour: int, minute: int, day_name: String, day_num: int, period: String, weather_icon: String = "☀️", weather_text: String = "Nắng ấm", temp_str: String = "30°C") -> void:
	if not time_label:
		return
	var time_str = "%02d:%02d" % [hour, minute]
	time_label.text = "%s %s - %s, %d/10 - %s (%s, %s)" % [weather_icon, time_str, day_name, day_num, period, weather_text, temp_str]

func update_inventory_display() -> void:
	if not inventory:
		return
	
	# Cập nhật tài nguyên (thêm rơm)
	if resource_label:
		resource_label.text = "💰%d  🌱%d  🌾%d  🥚%d  🌿%d  🐟%d" % [
			inventory.coins, inventory.seeds, inventory.crops_harvested, 
			inventory.eggs_collected, inventory.hay_bundles, inventory.fish_caught
		]
	
	# Cập nhật nhiệm vụ
	if quest_label:
		var q_title = ""
		match inventory.current_quest_id:
			1: q_title = "📋 Cuốc %d/%d luống đất" % [inventory.quest_progress, inventory.quest_target]
			2: q_title = "📋 Nhặt %d/%d trứng gà" % [inventory.quest_progress, inventory.quest_target]
			3: q_title = "📋 Thu hoạch %d/%d nông sản" % [inventory.quest_progress, inventory.quest_target]
			_: q_title = "✅ Hoàn thành tân thủ!"
		quest_label.text = q_title
	
	# Cập nhật hotbar active slot và số lượng trên các ô
	if hotbar_container:
		var b3 = hotbar_container.get_node_or_null("BtnTool3")
		if b3: b3.text = "3.Hạt 🌱 (%d)" % inventory.seeds
		var b5 = hotbar_container.get_node_or_null("BtnTool5")
		if b5: b5.text = "5.Rơm 🌿 (%d)" % inventory.hay_bundles
		var b6 = hotbar_container.get_node_or_null("BtnTool6")
		if b6: b6.text = "6.Bắp 🌽 (%d)" % inventory.crops_harvested
		var b7 = hotbar_container.get_node_or_null("BtnTool7")
		if b7: b7.text = "7.Trứng 🥚 (%d)" % inventory.eggs_collected

		for i in range(7):
			var btn = hotbar_container.get_node_or_null("BtnTool" + str(i + 1))
			if btn is Button:
				btn.button_pressed = (i + 1 == inventory.active_tool)

	# Cập nhật thông số trong Menu Túi Đồ
	if inv_coins_label:
		inv_coins_label.text = "💰 Tiền vàng: %d xu | Chọn ô để Trang bị / Sử dụng" % inventory.coins
	if label_seeds_inv:
		label_seeds_inv.text = "🌱 [3] Hạt Giống Nông Sản (Còn: x%d)" % inventory.seeds
	if label_hay_inv:
		label_hay_inv.text = "🌿 [5] Bó Rơm Gia Súc (Còn: x%d)" % inventory.hay_bundles
	if label_crop_inv:
		label_crop_inv.text = "🌽 [6] Bắp Ngô Thu Hoạch (Có: x%d)" % inventory.crops_harvested
	if label_egg_inv:
		label_egg_inv.text = "🥚 [7] Trứng Gà Quê (Có: x%d)" % inventory.eggs_collected

func show_toast(msg: String) -> void:
	_toast_queue.append(msg)
	if not _is_showing_toast:
		_show_next_toast()

func _process(delta: float) -> void:
	if not fishing_active:
		return
	if not fishing_bite:
		fishing_wait_timer -= delta
		if fishing_wait_timer <= 0.0:
			fishing_bite = true
			fishing_marker = randf_range(0.05, 0.95)
			fishing_marker_direction = 1.0
			fishing_target_start = randf_range(0.16, 0.68)
			_set_player_fishing_bite(true)
			fishing_gauge.set_gauge("CÁ CẮN CÂU! Canh kim vào vùng xanh.", fishing_marker, fishing_target_start, fishing_target_width)
			return
	else:
		fishing_marker += fishing_marker_direction * delta * 0.82
		if fishing_marker >= 1.0:
			fishing_marker = 1.0
			fishing_marker_direction = -1.0
		elif fishing_marker <= 0.0:
			fishing_marker = 0.0
			fishing_marker_direction = 1.0
		fishing_gauge.set_gauge("CÁ CẮN CÂU! Canh kim vào vùng xanh.", fishing_marker, fishing_target_start, fishing_target_width)

func start_fishing(target_global_position: Vector2) -> void:
	if fishing_active or is_shop_open or is_dialogue_open:
		return
	fishing_active = true
	fishing_bite = false
	fishing_wait_timer = randf_range(1.8, 3.4)
	fishing_gauge.visible = true
	fishing_gauge.set_gauge("Đã quăng cần, chờ cá cắn câu...", 0.0, 0.0, 0.0)
	_set_player_fishing_lock(true)
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.call("start_fishing_animation", target_global_position)

func _resolve_fishing() -> void:
	var zone_end: float = fishing_target_start + fishing_target_width
	if fishing_marker >= fishing_target_start and fishing_marker <= zone_end:
		var fish_names: Array[String] = ["cá nục", "cá dìa", "cá hồng", "cá chuồn"]
		inventory.add_fish(1)
		_finish_fishing(true, false)
		show_toast("🐟 Câu được %s! Mang đến vựa cá trên đảo bán với giá 40 xu." % fish_names.pick_random())
	else:
		_finish_fishing(false, false)
		show_toast("Cá tuột mất rồi! Hãy canh kim dừng trong vùng xanh để câu trúng.")

func _finish_fishing(caught: bool, cancelled: bool) -> void:
	fishing_active = false
	fishing_bite = false
	if fishing_gauge:
		fishing_gauge.visible = false
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.call("finish_fishing_animation", caught, cancelled)
	_set_player_fishing_lock(false)
	if cancelled:
		show_toast("Đã thu cần câu.")

func _set_player_fishing_lock(locked: bool) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.set("input_blocked", locked)

func _set_player_fishing_bite(active: bool) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.call("set_fishing_bite_animation", active)

func _show_next_toast() -> void:
	if _toast_queue.is_empty():
		_is_showing_toast = false
		return
	
	if not is_instance_valid(toast_panel) or not is_instance_valid(toast_label):
		_toast_queue.clear()
		_is_showing_toast = false
		return
	
	_is_showing_toast = true
	var msg = _toast_queue.pop_front()
	toast_label.text = msg
	toast_panel.visible = true
	toast_panel.modulate.a = 1.0
	
	if toast_tween and toast_tween.is_valid():
		toast_tween.kill()
	
	toast_tween = create_tween()
	toast_tween.tween_interval(1.5)
	toast_tween.tween_property(toast_panel, "modulate:a", 0.0, 0.35)
	toast_tween.tween_callback(func():
		if is_instance_valid(toast_panel):
			toast_panel.visible = false
		_show_next_toast()
	)

func open_dialogue(speaker: String, text: String) -> void:
	if not dialogue_panel:
		return
	is_dialogue_open = true
	dialogue_name.text = speaker
	dialogue_text.text = text
	dialogue_panel.visible = true

func close_dialogue() -> void:
	is_dialogue_open = false
	if dialogue_panel:
		dialogue_panel.visible = false

func _play_ui_sound(type: String = "click") -> void:
	if not is_inside_tree():
		return
	var audio = get_tree().root.get_node_or_null("Main/AudioManager")
	if audio:
		if type == "harvest":
			audio.play_harvest()
		elif type == "toggle":
			audio.play_toggle()
		else:
			audio.play_click()

func _on_tool_button_pressed(tool_idx: int) -> void:
	_play_ui_sound("click")
	if inventory:
		inventory.set_active_tool(tool_idx)
		show_toast("Đã chọn: %s" % get_tool_name(tool_idx))

# -------------------------------------------------------------
# QUẢN LÝ TIỆM HẠT GIỐNG CHỢ QUÊ (SHOP MENU)
# -------------------------------------------------------------
func open_shop() -> void:
	if not shop_panel:
		return
	fish_market_open = false
	_set_fish_market_layout(false)
	is_shop_open = true
	update_shop_display()
	shop_panel.visible = true

func close_shop() -> void:
	is_shop_open = false
	fish_market_open = false
	_set_fish_market_layout(false)
	if shop_panel:
		shop_panel.visible = false

func update_shop_display() -> void:
	if not inventory:
		return
	if shop_coins_label:
		shop_coins_label.text = "💰 Số xu hiện có: %d xu" % inventory.coins
	if shop_produce_label:
		if fish_market_open:
			shop_produce_label.text = "🐟 Cá đã câu: %d con" % inventory.fish_caught
		else:
			shop_produce_label.text = "🌾 %d bắp | 🥚 %d trứng | 🐟 %d cá" % [inventory.crops_harvested, inventory.eggs_collected, inventory.fish_caught]

func open_fish_shop() -> void:
	if not shop_panel:
		return
	fish_market_open = true
	_set_fish_market_layout(true)
	is_shop_open = true
	update_shop_display()
	shop_panel.visible = true

func _set_fish_market_layout(fish_only: bool) -> void:
	var title: Label = get_node_or_null("ShopPanel/MarginContainer/VBoxContainer/ShopTitle")
	var sell_button: Button = get_node_or_null("ShopPanel/MarginContainer/VBoxContainer/BtnSellAll")
	for node_path in ["LabelSeeds", "SeedButtons", "LabelHay", "HayButtons", "HSeparator1"]:
		var node = get_node_or_null("ShopPanel/MarginContainer/VBoxContainer/" + node_path)
		if node is CanvasItem:
			node.visible = not fish_only
	if title:
		title.text = "🐟 VỰA CÁ ĐẢO NGỌC - CHÚ SÁU" if fish_only else "🏮 TIỆM HẠT GIỐNG CHỢ QUÊ - CÔ ÚT"
	if sell_button:
		sell_button.text = "💰 Bán cá (+40 xu/con)" if fish_only else "💰 Bán nông sản, trứng và cá (cá 40 xu/con)"

func _on_buy_seeds_pressed(amount: int, cost_per_unit: int = 5) -> void:
	if not inventory:
		return
	var total_cost = amount * cost_per_unit
	if inventory.coins >= total_cost:
		inventory.coins -= total_cost
		inventory.seeds += amount
		inventory.inventory_changed.emit()
		update_shop_display()
		show_toast("🌱 Đã mua %d gói hạt giống (-%d xu)!" % [amount, total_cost])
	else:
		show_toast("❌ Không đủ xu! Cần %d xu." % total_cost)

func _on_buy_hay_pressed(amount: int, cost_per_unit: int = 4) -> void:
	if not inventory:
		return
	var total_cost = amount * cost_per_unit
	if inventory.coins >= total_cost:
		inventory.coins -= total_cost
		inventory.hay_bundles += amount
		inventory.inventory_changed.emit()
		update_shop_display()
		show_toast("🌿 Đã mua %d bó rơm gia súc (-%d xu)!" % [amount, total_cost])
	else:
		show_toast("❌ Không đủ xu! Cần %d xu." % total_cost)

func _on_sell_all_pressed() -> void:
	if not inventory:
		return
	if fish_market_open:
		if inventory.fish_caught == 0:
			show_toast("Bạn chưa câu được cá nào để bán!")
			return
		var market_fish_sold: int = inventory.fish_caught
		var fish_earned: int = market_fish_sold * 40
		inventory.fish_caught = 0
		inventory.add_coins(fish_earned)
		update_shop_display()
		show_toast("💰 Đã bán %d con cá, thu về +%d xu!" % [market_fish_sold, fish_earned])
		return
	if inventory.crops_harvested == 0 and inventory.eggs_collected == 0 and inventory.fish_caught == 0:
		show_toast("Chưa có nông sản, trứng hoặc cá nào để bán!")
		return
	var fish_sold: int = inventory.fish_caught
	var earned = inventory.crops_harvested * 25 + inventory.eggs_collected * 15 + fish_sold * 40
	var crops_sold = inventory.crops_harvested
	var eggs_sold = inventory.eggs_collected
	inventory.coins += earned
	inventory.crops_harvested = 0
	inventory.eggs_collected = 0
	inventory.fish_caught = 0
	inventory.inventory_changed.emit()
	update_shop_display()
	show_toast("💰 Đã bán %d bắp, %d trứng và %d cá, thu về +%d xu!" % [crops_sold, eggs_sold, fish_sold, earned])

# -------------------------------------------------------------
# QUẢN LÝ MENU TÚI ĐỒ VÀ CÁC Ô VẬT PHẨM (INVENTORY PANEL)
# -------------------------------------------------------------
func toggle_inventory_menu() -> void:
	if is_inventory_menu_open:
		close_inventory_menu()
	else:
		open_inventory_menu()

func open_inventory_menu() -> void:
	if not inventory_panel:
		return
	is_inventory_menu_open = true
	update_inventory_display()
	inventory_panel.visible = true

func close_inventory_menu() -> void:
	is_inventory_menu_open = false
	if inventory_panel:
		inventory_panel.visible = false

func select_tool_and_close(tool_id: int) -> void:
	if inventory:
		inventory.set_active_tool(tool_id)
		show_toast("Đã trang bị: %s" % get_tool_name(tool_id))
	close_inventory_menu()

func get_tool_name(tool_id: int) -> String:
	match tool_id:
		1: return "1. Cuốc Đất ⛏️"
		2: return "2. Bình Tưới 💧"
		3: return "3. Hạt Giống 🌱"
		4: return "4. Liềm Gặt 🌾"
		5: return "5. Bó Rơm 🌿"
		6: return "6. Bắp Ngô 🌽"
		7: return "7. Trứng Gà 🥚"
		_: return "Vật phẩm"

func _on_inventory_use_crop() -> void:
	if not inventory:
		return
	if inventory.consume_crop():
		if is_inside_tree():
			var tree = get_tree()
			if tree:
				var player = tree.get_first_node_in_group("player")
				if player and player.has_method("apply_speed_buff"):
					player.apply_speed_buff(1.30, 15.0)
		show_toast("🌽 Đã ăn 1 bắp ngô nướng! Nhận bùa tăng +30% tốc độ chạy trong 15 giây!")
		update_inventory_display()
	else:
		show_toast("❌ Bạn không có bắp ngô nào trong túi để ăn!")

func _on_inventory_use_egg() -> void:
	if not inventory:
		return
	if inventory.consume_egg():
		if is_inside_tree():
			var tree = get_tree()
			if tree:
				var player = tree.get_first_node_in_group("player")
				if player and player.has_method("apply_speed_buff"):
					player.apply_speed_buff(1.25, 12.0)
		show_toast("🥚 Đã ăn 1 quả trứng gà quê! Nhận bùa tăng +25% tốc độ chạy trong 12 giây!")
		update_inventory_display()
	else:
		show_toast("❌ Bạn không có quả trứng nào trong túi để ăn!")
