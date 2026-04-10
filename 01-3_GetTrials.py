import requests
import csv
import time

all_records = []
seen_ids = set()

search_terms = [
    "medical device implant",
    "orthopedic device",
    "cardiovascular device",
    "surgical device",
    "diagnostic device",
    "neurology device",
    "dental device",
    "radiology device",
]

print("Fetching clinical trials data...")

for term in search_terms:
    print(f"\nSearching: '{term}'")
    next_page_token = None
    term_count = 0

    while term_count < 1000:
        url = "https://clinicaltrials.gov/api/v2/studies"
        params = {
            "query.term": term,
            "pageSize": 100,
            "format": "json"
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        try:
            r = requests.get(url, params=params, timeout=15)
            data = r.json()

            studies = data.get("studies", [])
            if not studies:
                print("  No studies returned.")
                break

            for s in studies:
                proto       = s.get("protocolSection", {})
                id_mod      = proto.get("identificationModule", {})
                status_mod  = proto.get("statusModule", {})
                design_mod  = proto.get("designModule", {})
                sponsor_mod = proto.get("sponsorCollaboratorsModule", {})
                oversight   = proto.get("oversightModule", {})

                nct_id = id_mod.get("nctId")
                if not nct_id or nct_id in seen_ids:
                    continue
                seen_ids.add(nct_id)

                if not oversight.get("isFdaRegulatedDevice"):
                    continue

                all_records.append({
                    "nct_id":          nct_id,
                    "title":           id_mod.get("briefTitle"),
                    "status":          status_mod.get("overallStatus"),
                    "start_date":      status_mod.get("startDateStruct", {}).get("date"),
                    "completion_date": status_mod.get("completionDateStruct", {}).get("date"),
                    "phase":           ", ".join(design_mod.get("phases", [])),
                    "enrollment":      design_mod.get("enrollmentInfo", {}).get("count"),
                    "study_type":      design_mod.get("studyType"),
                    "sponsor":         sponsor_mod.get("leadSponsor", {}).get("name"),
                    "sponsor_class":   sponsor_mod.get("leadSponsor", {}).get("class"),
                    "fda_regulated":   oversight.get("isFdaRegulatedDevice"),
                })

            term_count += len(studies)
            print(f"  Unique trials so far: {len(all_records)}")

            # Get next page token from root level
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                print("  No more pages for this term.")
                break

            time.sleep(0.3)

        except Exception as e:
            print(f"  Error: {e}")
            break

    if len(all_records) >= 5000:
        print("\nReached 5000 records, stopping.")
        break

print(f"\nDone. Total unique trials: {len(all_records)}")

if all_records:
    fields = list(all_records[0].keys())
    with open("clinical_trials.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_records)
    print("Saved to clinical_trials.csv")