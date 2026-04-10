import sqlite3
import pandas as pd
df = pd.read_csv("fda_510k.csv")

df["decision_date"] = pd.to_datetime(df["decision_date"], errors="coerce")

df["decision_year"] = df["decision_date"].dt.year

conn = sqlite3.connect("MedDevice.db")

df.to_sql("fda_510k", conn, if_exists="replace", index=False)

print("Loaded successfully")

result = conn.execute("SELECT COUNT(*) FROM fda_510k").fetchone()
print(f'Rows in database: {result[0]}')

conn.close()