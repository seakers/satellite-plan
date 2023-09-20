import csv
import os
import time

from run_experiment import run_experiment

ffor_levels = [120,80,60,40,20]
ffov_levels = [20,10,5,2,1]
constellation_size_levels = [10,8,6,4,2]
agility_levels = [10,5,1,0.1,0.01]
event_duration_levels = [24*3600,12*3600,6*3600,3*3600,1.5*3600]
event_frequency_levels = [1/3600,0.1/3600,0.01/3600,0.001/3600,1e-4/3600]
event_density_levels = [1,5,10,20,50]
event_clustering_levels = [1,2,4,8,16]
planners = ["fifo","mcts","dp","heuristic","milp"]

default_settings = {
    "name": "experiment_test",
    "ffor": 60,
    "ffov": 5,
    "constellation_size": 6,
    "agility": 1,
    "event_duration": 6*3600,
    "event_frequency": 0.01/3600,
    "event_density": 10,
    "event_clustering": 4,
    "planner": "heuristic",
    "planner_options": {
            "reobserve": "encouraged",
            "reobserve_reward": 2
    }
}

parameters = {
    "agility": agility_levels,
    "event_duration": event_duration_levels,
    "event_clustering": event_clustering_levels,
    "event_frequency": event_frequency_levels,
    "event_density": event_density_levels,
    "ffor": ffor_levels,
    "ffov": ffov_levels,
    "constellation_size": constellation_size_levels
}

i = 0
settings_list = []
#settings_list.append(default_settings)
for parameter in parameters:
    for level in parameters[parameter]:
        experiment_name = 'experiment_num_'+str(i)
        i = i+1
        # already_experimented = False
        # for f in os.listdir('./missions/'):
        #     if experiment_name in f:
        #         already_experimented = True
        # if already_experimented:
        #     continue
        modified_settings = default_settings.copy()
        modified_settings[parameter] = level
        if modified_settings == default_settings:
            continue
        modified_settings["name"] = experiment_name
        settings_list.append(modified_settings)
        


#overall_results = run_experiment(default_settings)
with open('./experiment_results_091923.csv','w') as csvfile:
    csvwriter = csv.writer(csvfile,delimiter=',',quotechar='|')
    first_row = ["name","for","fov","constellation_size","agility",
                "event_duration","event_frequency","event_density","event_clustering",
                "planner","reobserve",
                "events","init_obs_count","replan_obs_count","vis_count",
                "init_event_obs_count","init_events_seen",
                "replan_event_obs_count","replan_events_seen"
                "vis_event_obs_count","vis_events_seen","time"]
    csvwriter.writerow(first_row)
    csvfile.close()
for settings in settings_list:
    start = time.time()
    print(settings["name"])
    overall_results = run_experiment(settings)
    end = time.time()
    elapsed_time = end-start
    with open('./experiment_results_091923.csv','a') as csvfile:
        csvwriter = csv.writer(csvfile,delimiter=',',quotechar='|')
        row = [settings["name"],settings["ffor"],settings["ffov"],settings["constellation_size"],settings["agility"],
            settings["event_duration"],settings["event_frequency"],settings["event_density"],settings["event_clustering"],
            settings["planner"],settings["planner_options"]["reobserve"],
            overall_results["num_events"],overall_results["num_obs_init"],overall_results["num_obs_replan"],overall_results["num_vis"],
            overall_results["init_results"]["event_obs_count"],overall_results["init_results"]["events_seen_once"],
            overall_results["replan_results"]["event_obs_count"],overall_results["replan_results"]["events_seen_once"],
            overall_results["vis_results"]["event_obs_count"],overall_results["vis_results"]["events_seen_once"],
            elapsed_time
        ]
        csvwriter.writerow(row)
        csvfile.close()