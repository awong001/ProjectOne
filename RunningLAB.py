import streamlit as st
import datetime
import pandas as pd
import json
import os

st.set_page_config(page_title="Running Lab", layout="centered")
st.title("Running Lab")

#tabs
tab1, tab2, tab3= st.tabs(["Tracker", "Countdown", "Calories"])

#running tracker
with tab1:
    st.subheader("Running Tracker")

    DATA_FILE = "running_data.json"  #json file to save data

    #load data if file exists
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            st.session_state.routes = data.get("routes", {})
            st.session_state.runs = data.get("runs", [])
    else:
        if "routes" not in st.session_state: #stores data while app is running
            st.session_state.routes = {}
        if "runs" not in st.session_state:
            st.session_state.runs = []

    #add new route
    with st.form("add_route_form"): #allows you to input multiple things before submitting
        route_name = st.text_input("Route Name")
        route_dist = st.number_input("Distance (mi)", min_value=0.0, step=0.1)
        add_route = st.form_submit_button("Add Route")
        if add_route:
            if route_name and route_dist > 0:
                st.session_state.routes[route_name] = route_dist #saves route to session state
                st.success(f"Route '{route_name}' added!")

                #save data to json
                with open(DATA_FILE, "w") as f:
                    json.dump({"routes": st.session_state.routes, "runs": st.session_state.runs}, f)

            else:
                st.error("Please enter a valid route name and distance.")

    #delete route
    if st.session_state.routes:
        delete_route = st.selectbox("Delete a Route", list(st.session_state.routes.keys())) #dropdown menu
        if st.button("Delete Route"):
            del st.session_state.routes[delete_route] #deletes route and runs in the route
            st.success(f"🗑️ Route '{delete_route}' deleted!")

            #save data to json
            with open(DATA_FILE, "w") as f:
                json.dump({"routes": st.session_state.routes, "runs": st.session_state.runs}, f) 

    #log a run
    if st.session_state.routes:
        selected_route = st.selectbox("Select Route", list(st.session_state.routes.keys())) #dropdown menu
        time_min = st.number_input("Time (minutes)", min_value=0.0, step=0.1)
        if st.button("Log Run"): 
            if selected_route and time_min > 0:
                today = datetime.date.today().isoformat() #gets current date
                dist = st.session_state.routes[selected_route] #gets distance of selected route
                st.session_state.runs.append((selected_route, dist, time_min, today)) #saves run to session state
                st.success("🏁 Run logged!")

                #save data to json
                with open(DATA_FILE, "w") as f:
                    json.dump({"routes": st.session_state.routes, "runs": st.session_state.runs}, f)

            else:
                st.error("Please select a route and enter a valid time.")

    #delete run
    if st.session_state.runs:
        run_df = pd.DataFrame(st.session_state.runs, columns=["Route", "Dist (mi)", "Time (min)", "Date"])
        run_to_delete = st.selectbox("Delete a Run", run_df.apply(lambda x: f"{x['Route']} - {x['Date']} ({x['Time (min)']} min)", axis=1)) 
        if st.button("Delete Run"):
            index = run_df[run_df.apply(lambda x: f"{x['Route']} - {x['Date']} ({x['Time (min)']} min)", axis=1) == run_to_delete].index[0]
            del st.session_state.runs[index] #deletes run 
            st.success("Run deleted!")

            #save data to json
            with open(DATA_FILE, "w") as f:
                json.dump({"routes": st.session_state.routes, "runs": st.session_state.runs}, f)

    #show table
    if st.session_state.runs:
        df = pd.DataFrame(st.session_state.runs, columns=["Route", "Dist (mi)", "Time (min)", "Date"]) #lists runs in scrollable table
        df["Pace (min/mi)"] = df["Time (min)"] / df["Dist (mi)"] #sets pace
        st.dataframe(df, use_container_width=True) #format
        st.line_chart(df[["Dist (mi)", "Time (min)", "Pace (min/mi)"]]) #line chart of distance, time, and pace

# Race Countdown (Tab 2)
with tab2:
    import datetime
    st.subheader("🏁 Race Countdown")

    if "races" not in st.session_state:
        st.session_state.races = []

    # form to add a race
    with st.form("add_race_form", clear_on_submit=True):
        race_name = st.text_input("Race Name", key="race_name_input")
        race_type = st.selectbox(
            "Race Type",
            ["5K", "10K", "Half Marathon", "Full Marathon"],
            key="race_type_input"
        )
        race_date = st.date_input("Race Date", key="race_date_input")
        add_race = st.form_submit_button("Add Race")

    # when form submitted
    if add_race and race_name:
        st.session_state.races.append({
            "name": race_name,
            "type": race_type,
            "date": race_date
        })

    # show all races
    if st.session_state.races:
        st.write("### Your Races")
        today = datetime.date.today()

        for i, race in enumerate(st.session_state.races):
            race_date = race["date"]
            days_left = (race_date - today).days

            if days_left < 0:
                st.markdown(f"**{race['name']}** — This race has already passed.")
                continue

            weeks = days_left // 7
            days = days_left % 7

            
            # adjust by race type
            if race["type"] == "5K":
                rec = "10–20 miles/week"
            elif race["type"] == "10K":
                rec = "20–30 miles/week"
            elif race["type"] == "Half Marathon":
                rec = "25–45 miles/week"
            elif race["type"] == "Full Marathon":
                rec = "35–55 miles/week"

            # display info
            st.markdown(
                f"**🏁 {race['name']}**  \n"
                f"*{race['type']}* — {race_date.strftime('%B %d, %Y')}  \n"
                f"⏱️ {weeks} weeks and {days} days remaining  \n"
                f"💡 Recommended mileage: **{rec}**"
            )

            # delete button for this race
            if st.button(f"Delete {race['name']}", key=f"delete_{i}"):
                st.session_state.races.pop(i)
                st.rerun()



#calorie calculator
with tab3:
    st.subheader("Calorie Calculator")

    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    height = st.number_input("Height (in)", min_value=1.0, step=0.1)
    weight = st.number_input("Weight (lbs)", min_value=1.0, step=0.1)

    if st.button("Calculate Calories"):
        try:
            if gender == "Male":
                bmr = 66 + 6.23 * weight + 12.7 * height - 6.8 * age
            else:
                bmr = 655 + 4.35 * weight + 4.7 * height - 4.7 * age
            st.write(f"**Maintain:** {round(bmr)} kcal/day")
            st.write(f"**Gain:** {round(bmr + 500)} kcal/day")
            st.write(f"**Lose:** {round(bmr - 500)} kcal/day")
        except:
            st.error("Please fill all fields correctly.")

#streamlit run /Users/brettcampbell/RunningLAB.py