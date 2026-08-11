# World Cup Logistic Regression Model

Predicts the probability of each team winning a match (Country A vs Country B) using a logistic regression model trained on historical international football results.

**Status: in progress.** Data cleaning pipeline is done; feature engineering (last-5-matches form) and model training are in progress.

## Data pipeline (done)

Source data: [international football results, 1872–2017 (Kaggle)](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017/data?select=results.csv)

`backend/country.py`:

- Extracts the 48 teams competing in the 2026 World Cup group stage from `results.csv`, assigns each a numeric ID, and writes `country.csv`

`backend/clean.py`:

- Filters matches to major competitions (World Cup, Euros, AFCON, Asian Cup, Copa América, etc.) and qualifiers, within a defined date window
- Maps team names to numeric IDs via `country.csv` for use as foreign keys
- Derives a `home_advantage_status` feature (neutral / team A home / team B home)
- Derives match outcome (`match_results`) from scores
- Drops incomplete rows and writes a cleaned `matches.csv`

## In progress

- Fixing the source data for `country.py` (see known issue below)
- Building a "last 5 matches" form feature per team
- Training and evaluating the logistic regression model

## Running it

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# place results.csv (from the Kaggle link above) in backend/
python country.py   # generates country.csv (2026 World Cup teams + IDs)
python clean.py      # generates matches.csv (cleaned, ID-mapped match data)
```

> **Known issue:** There currently isn't enough data for some countries internationally so, may have to extend the date range past 2022
