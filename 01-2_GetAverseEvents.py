import requests
import time
import csv

url = "https://api.fda.gov/device/event.json"
limit = 100
totalFetch = 5000
rows = []

for skip in range(0, totalFetch, limit):
    print(f'Fetching records {skip} to {skip + limit}...')
    params = {
        "limit": limit,
        "skip": skip,
        "search": "date_received:[20151201 TO 20260101]"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("results", [])

        if not records:
            print("No more records available.")
            break

        # PROCESS EACH RECORD IMMEDIATELY
        for rec in records:
            # Safe extraction of nested data
            devices = rec.get("device", [{}])
            device = devices[0] if devices else {}
            
            patients = rec.get("patient", [{}])
            patient = patients[0] if patients else {}
            
            openfda = device.get("openfda", {})
            outcomes = patient.get("sequence_number_outcome", [])

            rows.append({
                "report_number":    rec.get("report_number"),
                "event_type":       rec.get("event_type"),
                "event_location":   rec.get("event_location"),
                "date_of_event":    rec.get("date_of_event"),
                "date_received":    rec.get("date_received"),
                "adverse_flag":     rec.get("adverse_event_flag"),
                "device_name":      device.get("generic_name"),
                "brand_name":       device.get("brand_name"),
                "manufacturer":     device.get("manufacturer_d_name"),
                "product_code":     device.get("device_report_product_code"),
                "device_category":  openfda.get("medical_specialty_description"),
                "device_class":     openfda.get("device_class"),
                "outcome":          outcomes[0] if outcomes else "Unknown",
                "patient_age":      patient.get("patient_age"),
            })

    except Exception as e:
        print(f'Error at skip {skip}: {e}')
        # If the API fails once, we continue to the next skip
        continue

    time.sleep(0.5)

print(f"\nDone. Total records collected: {len(rows)}")

# Save to CSV
if rows:
    fields = list(rows[0].keys())
    with open("fda_adverse_events.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("Saved to fda_adverse_events.csv")
else:
    print("No data was collected. Check your internet connection or API URL.")