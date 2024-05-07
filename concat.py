import pandas as pd

# Load the datasets
positive_df = pd.read_csv('positive_Induct.csv')
commonsense_df = pd.read_csv('commonsense.csv')

# Check and clean null values
positive_df = positive_df.dropna().reset_index(drop=True)
commonsense_df = commonsense_df.dropna().reset_index(drop=True)

# Ensure both dataframes have the same length for concatenation
min_length = min(len(positive_df), len(commonsense_df))
positive_df = positive_df.head(min_length)
commonsense_df = commonsense_df.head(min_length)

# Concatenate the sentences with "!!" at the end
result_df = positive_df['Positive'] + ' ' + commonsense_df['Commonsense'] + '!!'

# Save the concatenated data to a new CSV file
result_df.to_csv('concatenated_sentences.csv', index=False)

print("Concatenation complete. Results saved to 'concatenated_sentences.csv'.")
