import pandas as pd
import glob
from collections import Counter
import matplotlib.pyplot as plt

# Specify the pattern for the files
file_pattern = r"C:\Users\user\Desktop\Raz\Practicum\IGT_ANA_DATA\*.txt"

# Adjust the path to match your directory
file_list = glob.glob(file_pattern)
print(file_list)

# Initialize an empty dataframe to store all data
all_data = pd.DataFrame()

# Loop over all files and append their data to the dataframe
for file in file_list:
    df = pd.read_csv(file, sep=' ', names=['reaction_time', 'button_clicked', 'fee_paid', 'pre_click_bank', 'post_click_bank', 'amount_won', 'fee_to_pay'])
    all_data = all_data.append(df, ignore_index=True)

# Now you have a dataframe (`all_data`) containing data from all your text files

# High risk is 1 or 2, Low risk is 3 or 4
risk_mapping = {1: 'high', 2: 'high', 3: 'low', 4: 'low'}
all_data['risk'] = all_data['button_clicked'].map(risk_mapping)

# Calculate frequencies
freq = Counter(all_data['risk'])
avg_freq = all_data.groupby('risk')['button_clicked'].mean()


print('Frequency of high-risk vs low-risk decisions:')
print('High-risk:', freq['high'])
print('Low-risk:', freq['low'])
print('\nAverage Frequency for high-risk vs low-risk decisions:')
print('High-risk:', avg_freq['high'])
print('Low-risk:', avg_freq['low'])

# Calculate average reaction times for high-risk and low-risk decisions
reaction_times = all_data.groupby('risk')['reaction_time'].mean()

print('\nAverage reaction times for high-risk vs low-risk decisions:')
print('High-risk:', reaction_times['high'])
print('Low-risk:', reaction_times['low'])

# Bar plot for frequency of decisions
plt.figure(figsize=(10, 5))
plt.bar(freq.keys(), freq.values(), color=['red', 'blue'])
plt.xlabel('Risk Type')
plt.ylabel('Frequency')
plt.title('Frequency of High-risk vs Low-risk Decisions')
plt.show()

# Bar plot for average reaction times
plt.figure(figsize=(10, 5))
plt.bar(reaction_times.index, reaction_times.values, color=['red', 'blue'])
plt.xlabel('Risk Type')
plt.ylabel('Average Reaction Time')
plt.title('Average Reaction Times for High-risk vs Low-risk Decisions')
plt.show()
