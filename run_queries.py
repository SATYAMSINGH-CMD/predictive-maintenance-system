import sqlite3
import pandas as pd

# Open our connection to the database vault
conn = sqlite3.connect('factory_vault.db')

# We lowered the threshold to 311.0 Kelvin so it captures the actual hot rows
sql_query = """
WITH Overheating_Alerts AS (
    SELECT 
        Type,
        Torque,
        Machine_Failure
    FROM milling_telemetry
    WHERE Process_Temp > 311.0
)
SELECT 
    Type,
    COUNT(*) as Total_Overheat_Events,
    SUM(Machine_Failure) as Actual_Breakdowns,
    ROUND(AVG(Torque), 2) as Avg_Torque_During_Overheat
FROM Overheating_Alerts
GROUP BY Type;
"""

# Execute the query and display the results cleanly using Pandas
result_df = pd.read_sql_query(sql_query, conn)

print("=== RISK ANALYSIS REPORT: OVERHEATING MACHINES BY VARIANT ===")
if result_df.empty:
    print("No data found. Try lowering the temperature threshold further!")
else:
    print(result_df.to_string(index=False))

# Close connection safely
conn.close()