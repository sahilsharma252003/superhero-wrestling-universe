import pandas as pd

# Load hero stats
try:
    stats = pd.read_csv("hero_stats.csv", index_col=0)
except FileNotFoundError:
    print("❌ No stats found. Run some fights first!")
    exit()

# Filter heroes who’ve fought at least once
stats = stats[stats["Battles"] > 0]

# Sort by most wins, then win rate
top_10 = stats.sort_values(by=["Wins", "Win Rate (%)"], ascending=False).head(10)

print("\n🏆 TOP 10 HEROES (by Wins):\n")
for i, (name, row) in enumerate(top_10.iterrows(), 1):
    print(f"{i}. {name}")
    print(f"   Battles: {int(row['Battles'])}")
    print(f"   Wins: {int(row['Wins'])}")
    print(f"   Losses: {int(row['Losses'])}")
    print(f"   Win Rate: {row['Win Rate (%)']}%\n")
