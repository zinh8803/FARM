extends Node

const PATCH_INDEX_PATH := "user://patches/installed_patches.json"

func _init() -> void:
	# Load patches before the main scene preloads scripts/scenes from res://.
	if not FileAccess.file_exists(PATCH_INDEX_PATH):
		return
	var index_file := FileAccess.open(PATCH_INDEX_PATH, FileAccess.READ)
	if index_file == null:
		return
	var index_data = JSON.parse_string(index_file.get_as_text())
	index_file.close()
	if not index_data is Dictionary:
		push_error("Installed patch index is invalid.")
		return
	var patch_files: Array = index_data.get("files", [])
	for patch_name in patch_files:
		var file_name := str(patch_name)
		if file_name.get_file() != file_name or not file_name.to_lower().ends_with(".pck"):
			push_error("Invalid patch filename: %s" % file_name)
			return
		var patch_path := ProjectSettings.globalize_path("user://patches/" + file_name)
		if not FileAccess.file_exists(patch_path):
			push_error("Installed patch is missing: %s" % patch_path)
			return
		if not ProjectSettings.load_resource_pack(patch_path, true):
			push_error("Could not load installed patch: %s" % patch_path)
			return
		print("Loaded game patch: ", file_name)
