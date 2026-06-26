import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import lightgbm as lgb

# 1. Pull the data from our new updated SQL features table
conn = sqlite3.connect('factory_vault.db')
df = pd.read_sql_query("SELECT * FROM milling_features", conn)
conn.close()

# 2. PATCH: We add our two newly engineered FFT features to the input list!
X = df[[
    'Air_Temp', 'Process_Temp', 'Rotational_Speed', 'Torque', 'Tool_Wear',
    'FFT_Max_Amplitude', 'FFT_Dominant_Peak'
]]
y = df['Machine_Failure']

# 3. Maintain our same exact evaluation split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Train the LightGBM Classifier on the new feature space
print("Training the Advanced Predictive Maintenance Model (with FFT features)...")
model = lgb.LGBMClassifier(random_state=42, n_estimators=100, learning_rate=0.05)
model.fit(X_train, y_train)

# 5. Evaluate the final hidden test set
y_pred = model.predict(X_test)

print("\n=== UPGRADED ML MODEL PERFORMANCE ===")
print(f"Overall Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred))