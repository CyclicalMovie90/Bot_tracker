# Step 1: Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Step 2: Load dataset
file_path = "noisy_human_vs_bot_dataset.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

df = pd.read_csv(file_path)

# Step 3: Preprocess
label_encoders = {}
for column in df.columns:
    if column != "Category":
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        label_encoders[column] = le

# Encode the target
target_encoder = LabelEncoder()
df["Category"] = target_encoder.fit_transform(df["Category"].astype(str))

X = df.drop(columns=["Category"])
y = df["Category"]

# Step 4: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 6: Evaluate
y_pred = model.predict(X_test)
print(f"✅ Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\n✅ Classification Report:")
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

# Step 7: Save model, encoders
joblib.dump({
    "model": model,
    "encoders": label_encoders,
    "target_encoder": target_encoder
}, "bot_detector_bundle.joblib")

print("\n✅ Model and encoders saved as: bot_detector_bundle.joblib")
