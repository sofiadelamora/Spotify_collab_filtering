import json
import os

parent_dir = "data/track_outs"
with open(f"{parent_dir}/0000000-99.json") as jsonfile:
    audio_data = json.load(jsonfile)

for filename in sorted(os.listdir(parent_dir)):
    if filename == "0000000-99.json":
        continue
    with open(f"{parent_dir}/{filename}") as jsonfile:
        new_audio_data = json.load(jsonfile)
        for key, datum in new_audio_data.items():
            audio_data[key] = datum

# with open("track_audio_data.json", "w") as outfile:
#     outfile.write(json.dumps(audio_data, indent=1))

