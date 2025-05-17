import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import logging

# File paths
PROBLEMS_FILE = "../problems.json"
README_FILE = "../README.md"
STATS_IMAGE = "../stats.png"

# Define colors for companies
COMPANY_COLORS = {
    "Amazon": "orange", "Google": "blue", "Microsoft": "green", "Uber": "black",
    "Apple": "gray", "Pivotal": "teal", "Twitter": "lightblue", "Square": "purple",
    "JaneStreet": "red", "Stripe": "#635BFF",
    "Facebook": "#3b5998", "Airbnb": "#ff5a60"
}
DEFAULT_COLOR = "blue"

# Colors for difficulty and status
DIFFICULTY_COLORS = {"Easy": "brightgreen", "Medium": "orange", "Hard": "red"}
STATUS_COLORS = {"Solved": "success", "InProgress": "yellow"}

# Load problems data
if not os.path.exists(PROBLEMS_FILE):
    raise FileNotFoundError(f"Error: {PROBLEMS_FILE} does not exist.")

try:
    with open(PROBLEMS_FILE, "r") as file:
        problems = json.load(file)
except json.JSONDecodeError as e:
    raise ValueError("Error: problems.json is not a valid JSON file.") from e

def handle_companies(x):
    if isinstance(x, list):
        # Convert the list of companies to a comma-separated string
        return ", ".join(x)
    logging.warning("Expected list for 'companies' field but received %s. Defaulting to ['Unknown'].", type(x).__name__)
    return "Unknown"


# Convert to DataFrame
df = pd.DataFrame(problems)
if df.empty:
    raise ValueError("Error: No problems data found in problems.json.")
df["companies"] = df["companies"].apply(handle_companies)

# Group data by company
company_stats = (
    df.groupby("companies")["status"]
    .agg(total="count", solved=lambda x: (x == "Solved").sum())
    .reset_index()
)
company_stats["unsolved"] = company_stats["total"] - company_stats["solved"]
company_stats.sort_values(by="total", ascending=False, inplace=True)

# Create enhanced visualization (Stacked Bar Chart with style)
plt.style.use("seaborn-v0_8-darkgrid")
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('white')
ax.set_facecolor('#f5f7fa')

# Bar chart
bar_width = 0.6
x = range(len(company_stats))
# Define custom color per company if available
colors_solved = [COMPANY_COLORS.get(company, "#2ecc71") for company in company_stats["companies"]]
colors_unsolved = ["#e74c3c"] * len(company_stats)  # Keep red for unsolved

bars_solved = ax.bar(x, company_stats["solved"], width=bar_width, label="Solved", color=colors_solved)
bars_unsolved = ax.bar(x, company_stats["unsolved"], width=bar_width, bottom=company_stats["solved"], label="Unsolved", color=colors_unsolved)

# Annotate bars with numbers
for i, (solved, unsolved) in enumerate(zip(company_stats["solved"], company_stats["unsolved"])):
    total = solved + unsolved
    solved_pct = f"{(solved / total * 100):.0f}%"
    unsolved_pct = f"{(unsolved / total * 100):.0f}%"

    # Add both numeric and percent
    if solved > 0:
        ax.text(i, solved / 2, f"{solved}\n({solved_pct})", ha="center", va="center", fontsize=10, color="white", fontweight='bold')
    if unsolved > 0:
        ax.text(i, solved + unsolved / 2, f"{unsolved}\n({unsolved_pct})", ha="center", va="center", fontsize=10, color="white", fontweight='bold')


# Labels and title
ax.set_title("📊 Company-Wise Problem Solving Progress", fontsize=16, fontweight="bold", pad=20)
ax.set_xlabel("Company", fontsize=12, fontweight="bold", labelpad=10)
ax.set_ylabel("Number of Problems", fontsize=12, fontweight="bold", labelpad=10)

# X-axis
ax.set_xticks(x)
ax.set_xticklabels(company_stats["companies"], rotation=45, ha="right", fontsize=11)

# Grid and legend
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.legend(frameon=True, loc='upper right', fontsize=11)

# Borders
for spine in ax.spines.values():
    spine.set_visible(False)

# Save the improved graph
try:
    plt.tight_layout()
    plt.savefig(STATS_IMAGE, dpi=300, bbox_inches="tight", facecolor='white')
    plt.close()
    print("✅ Improved graph saved successfully.")
except Exception as error:
    print(f"❌ Error saving improved image {STATS_IMAGE}: {error}")

# Generate Markdown Table
markdown_table = """<!-- stats-start -->

<table style="border: none;">
    <tr><th align="left">Company</th><th align="center">Total</th><th align="center">Solved</th><th align="center">Unsolved</th></tr>
"""

for _, row in company_stats.iterrows():
    solved_status = "✅" if row['solved'] > 0 else "❌"
    unsolved_status = "✅" if row['unsolved'] == 0 else "❌"
    markdown_table += f"<tr><td>{row['companies']}</td><td align='center'>{row['total']}</td><td align='center'>{solved_status} {row['solved']}</td><td align='center'>{unsolved_status} {row['unsolved']}</td></tr>\n"

markdown_table += """</table>

<p align="left" style="margin-top: 20px;">
    <img src="stats.png" width="600px" alt="Problem Statistics">
</p>

<!-- stats-end -->
"""

# Update README.md
try:
    if os.path.exists(README_FILE):
        with open(README_FILE, "r") as file:
            content = file.read()

        content = re.sub(r"<!-- stats-start -->.*?<!-- stats-end -->", markdown_table, content, flags=re.DOTALL)

        with open(README_FILE, "w") as file:
            file.write(content)
    else:
        with open(README_FILE, "w") as file:
            file.write(markdown_table)
    print("✅ README.md updated with problem statistics.")

except FileNotFoundError:
    print("⚠️ README.md not found. Creating a new one.")
    with open(README_FILE, "w") as file:
        file.write(markdown_table)

except Exception as e:
    print(f"Error updating README.md: {e}")

print("🚀 Script execution completed successfully!")
