import pandas as pd

#take in results.csv
#contains every single international match from 1872 - Present
results = pd.read_csv("results.csv", parse_dates=["date"])

#range of group stage matches
#to extract all 48 teams from the world cup
MIN_DATE = pd.Timestamp("2026-06-11")
MAX_DATE = pd.Timestamp("2026-06-27")

#get that range of matches
upcoming = results[(results["date"] >= MIN_DATE) & (results["date"] <= MAX_DATE)]

#extract team a and team b
team_a = set(upcoming["home_team"])
team_b = set(upcoming["away_team"])

all_teams = team_a | team_b #eliminates duplicates

teams_df = pd.DataFrame({
    "country_name": sorted(all_teams),
    "fifa_rank_2026": None
})

#add an id field
teams_df.index += 1
teams_df = teams_df.reset_index().rename(columns={"index": "id"})

teams_df.to_csv("country.csv", index=False)
print(teams_df)