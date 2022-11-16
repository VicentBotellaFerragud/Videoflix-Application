from content.admin import VideoResource

dataset = VideoResource().export()

videoinfos_in_json_format = dataset.json

print(videoinfos_in_json_format)
