import requests
import csv
import time

# Major publicly traded medical device companies + their SEC CIK numbers
COMPANIES = {
    "Medtronic":            "0000064670",
    "Abbott":               "0000001800",
    "Stryker":              "0000310764",
    "Boston_Scientific":    "0000885725",
    "Becton_Dickinson":     "0000010795",
    "Zimmer_Biomet":        "0001136893",
    "Edwards_Lifesciences": "0001099800",
    "Hologic":              "0000859737",
    "Intuitive_Surgical":   "0001035267",
    "Dexcom":               "0001093691",
}

# SEC requires a User-Agent header identifying who you are
headers = {"User-Agent": "MedDevice Research student@example.com"}

rows = []

print("Fetching SEC financial data...")

for company, cik in COMPANIES.items():
    print(f"  Fetching: {company}")
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        facts = r.json().get("facts", {}).get("us-gaap", {})

        # Revenue — try multiple field names as different companies use different ones
        revenue_data = (
            facts.get("RevenueFromContractWithCustomerExcludingAssessedTax") or
            facts.get("Revenues") or
            facts.get("SalesRevenueNet") or
            {}
        )

        # Net income
        income_data = facts.get("NetIncomeLoss", {})

        # R&D spending
        rd_data = facts.get("ResearchAndDevelopmentExpense", {})

        def extract_annual(data):
            units = data.get("units", {}).get("USD", [])
            return [
                {
                    "year": u.get("end", "")[:4],
                    "value": u["val"]
                }
                for u in units
                if u.get("form") in ("10-K", "20-F")
                and u.get("end", "")[:4] >= "2015"
            ]

        for item in extract_annual(revenue_data):
            rows.append({
                "company": company,
                "year":    item["year"],
                "metric":  "Revenue",
                "value_usd": item["value"],
                "value_bn":  round(item["value"] / 1e9, 3)
            })

        for item in extract_annual(income_data):
            rows.append({
                "company": company,
                "year":    item["year"],
                "metric":  "NetIncome",
                "value_usd": item["value"],
                "value_bn":  round(item["value"] / 1e9, 3)
            })

        for item in extract_annual(rd_data):
            rows.append({
                "company": company,
                "year":    item["year"],
                "metric":  "R&D",
                "value_usd": item["value"],
                "value_bn":  round(item["value"] / 1e9, 3)
            })

        time.sleep(0.5)

    except Exception as e:
        print(f"    Error: {e}")

print(f"\nDone. Total financial records: {len(rows)}")

# Save to CSV
fields = ["company", "year", "metric", "value_usd", "value_bn"]
with open("sec_financials.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print("Saved to sec_financials.csv")