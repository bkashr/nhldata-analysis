import requests
import pandas as pd

# NHL API URL for game schedule
NHL_API_URL = "https://statsapi.web.nhl.com/api/v1/schedule"

# Function to fetch game data
def fetch_nhl_games(start_date, end_date):
    params = {
        "startDate": start_date,
        "endDate": end_date
    }
    
    response = requests.get(NHL_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        games = []

        for date in data.get("dates", []):
            game_date = date["date"]
            for game in date["games"]:
                game_info = {
                    "date": game_date,
                    "home_team": game["teams"]["home"]["team"]["name"],
                    "away_team": game["teams"]["away"]["team"]["name"],
                    "home_score": game["teams"]["home"]["score"],
                    "away_score": game["teams"]["away"]["score"],
                    "game_id": game["gamePk"]
                }
                games.append(game_info)

        return pd.DataFrame(games)
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage - Fetch games from the start of this NHL season (adjust dates as needed)
start_date = "2023-10-10"
end_date = "2024-03-10"
nhl_games_df = fetch_nhl_games(start_date, end_date)

# Save data to CSV
if nhl_games_df is not None:
    nhl_games_df.to_csv("nhl_games.csv", index=False)
    print("Game data saved to nhl_games.csv")
    print(nhl_games_df.head())  # Preview data
