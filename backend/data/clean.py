import pandas as pd

results = pd.read_csv("results.csv", parse_dates=["date"])

COMPETIONS = [
    'FIFA World Cup', 'UEFA Euro',
    'African Cup of Nations', 'AFC Asian Cup', 'CONCACAF Series', 'Gold Cup',
    'Copa América', 'Oceania Nations Cup', 'FIFA World Cup qualification',
    'UEFA Euro qualification',
    'African Cup of Nations qualification',
    'AFC Asian Cup qualification',
    'CONCACAF Gold Cup qualification',
    'Copa América qualification',
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
    
def set_results(row):
    if row["team_a_score"] > row["team_b_score"]:
        return row["team_a_id"]
    elif row["team_b_score"] > row["team_a_score"]:
        return row["team_b_id"]
    else:
        return None
    
#filters results down to be inbetween the max date and min date    
results = results[(results["date"] >= MIN_DATE) & (results["date"] <= MAX_DATE)].reset_index(drop=True)

#filters results for the competitions defined above
results = results[(results["tournament"].isin(COMPETIONS))].reset_index(drop=True)

#sets a home advantage status. 0 = both teams away, 1 = team_a at home, 2 = team_b at home
results["home_advantage_status"] = results.apply(map_advantage, axis=1)

results = results.rename(columns={
    "date": "match_date",
    "home_team": "team_a_name",
    "away_team": "team_b_name",
    "home_score": "team_a_score",
    "away_score": "team_b_score",
    "country": "host_country"
})

#reads country.csv and maps it into a dictionary
country = pd.read_csv("country.csv")
name_to_id = {row["country_name"]: row["id"] for _, row in country.iterrows()}

#sets ids for team a and team b to be used as a foreign key
results["team_a_id"] = results["team_a_name"].map(name_to_id).astype("Int64")
results["team_b_id"] = results["team_b_name"].map(name_to_id).astype("Int64")

#country ids and host country now match to be used as a foreign key as well
results["host_country"] = results["host_country"].map(name_to_id).astype("Int64")

#drops null values for these columns
results = results.dropna(subset=["team_a_id", "team_b_id", "team_a_score", "team_b_score"]).reset_index()

#sets these to whole numbers
results["team_a_score"] = results["team_a_score"].astype("Int64")
results["team_b_score"] = results["team_b_score"].astype("Int64")

#create a new column called match_results that has the results for eeeeverything
# -1 == draw, anything else is an existing country
results["match_results"] = results.apply(set_results, axis=1)
results["match_results"] = results["match_results"].astype("Int64")

#add an id field to be index + 1
results["id"] = results.index + 1

#drop unnecessary columns
results = results.drop(columns=["city", "neutral", "index", "team_a_name", "team_b_name"])

results.to_csv("matches.csv", index=False)
print(results)
