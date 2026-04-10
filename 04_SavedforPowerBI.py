import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("MedDevice.db")

os.makedirs("powerbiData", exist_ok=True)

query1 = """
SELECT 
    c.advisory_committee_description AS category,
    COUNT(DISTINCT c.k_number)       AS clearances,
    COUNT(DISTINCT a.report_number)  AS adverse_events,
    ROUND(1.0 * COUNT(DISTINCT a.report_number) / 
          COUNT(DISTINCT c.k_number), 2) AS risk_ratio
FROM fda_510k c
LEFT JOIN fda_adverse_events a 
    ON c.product_code = a.product_code
GROUP BY category
HAVING clearances > 10
ORDER BY risk_ratio DESC
"""
pd.read_sql_query(query1, conn).to_csv("powerbiData/riskVSmarket.csv", index=False)

query2 = """
SELECT
    company,
    year,
    MAX(CASE WHEN metric = 'Revenue'   THEN value_bn END) AS revenue_bn,
    MAX(CASE WHEN metric = 'NetIncome' THEN value_bn END) AS net_income_bn,
    MAX(CASE WHEN metric = 'R&D'       THEN value_bn END) AS rd_spending_bn,
    ROUND(100.0 * MAX(CASE WHEN metric = 'R&D' THEN value_bn END) /
          NULLIF(MAX(CASE WHEN metric = 'Revenue' THEN value_bn END), 0), 1) AS rd_intensity_pct
FROM sec_financials
WHERE year >= 2015
GROUP BY company, year
ORDER BY company, year
"""
pd.read_sql_query(query2,conn).to_csv("powerbiData/rndVSrevenue.csv", index=False)

query3 = """
SELECT
    sponsor,
    sponsor_class,
    COUNT(*)                    AS total_trials,
    SUM(enrollment)             AS total_patients,
    ROUND(AVG(enrollment), 0)   AS avg_enrollment,
    COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END)   AS completed,
    COUNT(CASE WHEN status = 'RECRUITING' THEN 1 END)  AS recruiting,
    COUNT(CASE WHEN status = 'ACTIVE_NOT_RECRUITING' 
               THEN 1 END)                             AS active
FROM clinical_trials
WHERE sponsor IS NOT NULL
  AND enrollment > 0
GROUP BY sponsor, sponsor_class
HAVING total_trials >= 3
ORDER BY total_trials DESC
LIMIT 20
"""
pd.read_sql_query(query3, conn).to_csv("powerbiData/top_companies.csv", index=False)

query4 = """
SELECT
    f.advisory_committee_description AS category,
    COUNT(DISTINCT f.k_number)       AS clearances,
    COUNT(DISTINCT a.report_number)  AS adverse_events,
    ROUND(1.0 * COUNT(DISTINCT a.report_number) /
          NULLIF(COUNT(DISTINCT f.k_number), 0), 2) AS risk_ratio,
    COUNT(DISTINCT t.nct_id)         AS active_trials,
    -- Opportunity score: high clearances, low risk, high trials = attractive
    ROUND(
        (COUNT(DISTINCT f.k_number) * 1.0 / 100) +
        (COUNT(DISTINCT t.nct_id)  * 2.0) -
        (COUNT(DISTINCT a.report_number) * 0.5 / 10),
    1) AS opportunity_score
FROM fda_510k f
LEFT JOIN fda_adverse_events a
    ON f.product_code = a.product_code
LEFT JOIN clinical_trials t
    ON LOWER(t.title) LIKE '%' || LOWER(f.advisory_committee_description) || '%'
GROUP BY category
HAVING clearances > 20
ORDER BY opportunity_score DESC
LIMIT 15
"""
pd.read_sql_query(query4, conn).to_csv("powerbiData/MarketScore.csv", index=False)

print("Exported 4 files to powerbi data")
conn.close()