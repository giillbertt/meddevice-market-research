import sqlite3
import pandas as pd

conn = sqlite3.connect("MedDevice.db")

# Question 1: Which device categories have the most clearances 
# BUT also the most adverse events? (Risk vs Market Activity)
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

df1 = pd.read_sql_query(query1, conn)
pd.set_option('display.max_colwidth', None)
print("Risk Ratio by Device Category:")
print(df1.to_string())

# Question 2: R&D spending vs revenue for each company over time
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

df2 = pd.read_sql_query(query2, conn)
print("\nR&D Intensity by Company:")
print(df2.to_string())

# Question 3: Which companies dominate clinical trials pipeline?
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

df3 = pd.read_sql_query(query3, conn)
print("\nTop Companies in Clinical Trial Pipeline:")
print(df3.to_string())

# Question 4: Market Opportunity Score
# Combines clearance volume + trial activity + safety profile
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

df4 = pd.read_sql_query(query4, conn)
print("\nMarket Opportunity Score by Category:")
print(df4.to_string())