import requests
import base64
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

secret = "<SECRET HERE>"
id = "<ID HERE>"

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())



with open('track_data.json') as jsonfile:
    song_data = json.load(jsonfile)

buffer = []
uris = []
writeset = {}
start_dex = 332500
for song in song_data.items():
    key = song[0]
    if int(key) < start_dex:
        continue
    uri = song[1]["track_uri"]
    buffer.append(key)
    uris.append(uri)
    if len(buffer) >= 100:
        try:
            auto_feats = sp.audio_features(tracks=uris)
        except requests.exceptions.ReadTimeout:
            try:
                time.sleep(10)
                auto_feats = sp.audio_features(tracks=uris)
            except requests.exceptions.ReadTimeout:
                print(start_dex)
                exit()
        for i in range(len(auto_feats)):
            audio_set = auto_feats[i]
            if audio_set is None:
                writeset[buffer[i]] = None
                continue
            for feat in ["type", "uri", "track_href", "analysis_url"]:
                del audio_set[feat]
            writeset[buffer[i]] = audio_set
        with open(f'track_outs/{start_dex:07d}-{start_dex+99}.json', 'w') as write_file:
            write_file.write(json.dumps(writeset, indent=1)) 
        buffer = []
        writeset = {}
        uris = []
        start_dex += 100
        time.sleep(1)


