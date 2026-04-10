import sqlite3
import pandas as pd

df = pd.read_csv("clinical_trials.csv")

# Clean up dates
df["start_date"]      = pd.to_datetime(df["start_date"],      errors="coerce")
df["completion_date"] = pd.to_datetime(df["completion_date"], errors="coerce")
df["enrollment"]      = pd.to_numeric(df["enrollment"],       errors="coerce")

# Load to SQL
conn = sqlite3.connect("MedDevice.db")
df.to_sql("clinical_trials", conn, if_exists="replace", index=False)

result = conn.execute("SELECT COUNT(*) FROM clinical_trials").fetchone()
print(f"Rows in database: {result[0]}")
conn.close()