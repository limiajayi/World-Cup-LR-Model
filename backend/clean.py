import pandas as pd

results = pd.read_csv("results.csv", parse_dates=["date"])

COMPETIONS = [
    'FIFA World Cup', 'UEFA Euro',
    'African Cup of Nations', 'AFC Asian Cup', 'CONCACAF Series', 'Gold Cup',
    'Copa América', 'Oceania Nations Cup'
]

MIN_DATE = pd.Timestamp("2022-11-20")
MAX_DATE = pd.Timestamp("2026-06-09")

results = results[(results["date"] >= MIN_DATE) & (results["date"] <= MAX_DATE)].reset_index(drop=True)

results = results[(results["tournament"].isin(COMPETIONS))].reset_index(drop=True)

print(results)
