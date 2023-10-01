import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
