import json
import os
import datetime
import time

# File to store data
DATA_FILE = "runninglog_data.json"

# Initialize
routes = {}
runs = []

# Load data if file exists
if os.path.exists(DATA_FILE): 
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        routes = data.get("routes", {})
        runs = data.get("runs", [])

def save_data():
    with open(DATA_FILE, "w") as f:   # opens file for writing
        json.dump({"routes": routes, "runs": runs}, f) # writes out both routes and runs in JSON format

# ---------------------------
# Running LAB Tracker
# ---------------------------
def running_tracker():
    print("Welcome to Running LAB Tracker")
    while True:
        print("\n1. Add Route")
        print("2. Log Run")
        print("3. Show Runs")
        print("4. Back to Main Menu")
        choice = input("Pick an option (1-4): ")

        if choice == "1":
            name = input("Enter route name: ")
            dist = float(input("Enter distance (km): "))
            routes[name] = dist
            print("Route '" + name + "' (" + str(dist) + " km) added.")
            save_data()

        elif choice == "2":
            if not routes:
                print("No routes yet! Please add one first.")
                continue
            print("Available routes:")
            for r in routes:
                print(" - " + r + " (" + str(routes[r]) + " km)")
            r = input("Which route did you run? ")
            if r not in routes:
                print("Route not found.")
                continue
            t = float(input("How many minutes did it take? "))
            date = datetime.date.today().isoformat()
            runs.append([r, routes[r], t, date])
            print("Logged: " + r + " - " + str(routes[r]) + " km in " + str(t) + " minutes on " + date)
            save_data()

        elif choice == "3":
            if not runs:
                print("No runs logged yet.")
                continue
            print("\n=== Your Runs ===")
            for run in runs: #run[0]=route name run[1]=distance run[2]=time in minutes run[3]=date of run
                pace = run[2] / run[1]
                print(run[3] + " - " + run[0] + ": " + str(run[1]) + " km in " + str(run[2]) +
                      " min (Pace " + str(round(pace, 2)) + " min/km)")

        elif choice == "4":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice, try again.")

# ---------------------------
# Race Day Countdown
# ---------------------------
def race_countdown():
    RaceDay = input("Enter your race date and time (YYYY-MM-DD HH:MM:SS): ")
    race_type = input("What type of race are you running? (5k, 10k, half marathon, full marathon): ")

    # converting the input string to a datetime object
    RaceDay_time = datetime.datetime.strptime(RaceDay, "%Y-%m-%d %H:%M:%S")

    print(f"Countdown to: {RaceDay_time} — {race_type}")

    # Weekly mileage recommendations by race type 
    mileage_plan = {
        "5k": (15, 25),
        "10k": (20, 30),
        "half marathon": (25, 40),
        "full marathon": (35, 55)
    }

    while True:
        now = datetime.datetime.now()
        remaining = RaceDay_time - now

        if remaining.total_seconds() <= 0:
            print(f"\nIt's Race Day! Good luck with your {race_type}! 🏃‍♂️🎉")
            break

        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        weeks_left = days // 7

        if race_type in mileage_plan:
            low, high = mileage_plan[race_type]
            factor = 1 - min(weeks_left / 16, 1)  
            recommended = int(low + factor * (high - low))
            mileage_msg = f" | Recommended weekly mileage: ~{recommended} miles"
        else:
            mileage_msg = ""

        print(f"\r{days} days {hours:02}:{minutes:02}:{seconds:02} left until your {race_type}!!{mileage_msg}", end="")
        time.sleep(1)

# ---------------------------
# Main Menu
# ---------------------------
def main():
    while True:
        print("\n==== Main Menu ====")
        print("1. Running LAB Tracker")
        print("2. Race Day Countdown")
        print("3. Quit")
        choice = input("Pick an option (1-3): ")

        if choice == "1":
            running_tracker()
        elif choice == "2":
            race_countdown()
        elif choice == "3":
            print("Goodbye! Keep running strong.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
