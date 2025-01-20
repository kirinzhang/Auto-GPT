import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Set style for plots
plt.style.use('ggplot')
# Initialize lists to store data
agents = []
market_caps = []
tvl = []
holders = []
categories = []

# Data from the website (updated with latest market caps)
data = [
    {"name": "WAI Combinator", "market_cap": 9.04e6, "tvl": 0.98e6, "holders": 61188, "category": "Productivity"},
    {"name": "JAIHOZ", "market_cap": 7.99e6, "tvl": 0.95e6, "holders": 55000, "category": "Entertainment"},
    {"name": "MUSIC", "market_cap": 8.34e6, "tvl": 0.97e6, "holders": 58000, "category": "Entertainment"},
    {"name": "G.A.M.E", "market_cap": 143.38e6, "tvl": 20.55e6, "holders": 177973, "category": "Productivity"},
    {"name": "Luna", "market_cap": 51.68e6, "tvl": 9.55e6, "holders": 184522, "category": "Entertainment"},
    {"name": "aixbt", "market_cap": 526.9e6, "tvl": 8.8e6, "holders": 163956, "category": "Productivity"},
    {"name": "VaderAI", "market_cap": 68.39e6, "tvl": 2.93e6, "holders": 104992, "category": "Productivity"},
    {"name": "Acolyte", "market_cap": 37.22e6, "tvl": 1.68e6, "holders": 87731, "category": "Productivity"},
    {"name": "sekoia", "market_cap": 43.77e6, "tvl": 1.62e6, "holders": 127864, "category": "Productivity"}
]

# Process data
for item in data:
    agents.append(item["name"])
    market_caps.append(item["market_cap"])
    tvl.append(item["tvl"])
    holders.append(item["holders"])
    categories.append(item["category"])

# Create DataFrame
df = pd.DataFrame({
    'Agent': agents,
    'Market_Cap': market_caps,
    'TVL': tvl,
    'Holders': holders,
    'Category': categories
})

# Calculate basic statistics
stats = {
    'Total Market Cap': df['Market_Cap'].sum(),
    'Average Market Cap': df['Market_Cap'].mean(),
    'Median Market Cap': df['Market_Cap'].median(),
    'Max Market Cap': df['Market_Cap'].max(),
    'Min Market Cap': df['Market_Cap'].min()
}

# Market cap distribution by category
category_distribution = df.groupby('Category')['Market_Cap'].agg(['sum', 'count', 'mean'])
category_distribution = category_distribution.round(2)

# Calculate market cap ranges distribution
df['Market_Cap_Range'] = pd.cut(df['Market_Cap'], 
                               bins=[0, 5e6, 10e6, 25e6, 50e6, 100e6, float('inf')],
                               labels=['0-5M', '5-10M', '10-25M', '25-50M', '50-100M', '100M+'])
range_distribution = df['Market_Cap_Range'].value_counts().sort_index()

print("\n=== Market Cap Statistics ===")
print(f"Total Market Cap: ${stats['Total Market Cap']/1e6:.2f}M")
print(f"Average Market Cap: ${stats['Average Market Cap']/1e6:.2f}M")
print(f"Median Market Cap: ${stats['Median Market Cap']/1e6:.2f}M")
print(f"Max Market Cap: ${stats['Max Market Cap']/1e6:.2f}M (Agent: {df.loc[df['Market_Cap'].idxmax(), 'Agent']})")
print(f"Min Market Cap: ${stats['Min Market Cap']/1e6:.2f}M (Agent: {df.loc[df['Market_Cap'].idxmin(), 'Agent']})")

print("\n=== Market Cap Distribution by Category ===")
print("Category | Total Market Cap | Number of Agents | Average Market Cap")
print("-" * 65)
for category in category_distribution.index:
    total = float(category_distribution.loc[category, 'sum'])
    count = int(category_distribution.loc[category, 'count'])
    mean = float(category_distribution.loc[category, 'mean'])
    print(f"{category:<10} | ${total/1e6:>13.2f}M | {count:>15} | ${mean/1e6:>14.2f}M")

print("\n=== Market Cap Range Distribution ===")
print("Range      | Number of Agents | Percentage")
print("-" * 45)
for range_name, count in range_distribution.items():
    percentage = (count / len(df)) * 100
    print(f"{range_name:<10} | {count:>15} | {percentage:>8.1f}%")

