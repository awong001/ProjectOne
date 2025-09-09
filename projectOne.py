routes = {}
runs = []

print("Welcome to Running LAB Tracker")

while True:
    print("1. Add Route")
    print("2. Log Run")
    print("3. Show Runs")
    print("4. Quit")
    choice = input("Pick an option (1-4): ")

    if choice == "1":
        name = input("Enter route name: ")
        dist = float(input("Enter distance (km): "))
        routes[name] = dist
        print("Route '" + name + "' (" + str(dist) + " km) added.")

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
        runs.append([r, routes[r], t])
        print("Logged: " + r + " - " + str(routes[r]) + " km in " + str(t) + " minutes.")

    elif choice == "3":
        if not runs:
            print("No runs logged yet.")
            continue
        print("\n=== Your Runs ===")
        for run in runs:
            pace = run[2] / run[1]
            print(run[0] + ": " + str(run[1]) + " km in " + str(run[2]) +
                  " min (Pace " + str(round(pace, 2)) + " min/km)")

    elif choice == "4":
        print("Goodbye! Keep running strong.")
        break

    else:
        print("Invalid choice, try again.")
