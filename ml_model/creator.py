import pandas as pd

# Load the dataset
file_path = 'combined_dataset.csv'
data = pd.read_csv(file_path)

# Identify and remove unnamed columns
unnamed_columns = [col for col in data.columns if 'Unnamed' in col or col.strip() == '']
data_cleaned = data.drop(columns=unnamed_columns)

# Save the cleaned dataset to a new file
cleaned_file_path = 'cleaned_combined_dataset.csv'
data_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Cleaned file saved as: {cleaned_file_path}")