import datetime
import os
import sys
sys.path.append(".")

from src.create_mission import create_mission
from src.execute_mission import execute_mission
from src.process_mission import process_mission
from src.plan_mission_fov import plan_mission, plan_mission_replan_interval, plan_mission_replan_interval_het
from src.plot_mission import plot_mission
from src.plot_mission_heterogeneous import plot_mission_het
from src.utils.compute_experiment_statistics import compute_experiment_statistics
from src.utils.compute_experiment_statistics_het import compute_experiment_statistics_het
from src.utils.process_coobs import process_coobs
import pandas as pd

scenarios = pd.read_csv('./satplan_parametric/satplan_test_case_2_seed-1000.csv')

experiments = scenarios['Name']
num_planes = scenarios['Number Planes']
num_sats_per_planes = scenarios['Number of Satellites per Plane']
field_of_regard = scenarios['Field of Regard (deg)']
field_of_view = scenarios['Field of View (deg)']
max_slew_rate = scenarios['Maximum Slew Rate (deg/s)']
num_events_per_day = scenarios['Number of Events per Day']
event_duration = scenarios['Event Duration (hrs)']
grid_type = scenarios['Grid Type']
num_ground_points = scenarios['Number of Ground-Points']
horizon = scenarios['Preplanning Period']
preplanner = scenarios['Preplanner']
scenario_id = scenarios['Scenario ID']

def main(sim_num, homhet_flag):
    # name = "full_mission_test_het_{}".format(sim_num)
    name = str(scenario_id[sim_num]) + "_" + str(preplanner[sim_num]) + "_" + str(grid_type[sim_num]) + "_" + str(num_ground_points[sim_num])
    settings = {
        "name": name,
        "instrument": {
            "ffor": int(field_of_regard[sim_num]),
            "ffov": int(field_of_view[sim_num])
        },
        "agility": {
            "slew_constraint": "rate",
            "max_slew_rate": int(max_slew_rate[sim_num]),
            "inertia": 2.66,
            "max_torque": 4e-3
        },
        "orbit": {
            "altitude": 705, # km
            "inclination": 98.4, # deg
            "eccentricity": 0.0001,
            "argper": 0, # deg
        },
        "constellation": {
            "num_sats_per_plane": int(num_sats_per_planes[sim_num]),
            "num_planes": int(num_planes[sim_num]),
            "phasing_parameter": 1
        },
        "events": {
            "event_duration": 3600*int(event_duration[sim_num]),
            "event_frequency": int(num_events_per_day[sim_num]) / (24 * 3600),   # events / s
            "event_density": 2,
            "event_clustering": 4
        },
        "time": {
            "step_size": 10, # seconds
            "duration": 1, # days
            "initial_datetime": datetime.datetime(2020,1,1,0,0,0)
        },
        "rewards": {
            "reward": 10,
            "reward_increment": 1,
            "reobserve_conops": "linear_increase",
            "event_duration_decay": "step",
            "no_event_reward": 5,
            "oracle_reobs": "true",
            "initial_reward": 5
        },
        "plotting":{
            "plot_clouds": False,
            "plot_rain": False,
            "plot_duration": 1,
            "plot_interval": 10,
            "plot_obs": True
        },
        "planner": "dp",
        "event_csvs": ["./satplan_parametric/events/scenario_"+str(scenario_id[sim_num])+"_events.csv"],
        "num_meas_types": 3,
        "sharing_horizon": int(horizon[sim_num]),
        "planning_horizon": int(horizon[sim_num]),
        "directory": "./missions/"+name+"/",
        "grid_type": "custom", # can be "uniform" or "custom"
        "preplanned_observations": None,
        "process_obs_only": False,
        "conops": "onboard_processing",
        "point_grid": "./satplan_parametric/grids/"+str(grid_type[sim_num])+"_grid_"+str(num_ground_points[sim_num])+"_seed-1000.csv",
        "scenario_file": "./satplan_parametric/satplan_test_case_2_seed-1000.csv"
    }
    if settings["constellation"]["num_sats_per_plane"] == 0:
        raise Exception("Number of satellites is 0")

    if settings["constellation"]["num_planes"] == 0:
        raise Exception("Number of planes is 0")

    if not os.path.exists(settings["directory"]):
        os.mkdir(settings["directory"])
    if not os.path.exists(settings["directory"]+'orbit_data/'):
        os.mkdir(settings["directory"]+'orbit_data/')
    create_mission(settings)
    execute_mission(settings)

    num_sats = settings["constellation"]["num_planes"] * settings["constellation"]["num_sats_per_plane"]

    if homhet_flag == "homogeneous":
        if settings["preplanned_observations"] is None:
            plan_mission_replan_interval(settings) # must come before process as process expects a plan.csv in the orbit_data directory
        process_mission(settings, sim_num, num_sats)
        plot_mission(settings)
    elif homhet_flag == "heterogeneous":
        if settings["preplanned_observations"] is None:
            plan_mission_replan_interval_het(settings) # must come before process as process expects a plan.csv in the orbit_data directory
        process_mission(settings, sim_num, num_sats)
        # plot_mission_het(settings)
    else:
        print("Invalid homhet_flag")


if __name__ == "__main__":
    for sim_num in range(0, len(experiments)):
        if str(preplanner[sim_num]) == "dp":
            main(sim_num, homhet_flag="heterogeneous")
        else:
            continue