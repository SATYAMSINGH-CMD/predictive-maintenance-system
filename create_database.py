import sqlite3
import pandas as pd

# 1. Load the raw data from the CSV file
# We rename the columns slightly to make them clean and standard for SQL syntax
df = pd.read_csv('ai4i2020.csv')
df.columns = [
    'UDI', 'Product_ID', 'Type', 'Air_Temp', 'Process_Temp', 
    'Rotational_Speed', 'Torque', 'Tool_Wear', 'Machine_Failure',
    'TWF', 'HDF', 'PWF', 'OSF', 'RNF'
]

# 2. Establish a connection to create our local SQLite database file
conn = sqlite3.connect('factory_vault.db')
cursor = conn.cursor()

# 3. Create the structured SQL table
cursor.execute('''
CREATE TABLE IF NOT EXISTS milling_telemetry (
    UDI INTEGER PRIMARY KEY,
    Product_ID TEXT,
    Type TEXT,
    Air_Temp REAL,
    Process_Temp REAL,
    Rotational_Speed REAL,
    Torque REAL,
    Tool_Wear REAL,
    Machine_Failure INTEGER,
    TWF INTEGER,
    HDF INTEGER,
    PWF INTEGER,
    OSF INTEGER,
    RNF INTEGER
)
''')

# 4. Dump the data from pandas directly into our new SQL table
df.to_sql('milling_telemetry', conn, if_exists='replace', index=False)

# 5. Commit change and close connection safely
conn.commit()
conn.close()

print("Database 'factory_vault.db' created successfully and 10,000 rows injected into table 'milling_telemetry'!")