import json
import pandas as pd
import matplotlib.pyplot as plt
import os

# 📂 File Paths
PROBLEMS_FILE = "problems.json"
README_FILE = "README.md"
STATS_IMAGE = "stats.png"

# 🎨 Define Colors for Companies
COMPANY_COLORS = {
    "Amazon": "orange",
    "Google": "blue",
    "Microsoft": "green",
    "Uber": "black",
    "Apple": "gray",
    "Pivotal": "teal",
    "Twitter": "lightblue",
    "Square": "purple",
    "JaneStreet": "red",
}
DEFAULT_COLOR = "blue"  # Fallback color

# 📌 Difficulty & Status Colors
DIFFICULTY_COLORS = {"Easy": "brightgreen", "Medium": "orange", "Hard": "red"}
STATUS_COLORS = {"Solved": "success", "InProgress": "yellow"}

# 🚀 Load Problems Data
try:
    with open(PROBLEMS_FILE, "r") as file:
        problems = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    print("❌ Error: Could not load problems.json.")
    exit(1)

# 🗂 Convert to DataFrame
df = pd.DataFrame(problems)
df = df.explode("companies")  # Handle multiple companies per problem

# 🔍 Group Data by Company
company_stats = (
    df.groupby("companies")["status"]
    .agg(Total="count", Solved=lambda x: (x == "Solved").sum())
    .reset_index()
)
company_stats["Unsolved"] = company_stats["Total"] - company_stats["Solved"]
company_stats = company_stats.sort_values(by="Total", ascending=False)  # Sort for better visualization

# 🔥 Stacked Horizontal Bar Chart
fig, ax = plt.subplots(figsize=(8, 5))

ax.barh(company_stats["companies"], company_stats["Unsolved"], color="#FF6347", label="Unsolved")  # Red
ax.barh(company_stats["companies"], company_stats["Solved"], color="#4CAF50", label="Solved", left=company_stats["Unsolved"])  # Green

# 📌 Labels & Styling
ax.set_xlabel("Number of Problems")
ax.set_ylabel("Company")
ax.set_title("Problem Statistics by Company")
ax.legend()
plt.tight_layout()

# 📷 Save Graph
plt.savefig(STATS_IMAGE, dpi=300)
plt.close()
print(f"✅ Graph saved as {STATS_IMAGE}")

# 📋 Generate Problems Table
markdown_table = (
    "| Problem | Companies | Difficulty | Status |\n"
    "|---------|-----------|------------|--------|\n"
)
for problem in problems:
    company_badges = " ".join(
        [
            f"![{company}](https://img.shields.io/badge/-{company}-{COMPANY_COLORS.get(company, DEFAULT_COLOR)}?style=flat&logo={company.lower()})"
            for company in problem["companies"]
        ]
    )
    difficulty_badge = f"![{problem['difficulty']}](https://img.shields.io/badge/Difficulty-{problem['difficulty'].replace(' ', '%20')}-{DIFFICULTY_COLORS.get(problem['difficulty'], 'lightgray')}?style=flat)"
    status_badge = f"![{problem['status']}](https://img.shields.io/badge/Status-{problem['status']}-{STATUS_COLORS.get(problem['status'], 'lightgray')}?style=flat)"

    markdown_table += f"| [{problem['title']}]({problem['url']}) | {company_badges} | {difficulty_badge} | {status_badge} |\n"

# 🔄 Update Problems Table in README
try:
    with open(README_FILE, "r") as readme_file:
        content = readme_file.readlines()

    start_index = next(
        (i for i, line in enumerate(content) if "Problem" in line and "Companies" in line and "Difficulty" in line and "Status" in line),
        None
    )

    if start_index is None:
        print("⚠️ Problems table not found in README.md. Appending new table.")
        updated_content = content + ["\n" + markdown_table]
    else:
        end_index = start_index + 1
        while end_index < len(content) and content[end_index].strip().startswith("|"):
            end_index += 1
        updated_content = content[:start_index] + [line + "\n" for line in markdown_table.split("\n")] + content[end_index:]

    with open(README_FILE, "w") as readme_file:
        readme_file.writelines(updated_content)

    print("✅ README.md successfully updated with new problem list.")

except FileNotFoundError:
    print("⚠️ README.md not found. Creating a new one with the problem list.")
    with open(README_FILE, "w") as file:
        file.write(markdown_table)

print("🚀 Script execution completed successfully!")
