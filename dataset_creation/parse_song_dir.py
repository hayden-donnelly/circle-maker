import os
import pandas as pd
import re

song_dir = "C://Users/Hayden/AppData/Local/osu!/Songs/"
song_folders = os.listdir(song_dir)
osu_files = []

variable_names = [
    # General
    'AudioFilename',
    'AudioLeadIn',
    'PreviewTime',
    'Countdown',
    'SampleSet',
    'StackLeniency',
    'Mode',
    'LetterboxInBreaks',
    'WidescreenStoryboard',
    # Metadata
    'Title',
    'Artist',
    'Creator',
    'Version',
    'Tags',
    # Difficulty
    'HPDrainRate',
    'CircleSize',
    'OverallDifficulty',
    'ApproachRate',
    'SliderMultiplier',
    'SliderTickRate'
]

category_names = ['HitObjects', 'TimingPoints', 'Events', 'Colours']

# Setup data dictionary.
data = {}
data['FileName'] = []
for name in variable_names:
    data[name] = []
for name in category_names:
    data[name] = []

for i in range(len(song_folders)):
    song_files = os.listdir(song_dir + song_folders[i])
    
    for j in range(len(song_files)):
        if song_files[j].endswith(".osu"):
            data['FileName'].append(song_files[j])
            
            with open(song_dir + song_folders[i] + "/" + song_files[j], "r", encoding="utf-8") as f:
                lines = f.readlines()
                
                # Parse lines for specified variables.
                for line in lines:
                    for name in variable_names:
                        if line.startswith(name + ":"):
                            data[name].append(line[len(name) + 1:-1])
                            break
                
                # Parse lines for the starting index of specified categories.
                category_start_indices = {}
                for line in lines:
                    # Categories are surrounded by square brackets in osu files, so get rid of them.
                    potential_category = line[1:-2]
                    if potential_category in category_names:
                        print("Found category: " + potential_category)
                        category_start_indices[potential_category] = lines.index(line) + 1

                # Find the ending index of specified categories and append categories to data.
                for name in category_names:
                    # If the category start wasn't found in the initial parse, skip finding end.
                    if not name in category_start_indices.keys():
                       continue

                    category_start_index = category_start_indices[name]
                    category_end_index = category_start_index
                    for i in range(category_start_index, len(lines)):
                        if lines[i] == "\n":
                            category_end_index = i
                            break
                    data[name].append(lines[category_start_index:category_end_index])

                # Make sure there are the same number of data points for each variable.
                num_data_points = len(data['FileName'])
                for name in variable_names:
                    if len(data[name]) < num_data_points:
                        data[name].append(None)
                for name in category_names:
                    if len(data[name]) < num_data_points:
                        data[name].append(None)
            #break
    #break

df = pd.DataFrame(data)
print(df.head())
df.to_csv('../data/osu_beatmap_dataset.csv')

test_string = "title:hellowrold\n"
pattern = r"title:(.*)\n"
match = re.search(pattern, test_string)

if match:
    title = match.group(1)
    print(title)