import pandas as pd
import random
from datetime import datetime
from predict import df, model, numeric_cols, binary_cols, generate_fight_description, update_hero_stats

# === Show Tracking ===
SHOW_TRACKER = "show_counter.txt"
try:
    with open(SHOW_TRACKER, "r") as f:
        show_num = int(f.read().strip()) + 1
except:
    show_num = 1

# === PPV Titles ===
main_events = [
    "Multiverse Mayhem", "Infinity Brawl", "Secret Civil War", "Cosmic Collision",
    "Worlds Collide", "Apocalypse Ascension", "The Final Gauntlet", "Timebreak Turmoil",
    "Heroic Havoc", "Shadow Wars", "Universal Reckoning", "Crisis Convergence"
]

# === Show Name ===
show_type = "🔥 Clash of Powers"
if show_num % 4 == 0:
    show_type = f"🏆 MAIN EVENT: {random.choice(main_events)}"

# === Show Settings ===
match_count = 5
log_lines = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_lines.append(f"\n===== {show_type} | {timestamp} =====\n")

# === Storyline Elements ===
intros = [
    "{a} issues an open challenge, and {b} answers the call!",
    "{a} and {b} collide after weeks of tension!",
    "{a} called out {b} on the last show — it’s time to settle it.",
    "{b} attacked {a} backstage... now they face the consequences.",
    "This is a long-awaited rematch: {a} vs {b}!"
]

interference_chance = 0.1  # 10% chance of interference
story_intro_chance = 0.3   # 30% chance of special story intro

# === Match Simulation Function ===
def run_story_match(hero_a, hero_b):
    # Decide intro type
    if random.random() < story_intro_chance:
        intro = random.choice(intros).format(a=hero_a, b=hero_b)
        log_lines.append("🎤 " + intro)
        print("🎤", intro)
    else:
        basic_intro = f"{hero_a} faces off against {hero_b} in a one-on-one match."
        log_lines.append("🎯 " + basic_intro)
        print("🎯", basic_intro)

    # Match outcome logic
    hero_a_data = df.loc[hero_a]
    hero_b_data = df.loc[hero_b]

    features = {}
    for col in numeric_cols + binary_cols:
        features[f"{col}_diff"] = float(hero_a_data[col]) - float(hero_b_data[col])
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)[0]

    winner = hero_a if prediction == 1 else hero_b
    loser = hero_b if prediction == 1 else hero_a

    # Random Interference
    if random.random() < interference_chance:
        third_party = random.choice([h for h in df.index if h not in [hero_a, hero_b]])
        interference = f"💥 Suddenly, {third_party} rushes the ring and sabotages {winner}!"
        log_lines.append(interference)
        print(interference)
        winner, loser = loser, winner  # Interference flips winner

    update_hero_stats(winner, loser)
    result = generate_fight_description(hero_a, hero_b, winner, [])
    log_lines.append(result)
    print(result)

# === Build Match Card ===
all_fighters = list(df.index)
random.shuffle(all_fighters)
card = []

print(f"\n📺 {show_type} | MATCH CARD:\n")
for i in range(match_count):
    hero_a = all_fighters.pop()
    hero_b = all_fighters.pop()
    card.append((hero_a, hero_b))
    print(f"Match {i+1}: {hero_a} vs {hero_b}")

# === Run Matches ===
print("\n🎙️ MATCH RESULTS:\n")
for a, b in card:
    run_story_match(a, b)

# === Save Show Log ===
with open("weekly_show_log.txt", "a") as f:
    f.write("\n".join(log_lines))
    f.write("\n" + "=" * 60 + "\n")

# === Update Show Counter ===
with open(SHOW_TRACKER, "w") as f:
    f.write(str(show_num))

print(f"\n✅ {show_type} completed and logged to weekly_show_log.txt")
