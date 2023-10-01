import os
import csv
import pandas as pd
from collections import Counter
import glob
import matplotlib.pyplot as plt

def classify_subject(high_freq, low_freq, high_rt, low_rt):
    if high_freq > low_freq:
        if high_rt < low_rt:
            return "Risk-Taker & Impulsive"
        else:
            return "Risk-Taker & Deliberative"
    else:
        if high_rt < low_rt:
            return "Risk-Averse & Impulsive"
        else:
            return "Risk-Averse & Deliberative"

def get_IGT_metrics(file_path):
    df = pd.read_csv(file_path, sep=' ', names=['reaction_time', 'button_clicked', 'fee_paid', 'pre_click_bank', 'post_click_bank', 'amount_won', 'fee_to_pay'])
    risk_mapping = {1: 'high', 2: 'high', 3: 'low', 4: 'low'}
    df['risk'] = df['button_clicked'].map(risk_mapping)
    freq = Counter(df['risk'])
    reaction_times = df.groupby('risk')['reaction_time'].mean()
    return freq['high'], freq['low'], reaction_times['high'], reaction_times['low']

folder_path = r"C:\Users\user\Desktop\Raz\Practicum\ana data\IGT_ANA_DATA"
file_pattern = os.path.join(folder_path, "*.txt")
all_files = glob.glob(file_pattern)

results = []

for file_path in all_files:
    file_name = os.path.basename(file_path)
    high_freq, low_freq, high_rt, low_rt = get_IGT_metrics(file_path)
    classification = classify_subject(high_freq, low_freq, high_rt, low_rt)
    results.append([file_name, high_freq, low_freq, high_rt, low_rt, classification])

# Write results to a CSV file
with open('IGT_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['File Name', 'High-risk Frequency', 'Low-risk Frequency', 'High-risk Avg Reaction Time', 'Low-risk Avg Reaction Time', 'Classification'])
    writer.writerows(results)

# Convert results to DataFrame for plotting
results_df = pd.DataFrame(results, columns=['File Name', 'High-risk Frequency', 'Low-risk Frequency', 'High-risk Avg Reaction Time', 'Low-risk Avg Reaction Time', 'Classification'])

# Plotting the High-risk and Low-risk Frequencies
results_df[['High-risk Frequency', 'Low-risk Frequency']].plot(kind='bar')
plt.title('High-risk vs Low-risk Frequencies')
plt.xlabel('Subjects')
plt.ylabel('Frequency')
plt.show()
