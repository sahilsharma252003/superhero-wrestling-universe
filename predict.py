import pandas as pd
import joblib
import difflib
import random
import warnings
import os
from sklearn.exceptions import DataConversionWarning

# Suppress sklearn warnings about feature names
warnings.filterwarnings(action='ignore', category=UserWarning)
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

# Load model and hero stats
model = joblib.load("model.pkl")
df = pd.read_csv("clean_hero_stats.csv").set_index('name')

numeric_cols = ['intelligence_score', 'strength_score', 'speed_score',
                'durability_score', 'power_score', 'combat_score', 'overall_score']
binary_cols = [col for col in df.columns if col.startswith("has_")]

# Normalize names for fuzzy match
normalized_index = [name.lower().replace("-", "").replace(" ", "") for name in df.index]

# Create or load hero stats file
if not os.path.exists("hero_stats.csv"):
    hero_stats = pd.DataFrame(index=df.index)
    hero_stats["Battles"] = 0
    hero_stats["Wins"] = 0
    hero_stats["Losses"] = 0
    hero_stats["Win Rate (%)"] = 0.0
    hero_stats.to_csv("hero_stats.csv")
else:
    hero_stats = pd.read_csv("hero_stats.csv", index_col=0)

# ---------- Hero selection ---------- #
def smart_search(query):
    cleaned_query = query.lower().replace(" ", "").replace("-", "")
    matches = [(name, df.index[i]) for i, name in enumerate(normalized_index) if cleaned_query in name]

    if not matches:
        close = difflib.get_close_matches(cleaned_query, normalized_index, n=5, cutoff=0.5)
        matches = [(name, df.index[normalized_index.index(name)]) for name in close]

    return [real_name for _, real_name in matches]

def select_hero(prompt):
    while True:
        query = input(f"{prompt} (e.g., spiderman, iron man): ").strip()
        results = smart_search(query)
        if not results:
            print("❌ No matches found. Try again.")
            continue

        print("\nSelect from these options:")
        for i, name in enumerate(results):
            print(f"{i+1}. {name}")
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(results):
                return results[choice - 1]
            else:
                print("❌ Invalid number. Try again.")
        except ValueError:
            print("❌ Please enter a number.")

# ---------- Battle reporting ---------- #
def generate_fight_description(hero_a_name, hero_b_name, winner, top_advantages):
    loser = hero_b_name if winner == hero_a_name else hero_a_name

    settings = [
        "a crumbling city 🏙️", "a moonlit rooftop 🌙", "a secret Hydra base 🧪",
        "the ruins of Asgard ⚔️", "the heart of New York 🗽", "a remote desert 🏜️",
        "a multiverse rift 🌌", "Wakanda's borders 🐾", "a burning battlefield 🔥",
        "a deep underground arena 🕳️"
    ]

    openers = [
        f"💥 Under the shadows of {random.choice(settings)},",
        f"⚡ As lightning cracked above {random.choice(settings)},",
        f"🔥 In the chaos of {random.choice(settings)},",
        f"🌪️ With the fate of worlds hanging in balance at {random.choice(settings)},",
        f"🚨 Inside the warzone of {random.choice(settings)},"
    ]

    attacks = [
        "unleashed a devastating flurry of attacks 💣",
        "charged in with unstoppable momentum 🏃‍♂️",
        "used every ounce of power ⚡",
        "countered with precision and fury 🎯",
        "unleashed their ultimate form 🧬"
    ]

    finishes = [
        "💥 A thunderous strike silenced the battlefield.",
        "🔥 The skies lit up as the final blow landed.",
        "💣 The ground trembled under the victor's might.",
        "⚔️ A final roar echoed through the air.",
        "🌌 The multiverse shifted, acknowledging the winner."
    ]

    emoji_map = {
        "Strength": "💪",
        "Durability": "🛡️",
        "Power": "⚡",
        "Speed": "🚀",
        "Combat": "🥋",
        "Intelligence": "🧠"
    }

    reason_emojis = [f"{emoji_map.get(attr, '')} {attr}" for attr in top_advantages]
    reason_clause = f"Thanks to superior {', '.join(reason_emojis)}, {winner} claimed victory."

    story = (
        f"\n🌀 Battle Report\n"
        f"{random.choice(openers)} {hero_a_name} clashed with {hero_b_name} in an unforgettable showdown.\n"
        f"The fight was fierce as {winner} {random.choice(attacks)} while {loser} pushed back with all their might.\n"
        f"{random.choice(finishes)} {reason_clause}\n"
        f"\n🏆 Winner: {winner} 🎖️\n"
    )

    return story

# ---------- Stats tracking ---------- #
def update_hero_stats(winner, loser):
    for hero in [winner, loser]:
        if hero not in hero_stats.index:
            hero_stats.loc[hero] = [0, 0, 0, 0.0]
        hero_stats.at[hero, "Battles"] += 1

    hero_stats.at[winner, "Wins"] += 1
    hero_stats.at[loser, "Losses"] += 1

    for hero in [winner, loser]:
        wins = hero_stats.at[hero, "Wins"]
        battles = hero_stats.at[hero, "Battles"]
        win_rate = round((wins / battles) * 100, 2) if battles else 0
        hero_stats.at[hero, "Win Rate (%)"] = win_rate

    hero_stats.to_csv("hero_stats.csv")

# ---------- Main prediction function ---------- #
def predict_fight(hero_a_name, hero_b_name):
    hero_a = df.loc[hero_a_name]
    hero_b = df.loc[hero_b_name]

    features = {}
    for col in numeric_cols + binary_cols:
        features[f"{col}_diff"] = float(hero_a[col]) - float(hero_b[col])

    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)[0]

    winner = hero_a_name if prediction == 1 else hero_b_name
    loser = hero_b_name if prediction == 1 else hero_a_name

    # Top stat advantages
    diff_summary = {}
    for col in ['strength_score', 'durability_score', 'power_score', 'speed_score', 'combat_score', 'intelligence_score']:
        diff = float(hero_a[col]) - float(hero_b[col])
        if prediction == 1 and diff > 0:
            diff_summary[col] = diff
        elif prediction == 0 and diff < 0:
            diff_summary[col] = -diff

    top_advantages = sorted(diff_summary.items(), key=lambda x: -x[1])[:3]
    reasons = [col.replace("_score", "").capitalize() for col, _ in top_advantages]

    update_hero_stats(winner, loser)
    return generate_fight_description(hero_a_name, hero_b_name, winner, reasons)

# ---------- Run App ---------- #
if __name__ == "__main__":
    print("\n🔥 Welcome to the Superhero Fight Predictor 🔥\n")
    hero_a = select_hero("Enter Hero A")
    hero_b = select_hero("Enter Hero B")
    print(predict_fight(hero_a, hero_b))

