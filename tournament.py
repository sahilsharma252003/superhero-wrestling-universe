import pandas as pd
import random
import joblib
from datetime import datetime
from predict import df, model, numeric_cols, binary_cols, generate_fight_description, update_hero_stats, smart_search

def run_match(hero_a_name, hero_b_name, log_lines):
    hero_a = df.loc[hero_a_name]
    hero_b = df.loc[hero_b_name]

    features = {}
    for col in numeric_cols + binary_cols:
        features[f"{col}_diff"] = float(hero_a[col]) - float(hero_b[col])
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)[0]

    winner = hero_a_name if prediction == 1 else hero_b_name
    loser = hero_b_name if prediction == 1 else hero_a_name

    update_hero_stats(winner, loser)
    report = generate_fight_description(hero_a_name, hero_b_name, winner, [])
    print(report)
    log_lines.append(report)
    return winner

def manual_selection(size):
    chosen = []
    while len(chosen) < size:
        query = input(f"Enter hero #{len(chosen)+1} (partial name): ").strip()
        matches = smart_search(query)
        if not matches:
            print("❌ No matches found. Try again.")
            continue

        print("\nSelect from these options:")
        for i, name in enumerate(matches):
            print(f"{i+1}. {name}")
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(matches):
                hero = matches[choice - 1]
                if hero in chosen:
                    print("⚠️ Already selected. Choose a different hero.")
                else:
                    chosen.append(hero)
            else:
                print("❌ Invalid number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    return chosen

# === TOURNAMENT MODE ===
print("🏆 TOURNAMENT MODE - Customize Your Battle Royale")

# 1. Ask size
while True:
    try:
        size = int(input("Enter tournament size (4, 8, or 16): "))
        if size in [4, 8, 16]:
            break
        else:
            print("❌ Please enter 4, 8, or 16.")
    except ValueError:
        print("❌ Enter a valid number.")

# 2. Manual or Auto
while True:
    mode = input("Select mode - (A)uto-fill or (M)anual selection: ").strip().lower()
    if mode == 'a':
        while True:
            selected_heroes = random.sample(list(df.index), size)
            print("\n🎯 Randomly Selected Fighters:")
            for i, name in enumerate(selected_heroes, 1):
                print(f"{i}. {name}")
            confirm = input("Proceed with these heroes? (yes/no): ").strip().lower()
            if confirm == 'yes':
                break
        break
    elif mode == 'm':
        selected_heroes = manual_selection(size)
        break
    else:
        print("❌ Please enter 'A' or 'M'.")

# 3. Begin tournament
log = []
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.append(f"\n=== TOURNAMENT START [{timestamp}] ===")
log.append(f"Size: {size}, Mode: {'Manual' if mode == 'm' else 'Auto'}")
log.append("Fighters:\n" + "\n".join([f"{i+1}. {name}" for i, name in enumerate(selected_heroes)]))

# Rounds
round_num = 1
fighters = selected_heroes
while len(fighters) > 1:
    log.append(f"\n--- ROUND {round_num} ---")
    print(f"\n--- ROUND {round_num} ---")
    next_round = []
    for i in range(0, len(fighters), 2):
        winner = run_match(fighters[i], fighters[i+1], log)
        next_round.append(winner)
    fighters = next_round
    round_num += 1

champion = fighters[0]
log.append(f"\n🏅 TOURNAMENT CHAMPION: {champion} 🏆")
print(f"\n🏅 TOURNAMENT CHAMPION: {champion} 🏆")

# Save log
with open("tournament_history.txt", "a") as f:
    f.write("\n".join(log))
    f.write("\n" + "="*50 + "\n")
