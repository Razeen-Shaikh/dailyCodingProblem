import json

# Example data structure for tracking solved problems
with open("problems.json", "r") as file:
    problems = json.load(file)

company_stats = {}

for p in problems:
    company = p["company"]
    if company not in company_stats:
        company_stats[company] = {"total": 0, "solved": 0}
    company_stats[company]["total"] += 1
    if p["solved"]:
        company_stats[company]["solved"] += 1

table = (
    "| Company | Total Problems | Solved | Unsolved |\n"
    + "|---------|---------------|--------|----------|\n"
)
for company, stats in company_stats.items():
    unsolved = stats["total"] - stats["solved"]
    table += f"| {company} | {stats['total']} | {stats['solved']} ✅ | {unsolved} ❌ |\n"

# Read the README.md file
readme_path = "../README.md"

with open(readme_path, "r") as file:
    content = file.readlines()

if start_index := next(
    (
        i
        for i, line in enumerate(content)
        if "| Company | Total Problems | Solved | Unsolved |" in line
    ),
    None,
):
    end_index = start_index
    while end_index < len(content) and "|" in content[end_index]:
        end_index += 1

    # Replace old table with new one
    content = content[:start_index] + table.split("\n") + content[end_index:]

    # Write updated content back to README.md
    with open(readme_path, "w") as file:
        file.writelines("\n".join(content))

    print("✅ README.md updated successfully!")
else:
    print("⚠️ Table not found in README.md. Make sure it exists.")