# Sort agents by market cap and show top 5 and bottom 5
print("\n=== Top 5 Agents by Market Cap ===")
top_5 = df.nlargest(5, 'Market_Cap')[['Agent', 'Market_Cap', 'Category']]
for _, row in top_5.iterrows():
    market_cap = float(row['Market_Cap'])
    print(f"{row['Agent']:<25} | ${market_cap/1e6:>8.2f}M | {row['Category']}")

print("\n=== Bottom 5 Agents by Market Cap ===")
bottom_5 = df.nsmallest(5, 'Market_Cap')[['Agent', 'Market_Cap', 'Category']]
for _, row in bottom_5.iterrows():
    market_cap = float(row['Market_Cap'])
    print(f"{row['Agent']:<25} | ${market_cap/1e6:>8.2f}M | {row['Category']}")

print("\n=== Verification: All Agents Below 10M ===")
print("Agent                     | Market Cap | Category")
print("-" * 55)
below_10m = df[df['Market_Cap'] < 10e6].sort_values('Market_Cap')
for _, row in below_10m.iterrows():
    market_cap = float(row['Market_Cap'])
    print(f"{row['Agent']:<25} | ${market_cap/1e6:>8.2f}M | {row['Category']}")

# Create visualizations
plt.style.use('ggplot')  # Use ggplot style instead of seaborn
plt.rcParams['figure.figsize'] = [15, 12]
plt.rcParams['font.size'] = 10
plt.figure()

# Pie chart of market cap by category
plt.subplot(2, 1, 1)
category_sums = df.groupby('Category')['Market_Cap'].sum().round(2)
category_sums_millions = (category_sums / 1e6).astype(float)

# Sort categories by market cap for better visualization
sorted_indices = category_sums_millions.argsort()[::-1]
plt.pie(category_sums_millions.iloc[sorted_indices], 
        labels=[f"{cat}\n(${val:.2f}M)" for cat, val in zip(category_sums_millions.index[sorted_indices], category_sums_millions.iloc[sorted_indices])],
        autopct='%1.1f%%',
        explode=[0.1 if i == 0 else 0 for i in range(len(category_sums_millions))],
        shadow=True)
plt.title('Market Cap Distribution by Category', pad=20, fontsize=14)

# Bar chart of market cap ranges with percentages
plt.subplot(2, 1, 2)
range_counts = df['Market_Cap_Range'].value_counts().sort_index()
range_percentages = (range_counts / len(df) * 100).round(1)

x_pos = np.arange(len(range_counts))
bars = plt.bar(x_pos, range_counts.to_numpy(), color='skyblue')
plt.xticks(x_pos, [str(idx) for idx in range_counts.index], rotation=45)
plt.title('Number of Agents by Market Cap Range', pad=20, fontsize=14)
plt.ylabel('Number of Agents')

# Add value labels on top of each bar
for i, (count, percentage) in enumerate(zip(range_counts, range_percentages)):
    plt.text(i, count, f'{count}\n({percentage:.1f}%)', 
             ha='center', va='bottom', fontsize=10)

# Add grid for better readability
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Adjust layout and save
plt.tight_layout(pad=3.0)
plt.savefig('market_cap_distribution.png', bbox_inches='tight', dpi=300, facecolor='white')
plt.close()

# Calculate and display cumulative percentages
print("\n=== Cumulative Market Cap Distribution ===")
print("Range      | Count | Percentage | Cumulative %")
print("-" * 50)
cumulative_pct = 0
for range_name in range_counts.index:
    count = range_counts[range_name]
    percentage = range_percentages[range_name]
    cumulative_pct += percentage
    print(f"{range_name:<10} | {count:>5} | {percentage:>9.1f}% | {cumulative_pct:>11.1f}%")

# Print summary statistics
print("\n=== Summary of Market Cap Distribution ===")
print(f"Total number of AI agents analyzed: {len(df)}")
print(f"Total market cap across all agents: ${df['Market_Cap'].sum()/1e6:.2f}M")
print("\nDistribution by category:")
for cat in category_sums.index:
    num_agents = len(df[df['Category'] == cat])
    total_cap = category_sums[cat] / 1e6
    print(f"{cat}: {num_agents} agents, Total: ${total_cap:.2f}M")

print("\nMarket cap range distribution:")
print("Range      | Number of Agents | Percentage")
print("-" * 45)
for range_name, count in range_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{range_name:<10} | {count:>15} | {percentage:>8.1f}%")
