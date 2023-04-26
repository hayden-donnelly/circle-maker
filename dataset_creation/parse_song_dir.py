import os
import pandas as pd
import re

song_dir = "C://Users/Hayden/AppData/Local/osu!/songs/"
song_folders = os.listdir(song_dir)
osu_files = []
titles = []
artists = []

for i in range(len(song_folders)):
    song_files = os.listdir(song_dir + song_folders[i])
    
    for j in range(len(song_files)):
        if song_files[j].endswith(".osu"):
            osu_files.append(song_files[j])
            
            with open(song_dir + song_folders[i] + "/" + song_files[j], "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("Title:"):
                        titles.append(line[6:-1])
                    if line.startswith("Artist:"):
                        artists.append(line[7:-1])
    break

df = pd.DataFrame({
    'file_name:': osu_files, 
    'title': titles, 
    'artist': artists
})
print(df.head())