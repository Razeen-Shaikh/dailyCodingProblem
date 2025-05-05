import json
import requests
from datetime import datetime

# GitHub repo details
REPO_OWNER = "Razeen-Shaikh"
REPO_NAME = "dailyCodingProblem"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues?state=all&per_page=100&page="

def fetch_all_issues(api_url):
    issues = []
    page = 1

    while True:
        response = requests.get(api_url + str(page), headers={"Accept": "application/vnd.github.v3+json"}, timeout=10)

        if response.status_code == 200:
            page_issues = response.json()
            if not page_issues:
                break
            issues.extend(page_issues)
            page += 1
        elif response.status_code == 403:
            retry_after = response.headers.get("Retry-After")
            print(f"⚠️ Rate limit hit on page {page}. Retry after {retry_after or 'some time'}.")
            break
        else:
            print(f"❌ Error on page {page}: {response.status_code}")
            break

    return issues

# Reference lists
company_list = ["Amazon", "Google", "Microsoft", "Uber", "Apple", "Pivotal", "Twitter", "Square", "JaneStreet", "Stripe", "Airbnb", "Facebook"]
difficulty_levels = ["Easy", "Medium", "Hard"]

# Fetch issues
issues = fetch_all_issues(API_URL)
problems = []

for issue in issues:
    if "pull_request" in issue:
        continue

    title = issue["title"]
    url = issue["html_url"]
    labels = [label["name"] for label in issue.get("labels", [])]

    # Extract structured fields
    companies = [label for label in labels if label in company_list]
    difficulty = next((label for label in labels if label in difficulty_levels), "Unknown")
    status = "Solved" if issue["state"] == "closed" else "InProgress"
    tags = [label for label in labels if label not in company_list + difficulty_levels]
    date_added = issue.get("created_at", "")[:10]  # yyyy-mm-dd format
    notes = (issue.get("body") or "").strip() or "—"

    problems.append({
        "title": title,
        "url": url,
        "companies": companies,
        "difficulty": difficulty,
        "status": status,
        "tags": tags,
        "date_added": date_added,
        "notes": notes
    })

# Save to JSON
with open("problems.json", "w") as f:
    json.dump(problems, f, indent=4)

print("✅ Successfully fetched and saved enriched problems to problems.json")
