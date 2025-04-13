import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Step 1: Load and clean dataset
df = pd.read_csv("superheroes_nlp_dataset.csv")

numeric_cols = ['intelligence_score', 'strength_score', 'speed_score',
                'durability_score', 'power_score', 'combat_score', 'overall_score']
binary_cols = [col for col in df.columns if col.startswith("has_")]

# Keep needed columns and drop rows with NaNs
df = df[numeric_cols + binary_cols + ['name']].copy()
df[binary_cols] = df[binary_cols].apply(pd.to_numeric, errors='coerce')
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
df = df.dropna().reset_index(drop=True)

# Step 2: Generate fight data
np.random.seed(42)
matchups = []
for _ in range(5000):
    i, j = np.random.choice(df.index, size=2, replace=False)
    hero_a = df.loc[i]
    hero_b = df.loc[j]
    winner = 1 if hero_a['overall_score'] > hero_b['overall_score'] else 0

    match = {'hero_a_name': hero_a['name'], 'hero_b_name': hero_b['name']}
    for col in numeric_cols + binary_cols:
        match[f"{col}_diff"] = float(hero_a[col]) - float(hero_b[col])
    match['winner'] = winner
    matchups.append(match)

fight_df = pd.DataFrame(matchups)

# Step 3: Train model
X = fight_df.drop(columns=['hero_a_name', 'hero_b_name', 'winner'])
y = fight_df['winner']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and hero stats
joblib.dump(model, "model.pkl")
df.set_index('name').to_csv("clean_hero_stats.csv")
print("✅ Model trained and saved!")
