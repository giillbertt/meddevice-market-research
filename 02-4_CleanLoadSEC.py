import sqlite3
import pandas as pd

df = pd.read_csv("sec_financials.csv")
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["value_usd"] = pd.to_numeric(df["value_usd"], errors="coerce")
df["value_bn"] = pd.to_numeric(df["value_bn"], errors="coerce")

conn = sqlite3.connect("MedDevice.db")
df.to_sql("sec_financials", conn, if_exists="replace", index=False)

result = conn.execute("SELECT COUNT(*) FROM sec_financials").fetchone()
print(f"Rows in database: {result[0]}")
conn.close()