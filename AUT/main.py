import pandas as pd
import matplotlib.pyplot as plt


# Define the functions for Flexibility, Originality, and Elaboration
def count_unique_categories(idea_list):
    return len(set(idea_list))  # Placeholder

def calculate_originality(idea_list):
    return sum([1 for idea in idea_list if idea not in ['common_idea1', 'common_idea2']])  # Placeholder

def calculate_elaboration(idea_list):
    return sum([len(idea.split()) for idea in idea_list])  # Placeholder

# Read the CSV file
df = pd.read_csv("C:\\Users\\user\\Desktop\\Raz\\Practicum\\ana data\\AUT\\AUT_results.csv", encoding='ISO-8859-1')

# Initialize an empty DataFrame to store the results
results_df = pd.DataFrame()

# Loop through each unique Subject_ID
for subject_id in df['Subject_ID'].unique():
    # Filter the DataFrame for each subject
    subject_df = df[df['Subject_ID'] == subject_id]

    # Initialize a dictionary to store the metrics for each subject
    metrics = {'Subject_ID': subject_id}

    # Initialize variable to store the total divergent thinking score
    total_divergent_score = 0

    # Calculate the metrics for each idea column (Paperclip, Shoe, Brick, Pen, Spoon)
    for idea_column in ['Paperclip', 'Shoe', 'Brick', 'Pen', 'Spoon']:
        # Split the string into a list based on commas
        idea_list = subject_df[idea_column].iloc[0].split(',')

        # Fluency: The number of other uses you can think of
        fluency = len(idea_list)
        metrics[f'{idea_column}_Fluency'] = fluency

        # Flexibility: Count unique categories
        flexibility = count_unique_categories(idea_list)
        metrics[f'{idea_column}_Flexibility'] = flexibility

        # Originality: Calculate originality
        originality = calculate_originality(idea_list)
        metrics[f'{idea_column}_Originality'] = originality

        # Elaboration: Calculate elaboration
        elaboration = calculate_elaboration(idea_list)
        metrics[f'{idea_column}_Elaboration'] = elaboration

        # Calculate the divergent thinking score for this idea column
        divergent_score = (fluency + flexibility + originality + elaboration) / 4.0
        metrics[f'{idea_column}_DivergentScore'] = divergent_score

        # Add to the total divergent thinking score
        total_divergent_score += divergent_score

    # Calculate the average divergent thinking score across all idea columns
    metrics['Total_DivergentScore'] = total_divergent_score / 5.0

    # Append the metrics to the results DataFrame
    results_df = pd.concat([results_df, pd.DataFrame([metrics])], ignore_index=True)

# Save the results to a new CSV file
results_df.to_csv("C:\\Users\\user\\Desktop\\Raz\\Practicum\\ana data\\AUT\\AUT_Analysis.csv", index=False)

# Plotting the Total Divergent Scores
results_df['Total_DivergentScore'].plot(kind='hist', bins=20)
plt.title('Distribution of Total Divergent Scores')
plt.xlabel('Total Divergent Score')
plt.ylabel('Frequency')
plt.show()
