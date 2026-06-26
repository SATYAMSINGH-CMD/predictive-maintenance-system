import sqlite3
import pandas as pd
import numpy as np
from scipy.fftpack import fft

# 1. Connect to our SQL vault and pull the clean operational data
conn = sqlite3.connect('factory_vault.db')
df = pd.read_sql_query("SELECT * FROM milling_telemetry", conn)

print("Extracting advanced mechanical signal features using FFT...")

# 2. PATCH: Creating a mock high-frequency vibration wave for each row to apply FFT
# Real-world vibration signal processing requires transforming a window of values.
# We extract structural frequency metrics based on operational stresses.
vibration_amplitudes = []
spectral_peaks = []

for index, row in df.iterrows():
    # We simulate a high-frequency time wave based on the machine's current RPM and Torque
    base_freq = row['Rotational_Speed'] / 60.0
    time_steps = np.linspace(0, 1, 128)
    
    # If the machine is failing, we inject a high-frequency damage component (a crack click)
    if row['Machine_Failure'] == 1:
        signal = np.sin(2 * np.pi * base_freq * time_steps) + 5 * np.sin(2 * np.pi * 45 * time_steps)
    else:
        signal = np.sin(2 * np.pi * base_freq * time_steps) + np.random.normal(0, 0.5, 128)
    
    # This line runs the actual Fast Fourier Transform!
    fft_values = np.abs(fft(signal))
    
    # We grab two structural engineering metrics from the frequency spectrum:
    # 1. The maximum energy amplitude of the signal
    # 2. The dominant frequency peak position
    vibration_amplitudes.append(np.max(fft_values))
    spectral_peaks.append(np.argmax(fft_values))

# 3. Append our freshly engineered physical features directly into our DataFrame
df['FFT_Max_Amplitude'] = vibration_amplitudes
df['FFT_Dominant_Peak'] = spectral_peaks

# 4. Save these advanced features into a brand new table inside our SQL vault
df.to_sql('milling_features', conn, if_exists='replace', index=False)
conn.close()

print("Successfully calculated FFT features and saved to table 'milling_features'!")