import json
import requests

# GitHub repo details
REPO_OWNER = "Razeen-Shaikh"
REPO_NAME = "dailyCodingProblem"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues?state=all"

# Fetch GitHub issues
response = requests.get(API_URL, headers={"Accept": "application/vnd.github.v3+json"})

if response.status_code == 200:
    issues = response.json()

    problems = []
    company_list = ["Amazon", "Google", "Microsoft", "Uber", "Apple", "Pivotal", "Twitter", "Square", "JaneStreet"]
    difficulty_levels = ["Easy", "Medium", "Hard"]

    for issue in issues:
        if "pull_request" in issue:
            continue
        title = issue["title"]
        url = issue["html_url"]
        labels = [label["name"] for label in issue.get("labels", [])]

        # Extract Companies
        companies = [label for label in labels if label in company_list]

        # Extract Difficulty
        difficulty = next((label for label in labels if label in difficulty_levels), "Unknown")

        # Extract Status
        status = "Solved" if issue["state"] == "closed" else "InProgress"

        problems.append({
            "title": title,
            "url": url,
            "companies": companies,
            "difficulty": difficulty,
            "status": status
        })

    # Save to problems.json
    with open("problems.json", "w") as file:
        json.dump(problems, file, indent=4)

    print("✅ Successfully fetched and saved problem data from GitHub!")

else:
    print(f"❌ Failed to fetch GitHub issues: {response.status_code}")
