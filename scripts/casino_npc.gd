extends NPCVillager
class_name CasinoNPC

@export_enum("Bài Tây", "Poker", "Bi-da") var game_kind: String = "Bài Tây"

func interact(inventory: InventoryData, ui: Node) -> void:
	if inventory == null:
		return

	if game_kind == "Bi-da":
		var shots := randi_range(0, 3)
		if shots > 0:
			var reward := shots * 5
			inventory.add_coins(reward)
			_show_result(ui, "🎱 Bạn đánh trúng %d bi và nhận %d xu!" % [shots, reward])
		else:
			_show_result(ui, "🎱 Bi trượt mất rồi. Thử ngắm kỹ hơn nhé!")
		return

	var bet := 10 if game_kind == "Bài Tây" else 20
	if inventory.coins < bet:
		_show_result(ui, "Bạn cần ít nhất %d xu để vào bàn %s." % [bet, game_kind])
		return

	inventory.coins -= bet
	inventory.inventory_changed.emit()
	if game_kind == "Bài Tây":
		var player_card := randi_range(1, 13)
		var dealer_card := randi_range(1, 13)
		if player_card > dealer_card:
			inventory.add_coins(bet * 2)
			_show_result(ui, "🂡 Bạn rút %d, nhà cái rút %d. Bạn thắng %d xu!" % [player_card, dealer_card, bet])
		elif player_card == dealer_card:
			inventory.add_coins(bet)
			_show_result(ui, "🂡 Hai bên cùng %d điểm, hoàn lại tiền cược." % player_card)
		else:
			_show_result(ui, "🂡 Bạn rút %d, nhà cái rút %d. Ván này thua %d xu." % [player_card, dealer_card, bet])
	else:
		var hand := randi_range(1, 100)
		if hand >= 72:
			inventory.add_coins(bet * 3)
			_show_result(ui, "♠️ Poker: bài mạnh! Bạn thắng %d xu." % (bet * 2))
		else:
			_show_result(ui, "♠️ Poker: đối thủ có bài cao hơn. Bạn mất %d xu." % bet)

func _show_result(ui: Node, message: String) -> void:
	if ui and ui.has_method("show_toast"):
		ui.show_toast(message)
