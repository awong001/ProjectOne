import json
import os
import datetime

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

print("Welcome to Running LAB Tracker")

def save_data():
    with open(DATA_FILE, "w") as f:   #opens file for writing
        json.dump({"routes": routes, "runs": runs}, f) #writes out both routes and runs in JSON format

while True:
    print("\n1. Add Route")
    print("2. Log Run")
    print("3. Show Runs")
    print("4. Quit")
    choice = input("Pick an option (1-4): ")

    if choice == "1":
        name = input("Enter route name: ")
        dist = float(input("Enter distance (km): "))
        routes[name] = dist
        print("Route '" + name + "' (" + str(dist) + " km) added.")
        save_data() #immediatley stores data when save_data()

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
        for run in runs:
            pace = run[2] / run[1]
            print(run[3] + " - " + run[0] + ": " + str(run[1]) + " km in " + str(run[2]) +
                  " min (Pace " + str(round(pace, 2)) + " min/km)")

    elif choice == "4":
        print("Goodbye! Keep running strong.")
        break

    else:
        print("Invalid choice, try again.")
#the
