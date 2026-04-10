import sqlite3
import pandas as pd

conn = sqlite3.connect("meddevice.db")

# Pull our three summary tables
df_yearly = pd.read_sql_query("""
    SELECT decision_year, COUNT(*) AS clearances
    FROM fda_510k
    WHERE decision_year IS NOT NULL
    GROUP BY decision_year
    ORDER BY decision_year
""", conn)

df_categories = pd.read_sql_query("""
    SELECT advisory_committee_description AS category, 
           COUNT(*) AS clearances
    FROM fda_510k
    GROUP BY category
    ORDER BY clearances DESC
""", conn)

df_companies = pd.read_sql_query("""
    SELECT applicant AS company, 
           COUNT(*) AS clearances
    FROM fda_510k
    GROUP BY company
    ORDER BY clearances DESC
    LIMIT 20
""", conn)

# Write all three to separate sheets in one Excel file
with pd.ExcelWriter("meddevice_market_research.xlsx", engine="openpyxl") as writer:
    df_yearly.to_excel(writer, sheet_name="Yearly Clearances", index=False)
    df_categories.to_excel(writer, sheet_name="Device Categories", index=False)
    df_companies.to_excel(writer, sheet_name="Top Companies", index=False)

print("Excel file saved: meddevice_market_research.xlsx")
conn.close()