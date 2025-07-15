import numpy as np
import pandas as pd

test_sample_human = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110',
    'Screen Resolution': '1920x1080',
    'OS': 'Windows 10',
    'Language': 'en-US',
    'CPU/GPU Specs': 'Intel Core i7, NVIDIA GeForce GTX 1660',
    'Browser Fingerprinting': 'Unique',
    'Plugins': 'PDF Viewer, Shockwave Flash',
    'Canvas Fingerprint': 'Unique Hash',
    'Timezone': 'UTC+1',
    'IP Address (Masked)': '192.168.x.x',
    'Connection Speed': '100 Mbps',
    'Proxy/VPN Detection': 'Not Detected',
    'Mouse Movement Patterns': 'Smooth, Curved Movements',
    'Click Timings': '[0.8, 2.1, 1.5]',
    'Scroll Depth': 'Partial Scroll',
    'Touch Pressure': 'Natural Touch',
    'Page Load Time': '[2.1, 3.5, 1.8]',
    'Dwell Time': '[15.2, 22.3, 45.1]',
    'Inactivity Patterns': 'Periodic Inactivity',
    'Keystroke Dynamics': 'Occasional Errors',
    'Small Pointer Movements': 'Small Adjustments'
}

flat_sample = test_sample_human.copy()


# Create DataFrame
df_test = pd.DataFrame([flat_sample])

# Ensure df_test has the same columns as used during training
for column in X_train.columns:
    if column not in df_test.columns:
        df_test[column] = 0  # Or np.nan

# Encode categorical values using previously fitted LabelEncoders
for column in df_test.columns:
    if column in label_encoders:
        le = label_encoders[column]
        try:
            df_test[column] = le.transform(df_test[column])
        except ValueError:
            unseen_labels = list(set(df_test[column]) - set(le.classes_))
            print(f"Warning: Unseen label(s) {unseen_labels} in column '{column}'. Adding them.")
            le.classes_ = np.append(le.classes_, unseen_labels)
            df_test[column] = le.transform(df_test[column])

# Reorder columns
df_test = df_test[X_train.columns]

# Predict
prediction = model.predict(df_test)
print(f"Prediction for Human Sample: {prediction[0]}")