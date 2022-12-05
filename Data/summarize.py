import json
import os


ORD_FEATURES = ["danceability", "energy", "loudness", "mode", "speechiness",
            "acousticness", "liveness", "valence", "tempo", "duration_ms"]

CAT_FEATURES = {
    "time_signature": ["0", "1", "3", "4", "5"],
    "key": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
}

with open("track_audio_data.json") as jsonfile:
    track_audio_data = json.load(jsonfile)

with open("playlist_data.json") as jsonfile:
    playlist_data = json.load(jsonfile)

playlist_summaries = {}

def playlist_summary(playlist, audio_data):
    total_tracks = playlist["num_tracks"]
    audio_summary = dict.fromkeys(ORD_FEATURES, 0)
    for feat, values in CAT_FEATURES.items():
        for value in values:
            audio_summary[f"{feat}_{value}"] = 0
    for track_num in playlist["tracks"]:
        try:
            track_audio_feats = audio_data[str(track_num)]
        except KeyError:
            continue

        if track_audio_feats is None:
            total_tracks -= 1
            continue
        for feat, val in track_audio_feats.items():
            if feat in CAT_FEATURES:
                audio_summary[f"{feat}_{val}"] += 1
            elif feat in ORD_FEATURES:
                audio_summary[feat] += val
            
    for feat in audio_summary.keys():
        audio_summary[feat] = round(audio_summary[feat] / total_tracks, 5)
    return audio_summary

for playlist in playlist_data:
    playlist_summaries[playlist["pid"]] = playlist_summary(playlist, track_audio_data)

with open("playlist_summaries.json", "w") as outfile:
    outfile.write(json.dumps(playlist_summaries, indent=1))