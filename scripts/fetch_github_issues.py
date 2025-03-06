import json
import requests

repo_owner = "Razeen-Shaikh"
repo_name = "dailyCodingProblem"
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?state=all"

response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})

if response.status_code == 200:
    issues = response.json()

    problems = []
    for issue in issues:
        company_tags = [label["name"] for label in issue.get("labels", []) if label["name"] in ["Amazon", "Google", "Microsoft", "Uber", "Apple", "Pivotal", "Twitter", "Square", "Jane Street"]]
        solved = issue["state"] == "closed"

        problems.extend(
            {"company": company, "solved": solved} for company in company_tags
        )
    # Save to problems.json
    with open("problems.json", "w") as file:
        json.dump(problems, file, indent=4)

    print("✅ Successfully fetched and saved problem data from GitHub!")
else:
    print(f"❌ Failed to fetch GitHub issues: {response.status_code}")
