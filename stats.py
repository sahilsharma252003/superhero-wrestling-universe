import pandas as pd
import difflib

# Load hero stats
try:
    stats = pd.read_csv("hero_stats.csv", index_col=0)
except FileNotFoundError:
    print("❌ No stats file found. Run some fights first!")
    exit()

# Normalize names for matching
normalized_names = [name.lower().replace("-", "").replace(" ", "") for name in stats.index]

# Ask user for fuzzy input
query = input("🔍 Enter hero name (e.g., spiderman, iron man): ").lower().replace(" ", "").replace("-", "")

# Find close matches
matches = [(norm, stats.index[i]) for i, norm in enumerate(normalized_names) if query in norm]

# If no exact substring match, try fuzzy close match
if not matches:
    close = difflib.get_close_matches(query, normalized_names, n=5, cutoff=0.5)
    matches = [(norm, stats.index[normalized_names.index(norm)]) for norm in close]

# Handle result
if not matches:
    print("❌ No matching hero found.")
else:
    print("\n🎯 Matching Heroes:")
    for i, name in enumerate(matches):
        print(f"{i+1}. {name[1]}")

    try:
        choice = int(input("Enter the number of your choice: "))
        if 1 <= choice <= len(matches):
            hero = matches[choice - 1][1]
            data = stats.loc[hero]
            print(f"\n📊 Stats for {hero}")
            print(f"  Battles: {int(data['Battles'])}")
            print(f"  Wins: {int(data['Wins'])}")
            print(f"  Losses: {int(data['Losses'])}")
            print(f"  Win Rate: {data['Win Rate (%)']}%")
        else:
            print("❌ Invalid number.")
    except ValueError:
        print("❌ Please enter a valid number.")
