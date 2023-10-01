import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

folder_path = r"C:\Users\user\Desktop\Raz\Practicum\ana data\IAT_ANA_DATA"
all_files = os.listdir(folder_path)

results = []
for file_name in all_files:
    if file_name.endswith(".txt"):
        file_path = os.path.join(folder_path, file_name)
        scores = get_scores(file_path)
        results.append([file_name] + list(scores))

# Create a DataFrame from the results
df = pd.DataFrame(results, columns=['File Name', 'IAT Score', 'IAT D Score', 'Percentage faster than 300ms'])

# Normalize the D Scores using Min-Max normalization
min_d_score = df['IAT D Score'].min()
max_d_score = df['IAT D Score'].max()
df['Normalized D Score'] = (df['IAT D Score'] - min_d_score) / (max_d_score - min_d_score)

# Function to classify subjects based on Normalized D Score
def classify_subject(normalized_d_score):
    if normalized_d_score > 0.65:
        return 'Strongly racially biased'
    elif 0.35 < normalized_d_score <= 0.65:
        return 'Moderately racially biased'
    elif 0.15 < normalized_d_score <= 0.35:
        return 'Slightly racially biased'
    else:
        return 'No significant bias'

# Apply the classification function to the DataFrame
df['Classification'] = df['Normalized D Score'].apply(classify_subject)

# Write results to a CSV file
df.to_csv('IAT results.csv', index=False)

# Plotting the Normalized D Scores
df['Normalized D Score'].plot(kind='hist', bins=20)
plt.title('Distribution of Normalized D Scores')
plt.xlabel('Normalized D Score')
plt.ylabel('Frequency')
plt.show()


# Load the data
df = pd.read_csv('results.csv')

# Normalize the D Scores using Min-Max normalization
min_d_score = df['IAT D Score'].min()
max_d_score = df['IAT D Score'].max()
df['Normalized D Score'] = (df['IAT D Score'] - min_d_score) / (max_d_score - min_d_score)

# Function to classify subjects based on Normalized D Score
def classify_subject(normalized_d_score):
    if normalized_d_score > 0.65:
        return 'Strongly racially biased'
    elif 0.35 < normalized_d_score <= 0.65:
        return 'Moderately racially biased'
    elif 0.15 < normalized_d_score <= 0.35:
        return 'Slightly racially biased'
    else:
        return 'No significant bias'

# Apply the classification function to the DataFrame
df['Classification'] = df['Normalized D Score'].apply(classify_subject)

# Count the number of subjects in each classification group and print as a dictionary
subject_count = df['Classification'].value_counts().to_dict()
print(f"Number of subjects in each classification group: {subject_count}")

# Plot 1: Normalized D values divided according to classification
plt.figure(figsize=(10, 6))
sns.boxplot(x='Classification', y='Normalized D Score', data=df)
plt.title('Distribution of Normalized D Scores by Classification')
plt.xlabel('Classification')
plt.ylabel('Normalized D Score')
plt.show()

# Plot 2: Number of subjects in each classification group
plt.figure(figsize=(10, 6))
sns.countplot(x='Classification', data=df, order=df['Classification'].value_counts().index)
plt.title('Number of Subjects by Classification')
plt.xlabel('Classification')
plt.ylabel('Number of Subjects')
plt.show()

