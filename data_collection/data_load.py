#Import libraries
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


FEATURES = ['name', 'collab', 'pid', 'modified_at', 'num_tracks', 'albums', 'followers', 'tracks']
#Read json files with playlists
begin = 0
split = 1000

song_index = 0
track_map = {}
track_info = {}
playlist_info = []
path = lambda x, d : f"dataset/mpd.slice.{x}-{x+d-1}.json"

while begin + split <= 1000000:
    print(f"In file: {begin}")
    with open(path(begin, split), 'r') as json_file:
        playlist_file = json.load(json_file)
        for playlist in playlist_file['playlists']:
            track_list = []
            for track in playlist['tracks']:
                if track['track_uri'] not in track_map:
                    track_map[track['track_uri']] = song_index
                    del track['pos']
                    track_info[song_index] = track
                    song_index += 1
                track_list.append(track_map[track['track_uri']])
            playlist['tracks'] = track_list
            playlist_info.append(playlist)
        begin += 1000

with open('playlist_data.json', 'w') as outfile:
    outfile.write(json.dumps(playlist_info, indent=1))

with open('track_map.json', 'w') as outfile:
    outfile.write(json.dumps(track_map, indent=1))

with open('track_data.json', 'w') as outfile:
    outfile.write(json.dumps(track_info, indent=1))

# print(playlist_info)
#     playlist = pd.concat([playlist, pd.DataFrame.from_dict(file['playlists'], orient='columns')], ignore_index = True)
#     begin += 1000