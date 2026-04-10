import requests
import time
import csv

url = "https://api.fda.gov/device/510k.json"

all_records = []

limit = 100
totalFetch = 5000

for skip in range(0, totalFetch, limit):
    print(f'Fetching records {skip}, to {skip + limit}...')
    params = {
        "limit": limit,
        "skip": skip,
        "search": "decision_date:[2015-01-01 TO 2026-12-31]"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        records = data.get("results", [])

        if not records:
            print("No more records available, stopping.")
            break

        all_records.extend(records)
    except Exception as e:
        print(f'Error at skip {skip}: {e}')
        continue

    time.sleep(0.5)

print(f"\nDone. Total records collected: {len(all_records)}")

# print(all_records[0].get("applicant"))
# print(all_records[0].get("device_name"))

fields = ["k_number", "applicant", "device_name", "decision_date", 
          "country_code", "product_code", "advisory_committee_description",
          "decision_description", "clearance_type", "state", "city"]

with open("fda_510k.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(all_records)

print("Saved to fda_510k.csv")