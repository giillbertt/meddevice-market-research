# 🏥 Medical Device Market Research
### An end-to-end data analytics project using Python, SQL, Power BI, and Excel

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-Summary-217346?style=flat&logo=microsoftexcel&logoColor=white)

---

## 📌 Project Overview

This project answers a real market research question:

> **What does the US medical device market look like — who's entering, where the risk is, and who's investing in the future?**

Using four real public APIs, I collected over **11,000 records** across device clearances, safety reports, clinical trials, and company financials — then cleaned, stored, analyzed, and visualized the data into a full market intelligence report.

---

## 🗂️ Data Sources

| Dataset | Source | Records | Description |
|---|---|---|---|
| FDA 510(k) Clearances | [openFDA API](https://api.fda.gov/device/510k.json) | 5,000 | Device market entry approvals 2015–2026 |
| FDA MAUDE Adverse Events | [openFDA API](https://api.fda.gov/device/event.json) | 4,155 | Device safety incident reports |
| Clinical Trials | [ClinicalTrials.gov API](https://clinicaltrials.gov/api/v2/studies) | 981 | FDA-regulated device trials |
| Company Financials | [SEC EDGAR API](https://data.sec.gov/api/xbrl/) | 1,206 | Revenue, net income, R&D for 10 major companies |

---

## 🏗️ Project Pipeline

```
API Calls (Python) → Clean & Store (SQLite) → Analyze (SQL) → Visualize (Python/Matplotlib) → Dashboard (Power BI) → Report (Excel)
```

---

## 📁 Repository Structure

```
meddevice-market-research/
│
├── 01_collect_fda_510k.py          # FDA 510(k) clearance data collection
├── 02_collect_adverse_events.py    # FDA MAUDE adverse event collection
├── 02b_clean_adverse_events.py     # Adverse event cleaning & filtering
├── 03_collect_trials.py            # ClinicalTrials.gov data collection
├── 04_collect_sec.py               # SEC EDGAR financial data collection
├── 05_load_sql.py                  # Load all datasets into SQLite
├── 06_cross_analysis.py            # Cross-dataset SQL analysis
├── 07_visualize.py                 # Python charts (Matplotlib)
├── 08_export_powerbi.py            # Export CSVs for Power BI
├── 09_excel_summary.py             # Excel summary workbook
│
├── data/
│   ├── raw/                        # Raw CSVs from APIs
│   ├── clean/                      # Cleaned CSVs
│   └── powerbi_ready/              # Aggregated CSVs for Power BI
│
├── screenshots/
│   └── dashboard.png               # Power BI dashboard screenshot
│
├── requirements.txt
└── README.md
```

---

## 🔍 Key Findings

### 1. Market Entry Trends
- **2017** was the peak year with **119 clearances**
- A **−44% drop** from 2017 to 2019 coinciding with COVID disruption
- Strong **+62% recovery** from 2020 to 2023
- Market remains **fragmented** — no single company dominates

### 2. Risk Analysis (Clearances vs Adverse Events)
| Category | Clearances | Adverse Events | Risk Ratio |
|---|---|---|---|
| Clinical Chemistry | 138 | 658 | **4.77 ⚠️** |
| General Hospital | 393 | 272 | 0.69 |
| Orthopedic | 782 | 190 | 0.24 |
| Cardiovascular | 575 | 118 | 0.21 |
| Radiology | 651 | 10 | **0.02 ✅** |

> Clinical Chemistry has nearly **5 adverse events per clearance** — the highest risk category by far.

### 3. Market Opportunity Score
A composite score combining clearance volume, active trial pipeline, and safety profile:

```
Score = (Clearances ÷ 100) + (Active Trials × 2) − (Adverse Events × 0.05)
```

| Rank | Category | Score | Why |
|---|---|---|---|
| #1 | **Dental** | 16.1 | 10 active trials — highest pipeline activity |
| #2 | **Radiology** | 10.0 | 651 clearances, risk ratio of just 0.02 |
| #3 | **Orthopedic** | 4.3 | Highest volume but moderate risk |

### 4. R&D Investment
- **Edwards Lifesciences** leads at **19.4% R&D intensity** (2024)
- Industry average clusters around **6–7%**
- **Dexcom** shows classic growth-phase behavior — heavy R&D spending with negative net income
- **Intuitive Surgical** consistently invests 12–14% — signals sustained innovation focus

---

## 📊 SQL Analysis Highlights

The project includes 12 SQL queries across 4 tables, including cross-dataset joins:

```sql
-- Risk ratio: adverse events per clearance by device category
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
```

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/[your-handle]/meddevice-market-research.git
cd meddevice-market-research
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Collect data (runs all API calls)
```bash
python 01_collect_fda_510k.py
python 02_collect_adverse_events.py
python 02b_clean_adverse_events.py
python 03_collect_trials.py
python 04_collect_sec.py
```

### 4. Load into SQL and analyze
```bash
python 05_load_sql.py
python 06_cross_analysis.py
```

### 5. Generate charts and exports
```bash
python 07_visualize.py
python 08_export_powerbi.py
python 09_excel_summary.py
```

### 6. Open Power BI
Connect Power BI Desktop to the CSVs in `data/powerbi_ready/` and open the `.pbix` file.

---

## 📦 Requirements

```
requests
pandas
matplotlib
seaborn
sqlalchemy
openpyxl
tqdm
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|---|---|
| **Python** | API data collection, cleaning, EDA, visualization |
| **SQLite** | Data storage, cross-dataset SQL analysis |
| **Power BI** | Interactive market intelligence dashboard |
| **Excel** | Stakeholder-ready summary workbook |

---

## 👤 Author

**Ignatius Gilbert Wicaksana**
Biomedical Engineering Graduate — Universitas Gadjah Mada

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/[your-handle])
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/[your-handle])

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

> **Data disclaimer:** All data used in this project is sourced from US government public APIs (FDA, SEC, ClinicalTrials.gov). No proprietary or private data was used.
