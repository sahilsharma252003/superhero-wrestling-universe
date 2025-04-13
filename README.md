
# 🏟️ Superhero Wrestling Universe (SHU)

> A machine learning-powered event simulation engine where superheroes clash in WWE-style weekly shows filled with rivalries, interferences, championship battles, and cinematic storylines.

---

![SHU Banner](https://via.placeholder.com/1200x300.png?text=Superhero+Wrestling+Universe+%28SHU%29+by+Sahil+Sharma)

---

## 📦 About the Project

**Superhero Wrestling Universe (SHU)** is a Python-based ML simulation project where fictional superheroes compete in a wrestling-style environment with:

- Weekly match cards
- Interferences and rivalries
- Auto-triggered PPV events
- Champion & stat tracking
- Full story logs with AI-generated commentary

Built to merge data science, simulation, and storytelling into one powerful creative sandbox.

---

## 🚀 Getting Started

### 🔽 1. Clone the Repo

```bash
git clone https://github.com/sahilsharma252003/superhero-wrestling-universe.git
cd superhero-wrestling-universe
```

### 🛠️ 2. Install Requirements

> Make sure Python 3.10+ is installed.

```bash
pip install pandas scikit-learn joblib
```

### 🧠 3. Run the Setup

This project assumes you already have:
- `clean_hero_stats.csv` with superhero attributes
- `model.pkl` – pre-trained ML model (included)

If not, train the model using your `predict.py` setup or upload files from your local dataset.

---

## 🎮 Available Simulators

### 🗓️ Weekly Show
```bash
python3 weekly_show.py
```
Generates a 5-match wrestling-style card with rare storytelling elements and interference.

### 🏆 Tournament Mode
```bash
python3 tournament.py
```
Custom-sized knockout tournament with manual or auto-filled entries.

### 👑 Champion Challenge Mode
```bash
python3 champion.py
```
Let a reigning champion face off against new challengers.

---

## 📁 Project Structure

```
superhero-wrestling-universe/
├── predict.py               # ML prediction engine
├── weekly_show.py          # Weekly event simulator
├── tournament.py           # Tournament mode
├── champion.py             # Champion challenge mode
├── hero_stats.csv          # Tracks each hero’s record
├── weekly_show_log.txt     # Event storyline logs
├── show_counter.txt        # Show count tracker
├── model.pkl               # Pre-trained ML model
└── clean_hero_stats.csv    # Superhero stats (attributes)
```

---

## 🛠️ Built With

- Python
- scikit-learn
- pandas
- joblib
- Creativity and chaos 💥

---

## 👤 Maintainer

**Sahil Sharma**  
[LinkedIn](https://www.linkedin.com/in/sahilsharma2003/) · [GitHub](https://github.com/sahilsharma252003)

---
