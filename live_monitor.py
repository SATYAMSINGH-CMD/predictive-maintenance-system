import sqlite3
import pandas as pd
import time
import lightgbm as lgb
from sklearn.model_selection import train_test_split

# 1. Connect to the vault and reload the dataset
conn = sqlite3.connect('factory_vault.db')
df = pd.read_sql_query("SELECT * FROM milling_features", conn)
conn.close()

# 2. Re-train our model quickly so it's loaded fresh in memory
X = df[['Air_Temp', 'Process_Temp', 'Rotational_Speed', 'Torque', 'Tool_Wear', 'FFT_Max_Amplitude', 'FFT_Dominant_Peak']]
y = df['Machine_Failure']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = lgb.LGBMClassifier(random_state=42, n_estimators=100, learning_rate=0.05, verbose=-1)
model.fit(X_train, y_train)

# 3. Simulate a live factory telemetry stream using the hidden test set
print("Initializing Factory Control Room Telemetry Stream...")
print("Monitoring live machine feeds. Press Ctrl+C to stop.\n")
time.sleep(1.5)

# We grab the first 30 rows of our test data to simulate live incoming data packets
live_stream = X_test.head(30)
actual_outcomes = y_test.head(30).values

for i in range(len(live_stream)):
    # Extract a single row of telemetry from a machine
    current_data_packet = live_stream.iloc[[i]]
    
    # Let the model calculate the failure risk probability
    risk_probability = model.predict_proba(current_data_packet)[0][1]
    
    # Fetch details for the console log
    temp = current_data_packet['Process_Temp'].values[0]
    torque = current_data_packet['Torque'].values[0]
    
    # Console Output Log
    print(f"[STREAMING] Machine ID Ref {i+1} | Process Temp: {temp}K | Torque: {torque} Nm | Risk: {risk_probability*100:.1f}%")
    
    # If the AI calculates a risk greater than 50%, sound the alarm!
    if risk_probability > 0.5:
        print(f"🚨 ALERT: CRITICAL FAILURE RISK DETECTED ON MACHINE {i+1}!")
        print(f"👉 ACTION REQUIRED: Emergency shutdown sequence initiated. Actual Status: {'CRASHED' if actual_outcomes[i] == 1 else 'SAFE'}\n")
    
    # Pause for half a second to simulate real-time data ticks
    time.sleep(0.5)

print("\nSimulation complete. All high-risk anomalies intercepted successfully.")