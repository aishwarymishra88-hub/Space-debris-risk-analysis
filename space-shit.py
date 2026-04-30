
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct folder
data_folder = os.path.join(BASE_DIR, "2_Files")

print("Folder ready")


# --- FUNCTIONS ---
def calculate_altitude(mean_motion):
    return ((398600.4418 / ((mean_motion * 2 * np.pi / 86400) ** 2)) ** (1/3)) - 6371


def orbit_class(alt):
    if alt < 2000:
        return "LEO"
    elif alt < 35786:
        return "MEO"
    else:
        return "GEO"


def estimate_velocity(orbit):
    if orbit == "LEO":
        return 7.8
    elif orbit == "MEO":
        return 3.9
    else:
        return 3.1


def calculate_risk(debris_row, sat_row):
    score = 0

    if abs(debris_row["Altitude"] - sat_row["Altitude"]) < 200:
        score += 1
    if abs(debris_row["Velocity"] - sat_row["Velocity"]) < 2:
        score += 1
    if debris_row["Orbit_Type"] == sat_row["Orbit_Type"]:
        score += 1

    if score == 3:
        return "High"
    elif score == 2:
        return "Medium"
    else:
        return "Low"


# --- MAIN ---
if __name__ == "__main__":

    # ✅ Load directly from 2_Files
    active_path = os.path.join(data_folder, "active_final.csv")
    debris_path = os.path.join(data_folder, "debris_final.csv")

    active_df = pd.read_csv(active_path)
    debris_df = pd.read_csv(debris_path)

    print("CSV Data loaded successfully")

    # Process
    active_df["Altitude"] = active_df["Mean_Motion"].apply(calculate_altitude)
    debris_df["Altitude"] = debris_df["Mean_Motion"].apply(calculate_altitude)

    active_df["Orbit_Type"] = active_df["Altitude"].apply(orbit_class)
    debris_df["Orbit_Type"] = debris_df["Altitude"].apply(orbit_class)

    active_df["Velocity"] = active_df["Orbit_Type"].apply(estimate_velocity)
    debris_df["Velocity"] = debris_df["Orbit_Type"].apply(estimate_velocity)

    active_df = active_df.head(100)
    debris_df = debris_df.head(50)

    # Save outputs (same folder)
    active_df.to_csv(os.path.join(data_folder, "active_final.csv"), index=False)
    debris_df.to_csv(os.path.join(data_folder, "debris_final.csv"), index=False)

    results = []
    for _, debris in debris_df.iterrows():
        for _, sat in active_df.iterrows():
            risk = calculate_risk(debris, sat)
            results.append({
                "Debris": debris["Name"],
                "Satellite": sat["Name"],
                "Risk_Level": risk
            })

    risk_df = pd.DataFrame(results)

    high_risk = risk_df[risk_df["Risk_Level"] != "Low"]

    # Save result
    high_risk.to_csv(os.path.join(data_folder, "risk_output.csv"), index=False)

    print("File saved successfully")

    # Charts
    risk_df["Risk_Level"].value_counts().plot(kind="bar")
    plt.title("Distribution of Risk Levels")
    plt.xlabel("Risk Level")
    plt.ylabel("Count")
    plt.show()

    active_df["Orbit_Type"].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title("Satellite Orbit Distribution")
    plt.show()