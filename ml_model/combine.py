import pandas as pd

# Load both datasets
old_df = pd.read_csv("noisy_human_vs_bot_dataset.csv")
new_df = pd.read_csv("NEW DATASET.csv")

# Combine them
combined_df = pd.concat([old_df, new_df], ignore_index=True)

# Optional: Remove duplicates
combined_df = combined_df.drop_duplicates()

# Save to new file
combined_df.to_csv("combined_human_vs_bot_dataset.csv", index=False)

print("✅ Merged dataset saved as combined_human_vs_bot_dataset.csv")
