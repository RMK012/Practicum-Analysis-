import os
import csv
import pandas as pd


# Function to get IAT scores
def get_scores(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
        last_line = lines[-1]
        values = last_line.split()

        IAT_score = float(values[0])
        IAT_D_score = float(values[1])
        perc_faster_300ms = float(values[2])

        return IAT_score, IAT_D_score, perc_faster_300ms


# Function to classify subjects based on IAT D Score
def classify_subject(iat_d_score):
    if iat_d_score > 0.65:
        return 'Strongly racially biased'
    elif 0.35 < iat_d_score <= 0.65:
        return 'Moderately racially biased'
    elif 0.15 < iat_d_score <= 0.35:
        return 'Slightly racially biased'
    else:
        return 'No significant bias'


folder_path = r"C:\Users\user\Desktop\Raz\Practicum\IAT_ANA_DATA"
all_files = os.listdir(folder_path)

results = []
for file_name in all_files:
    if file_name.endswith(".txt"):
        file_path = os.path.join(folder_path, file_name)
        IAT_score, IAT_D_score, perc_faster_300ms = get_scores(file_path)

        # Classify the subject based on IAT D Score
        classification = classify_subject(IAT_D_score)

        results.append([file_name, IAT_score, IAT_D_score, perc_faster_300ms, classification])

# Write results to a CSV file
with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['File Name', 'IAT Score', 'IAT D Score', 'Percentage faster than 300ms', 'IAT Classification'])
    writer.writerows(results)

# Load the data into a DataFrame
df = pd.read_csv('results.csv')

# Normalize the D Scores using Min-Max normalization
min_d_score = df['IAT D Score'].min()
max_d_score = df['IAT D Score'].max()
df['Normalized D Score'] = (df['IAT D Score'] - min_d_score) / (max_d_score - min_d_score)

# Save the DataFrame back to 'results.csv' with the new column
df.to_csv('results.csv', index=False)
