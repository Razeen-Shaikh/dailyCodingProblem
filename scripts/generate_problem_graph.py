import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# File paths
PROBLEMS_FILE = "problems.json"
README_FILE = "README.md"
STATS_IMAGE = "stats.png"

# Define colors for companies
COMPANY_COLORS = {
    "Amazon": "orange", "Google": "blue", "Microsoft": "green", "Uber": "black",
    "Apple": "gray", "Pivotal": "teal", "Twitter": "lightblue", "Square": "purple",
    "JaneStreet": "red"
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
except json.JSONDecodeError:
    raise ValueError("Error: problems.json is not a valid JSON file.")

# Convert to DataFrame
df = pd.DataFrame(problems)
if df.empty:
    raise ValueError("Error: No problems data found in problems.json.")
df["companies"] = df["companies"].apply(lambda x: x if isinstance(x, list) else ["Unknown"])
df = df.explode("companies", ignore_index=True)

# Group data by company
company_stats = (
    df.groupby("companies")["status"]
    .agg(total="count", solved=lambda x: (x == "Solved").sum())
    .reset_index()
)
company_stats["unsolved"] = company_stats["total"] - company_stats["solved"]
company_stats.sort_values(by="total", ascending=False, inplace=True)

# Create visualization (Vertical Bar Chart)
plt.style.use('default')
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('white')

# Use company-specific colors or default color
bar_colors = [COMPANY_COLORS.get(company, DEFAULT_COLOR) for company in company_stats["companies"]]

bars_solved = ax.bar(company_stats["companies"], company_stats["solved"], color=bar_colors, label="Solved", alpha=0.8)
bars_unsolved = ax.bar(company_stats["companies"], company_stats["unsolved"], bottom=company_stats["solved"], color="#e74c3c", label="Unsolved", alpha=0.8)

ax.set_xlabel("Company", fontsize=12, fontweight='bold')
ax.set_ylabel("Number of Problems", fontsize=12, fontweight='bold')
ax.set_title("Problem Statistics by Company", fontsize=14, fontweight='bold', y=1.05)

# Rotate x-axis labels for better visibility
ax.set_xticks(range(len(company_stats["companies"])))
ax.set_xticklabels(company_stats["companies"], rotation=45, ha="right")

# Add value labels on bars
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2, f'{int(height)}', ha='center', va='center', fontsize=9)

add_value_labels(bars_solved)
add_value_labels(bars_unsolved)

ax.grid(True, axis='y', linestyle='--', alpha=0.7)
ax.legend(loc='upper right', fontsize=10)

for spine in ax.spines.values():
    spine.set_linewidth(0.5)
    spine.set_color('#666666')

plt.tight_layout()
plt.savefig(STATS_IMAGE, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()


# Generate Markdown Table
markdown_table = """## 📊 Problem Statistics

<div align="center">

<table>
<tr>
    <td style="vertical-align: top; padding-right: 20px;">
    <table>
        <tr><th>Company</th><th>Total</th><th>Solved</th><th>Unsolved</th></tr>
"""

for _, row in company_stats.iterrows():
    solved_status = "✅" if row['solved'] > 0 else "❌"
    unsolved_status = "✅" if row['unsolved'] == 0 else "❌"
    markdown_table += f"<tr><td>{row['companies']}</td><td>{row['total']}</td><td>{solved_status} {row['solved']}</td><td>{unsolved_status} {row['unsolved']}</td></tr>\n"

markdown_table += """</table>
    </td>
    <td style="text-align: center;">
        <img src="stats.png" width="600px" alt="Problem Statistics">
    </td>
</tr>
</table>

</div>
"""

# Update README.md
try:
    if os.path.exists(README_FILE):
        with open(README_FILE, "r") as file:
            content = file.read()

        content = re.sub(r"## 📊 Problem Statistics.*", markdown_table, content, flags=re.DOTALL)

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