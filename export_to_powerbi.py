import sqlite3
import pandas as pd

# Pull the advanced features from our SQL database
conn = sqlite3.connect('factory_vault.db')
df = pd.read_sql_query("SELECT * FROM milling_features", conn)
conn.close()

# Save it as a CSV file so Power BI can ingest it instantly
df.to_csv('powerbi_factory_data.csv', index=False)
print("Data successfully packaged into 'powerbi_factory_data.csv' for Power BI import!")
