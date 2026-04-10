import pandas as pd
import sqlite3

df = pd.read_csv("fda_adverse_events.csv", dtype=str)

# 1. Fix dates — convert YYYYMMDD to proper datetime
df["date_of_event"] = pd.to_datetime(df["date_of_event"], format="%Y%m%d", errors="coerce")
df["date_received"]  = pd.to_datetime(df["date_received"],  format="%Y%m%d", errors="coerce")

# 2. Filter to 2015-2026 only
df = df[df["date_of_event"].dt.year.between(2015, 2026)]

# 3. Extract year and month
df["event_year"]  = df["date_of_event"].dt.year
df["event_month"] = df["date_of_event"].dt.month

# 4. Clean patient age — extract just the number
df["patient_age"] = df["patient_age"].str.extract(r"(\d+)").astype(float)

# 5. Clean junk brand names
junk_values = ["N/A", "SAME AS ABOVE", "NI", "INVALID DATA", "*", ""]
df["brand_name"] = df["brand_name"].replace(junk_values, pd.NA)

# 6. Standardize event location codes
location_map = {
    "I": "Home",
    "HOSPITAL": "Hospital",
    "OTHER": "Other",
    "INVALID DATA": pd.NA
}
df["event_location"] = df["event_location"].replace(location_map)

# 7. Replace "Unknown" device category with NA
df["device_category"] = df["device_category"].replace("Unknown", pd.NA)

# 8. Drop rows with no event date or device name
df = df.dropna(subset=["date_of_event", "device_name"])

# 9. Drop duplicates
df = df.drop_duplicates(subset=["report_number"])

print(f"Clean records: {len(df)}")
print(f"\nNull counts:")
print(df.isnull().sum())

df.to_csv("fda_adverse_events_clean.csv", index=False)
print("\nSaved to fda_adverse_events_clean.csv")

conn = sqlite3.connect("MedDevice.db")
df.to_sql("fda_adverse_events", conn, if_exists="replace", index=False)

result = conn.execute("SELECT COUNT(*) FROM fda_adverse_events").fetchone()
print(f"Rows in database: {result[0]}")
conn.close()