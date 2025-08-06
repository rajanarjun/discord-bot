import requests
import json
import os
from datetime import datetime, timedelta

class GitCommitTracker:
    def __init__(self, username, repo):
        self.username = username
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{username}/{repo}/commits"
        self.commit_data = None
        self.load_commit()

    def load_commit(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and data:
                self.commit_data = data[0]
        except Exception as e:
            print(f"Failed to fetch commit info: {e}")

    def get_commit_info(self):
        if not self.commit_data:
            return None
        return {
            "author": self.commit_data["commit"]["author"]["name"],
            "commit_id": self.commit_data["sha"][:7],
            "message": self.commit_data["commit"]["message"],
            "date": self.commit_data["commit"]["author"]["date"][:10]
        }

    def get_streak(self):
        if not self.commit_data:
            return 0
        
        date_str = self.commit_data["commit"]["author"]["date"][:10]
        json_path = "commit_streaks.json"

        # Load or initialize JSON
        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                data = json.load(file)
        else:
            data = {}

        if self.username not in data:
            data[self.username] = {}
        if self.repo not in data[self.username]:
            data[self.username][self.repo] = {
                "dates": [],
                "streak": 0
            }

        record = data[self.username][self.repo]

        # Add today's commit date
        if date_str not in record["dates"]:
            record["dates"].append(date_str)

        # Clean and sort dates
        date_objects = sorted(set(datetime.strptime(d, "%Y-%m-%d").date() for d in record["dates"]))

        # Calculate streak
        streak = 1
        streak_dates = [date_objects[-1]]
        for i in range(len(date_objects) - 2, -1, -1):
            delta = (streak_dates[0] - date_objects[i]).days
            if delta == 1:
                streak += 1
                streak_dates.insert(0, date_objects[i])
            else:
                break  # If There is a gap it will reset

        # Update record
        record["streak"] = streak
        record["dates"] = [d.strftime("%Y-%m-%d") for d in streak_dates]

        # Save back
        with open(json_path, "w") as file:
            json.dump(data, file, indent=4)

        return streak
