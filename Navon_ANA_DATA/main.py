import pandas as pd
import glob
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

def classify_navon_subject(global_freq, local_freq, global_rt, local_rt):
    if global_freq > local_freq:
        if global_rt < local_rt:
            return "Global-Focused & Fast"
        else:
            return "Global-Focused & Slow"
    else:
        if local_rt < global_rt:
            return "Local-Focused & Fast"
        else:
            return "Local-Focused & Slow"

# Specify the pattern for the files
file_pattern = r"C:\Users\user\Desktop\Raz\Practicum\ana data\Navon_ANA_DATA\*.txt"

# Adjust the path to match your directory
file_list = glob.glob(file_pattern)

# Initialize results list
results = []

# Loop over all files and append their data to the dataframe
for file in file_list:
    # Keep the full file name
    full_file_name = os.path.basename(file)

    df = pd.read_csv(file, sep=' ', names=['letter', 'target_level', 'target_level_num', 'status', 'reaction_time'])

    # Level mapping
    level_mapping = {0: 'none', 1: 'local', 2: 'global'}
    df['level'] = df['target_level_num'].map(level_mapping)

    # Update counters and reaction times lists for each level
    counters = {'none': Counter(), 'local': Counter(), 'global': Counter()}
    reaction_times = {'none': [], 'local': [], 'global': []}
    for level in ['none', 'local', 'global']:
        counters[level].update(df[df['level'] == level]['status'])
        reaction_times[level].extend(df[(df['level'] == level) & (df['status'] == 1)]['reaction_time'])

    # Calculate total frequencies and average reaction times
    global_freq = counters['global'][1]
    local_freq = counters['local'][1]
    global_rt = np.mean(reaction_times['global']) if reaction_times['global'] else None
    local_rt = np.mean(reaction_times['local']) if reaction_times['local'] else None

    # Classify the subject
    if global_rt is not None and local_rt is not None:
        classification = classify_navon_subject(global_freq, local_freq, global_rt, local_rt)
    else:
        classification = "Insufficient Data"

    # Append to results
    results.append([full_file_name, global_freq, local_freq, global_rt, local_rt, classification])

# Write results to a CSV file
with open('Navon results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['File Name', 'Global Frequency', 'Local Frequency', 'Global Avg Reaction Time', 'Local Avg Reaction Time', 'Classification'])
    writer.writerows(results)

# Convert results to DataFrame for plotting
results_df = pd.DataFrame(results, columns=['File Name', 'Global Frequency', 'Local Frequency', 'Global Avg Reaction Time', 'Local Avg Reaction Time', 'Classification'])

# Plotting the Global and Local Frequencies
results_df[['Global Frequency', 'Local Frequency']].plot(kind='bar')
plt.title('Global vs Local Frequencies')
plt.xlabel('Subjects')
plt.ylabel('Frequency')
plt.show()
