import pandas as pd

results = pd.read_csv("results.csv", parse_dates=["date"])

COMPETIONS = [
    'FIFA World Cup', 'UEFA Euro',
    'African Cup of Nations', 'AFC Asian Cup', 'CONCACAF Series', 'Gold Cup',
    'Copa América', 'Oceania Nations Cup'
]

MIN_DATE = pd.Timestamp("2022-11-20")
MAX_DATE = pd.Timestamp("2026-06-09")

def map_advantage(row):
    if row["neutral"] == True:
        return 0
    elif row["home_team"] == row["country"]:
        return 1
    elif row["away_team"] == row["country"]:
        return 2
    
results = results[(results["date"] >= MIN_DATE) & (results["date"] <= MAX_DATE)].reset_index(drop=True)

results = results[(results["tournament"].isin(COMPETIONS))].reset_index(drop=True)

results["home_advantage_status"] = results.apply(map_advantage, axis=1)

results = results.rename(columns={
    "date": "match_date",
    "home_team": "team_a_name",
    "away_team": "team_b_name",
    "home_score": "team_a_score",
    "away_score": "team_b_score"
})

country = pd.read_csv("country.csv")

name_to_id = {row["country_name"]: row["id"] for _, row in country.iterrows()}

results["team_a_id"] = results["team_a_name"].map(name_to_id).astype("Int64")
results["team_b_id"] = results["team_b_name"].map(name_to_id).astype("Int64")
results = results.dropna(subset=["team_a_id", "team_b_id"]).reset_index()

# print(name_to_id)

print(results)
