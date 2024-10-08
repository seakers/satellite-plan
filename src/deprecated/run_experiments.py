import csv
import os
import time

from run_experiment import run_experiment

ffor_levels = [10,20,40,60,80]
ffov_levels = [20,10,5,2,1]
constellation_size_levels = [2,4,6,8,10]
agility_levels = [10,5,1,0.1,0.01]
event_duration_levels = [24*3600,12*3600,6*3600,3*3600,1.5*3600]
event_frequency_levels = [1/3600,0.1/3600,0.01/3600,0.001/3600,1e-4/3600]
event_density_levels = [1,2,5,10]
event_clustering_levels = [1,2,4,8,16]
reward_levels = [0.5,1,2,5,10]
planners = ["fifo","mcts","dp","heuristic"]
reobserve_reward_levels = [0.1,0.5,1,2,5]

default_settings = {
    "name": "reobs_reward_comparison_default",
    "ffor": 60,
    "ffov": 5,
    "constellation_size": 6,
    "agility": 1,
    "event_duration": 6*3600,
    "event_frequency": 0.01/3600,
    "event_density": 10,
    "event_clustering": 4,
    "planner": "heuristic",
    "reobserve_reward": 2,
    "reward": 0.5
}

parameters = {
    # "agility": agility_levels,
    # "event_duration": event_duration_levels,
    # "event_clustering": event_clustering_levels,
    # "event_frequency": event_frequency_levels,
    # "event_density": event_density_levels,
    # "ffor": ffor_levels,
    # "constellation_size": constellation_size_levels,
    # "ffov": ffov_levels
    #"planner": planners
    #"reward": reward_levels
    "reobserve_reward": reobserve_reward_levels
}

i = 0
settings_list = []
settings_list.append(default_settings)
for parameter in parameters:
    for level in parameters[parameter]:
        experiment_name = 'reobs_reward_comparison_'+str(i)
        modified_settings = default_settings.copy()
        modified_settings[parameter] = level
        if modified_settings == default_settings:
            continue
        modified_settings["name"] = experiment_name
        settings_list.append(modified_settings)
        i = i+1
        
with open('./reobs_reward_comparison.csv','w') as csvfile:
    csvwriter = csv.writer(csvfile,delimiter=',',quotechar='|')
    first_row = ["name","for","fov","constellation_size","agility",
                "event_duration","event_frequency","event_density","event_clustering",
                "planner","reobserve_reward", "reward",
                "events","init_obs_count","replan_obs_count","vis_count",
                "init_event_obs_count","init_events_seen","init_event_reward","init_planner_reward","init_perc_cov","init_max_rev","init_avg_rev","init_all_perc_cov","init_all_max_rev","init_all_avg_rev",
                "replan_event_obs_count","replan_events_seen","replan_event_reward","replan_planner_reward","replan_perc_cov","replan_max_rev","replan_avg_rev","replan_all_perc_cov","replan_all_max_rev","replan_all_avg_rev",
                "vis_event_obs_count","vis_events_seen","vis_event_reward","vis_planner_reward","vis_perc_cov","vis_max_rev","vis_avg_rev","vis_all_perc_cov","vis_all_max_rev","vis_all_avg_rev",
                "time"]
    csvwriter.writerow(first_row)
    csvfile.close()
for settings in settings_list:
    start = time.time()
    print(settings["name"])
    overall_results = run_experiment(settings)
    end = time.time()
    elapsed_time = end-start
    with open('./reobs_reward_comparison.csv','a') as csvfile:
        csvwriter = csv.writer(csvfile,delimiter=',',quotechar='|')
        row = [settings["name"],settings["instrument"]["ffor"],settings["instrument"]["ffov"],settings["constellation"]["num_planes"],settings["agility"]["max_slew_rate"],
            settings["events"]["event_duration"],settings["events"]["event_frequency"],settings["events"]["event_density"],settings["events"]["event_clustering"],settings["num_meas_types"],
            settings["planner"],settings["rewards"]["reobserve_reward"], settings["rewards"]["reward"],
            overall_results["num_events"],overall_results["num_obs_init"],overall_results["num_obs_replan"],overall_results["num_vis"],
            overall_results["init_results"]["event_obs_count"],overall_results["init_results"]["events_seen_once"],overall_results["init_results"]["event_reward"],overall_results["init_results"]["planner_reward"],overall_results["init_results"]["percent_coverage"],overall_results["init_results"]["event_max_revisit_time"],overall_results["init_results"]["event_avg_revisit_time"],overall_results["init_results"]["all_percent_coverage"],overall_results["init_results"]["all_max_revisit_time"],overall_results["init_results"]["all_avg_revisit_time"],
            overall_results["replan_results"]["event_obs_count"],overall_results["replan_results"]["events_seen_once"],overall_results["replan_results"]["event_reward"],overall_results["replan_results"]["planner_reward"],overall_results["replan_results"]["percent_coverage"],overall_results["replan_results"]["event_max_revisit_time"],overall_results["replan_results"]["event_avg_revisit_time"],overall_results["replan_results"]["all_percent_coverage"],overall_results["replan_results"]["all_max_revisit_time"],overall_results["replan_results"]["all_avg_revisit_time"],
            overall_results["vis_results"]["event_obs_count"],overall_results["vis_results"]["events_seen_once"],overall_results["vis_results"]["event_reward"],overall_results["vis_results"]["planner_reward"],overall_results["vis_results"]["percent_coverage"],overall_results["vis_results"]["event_max_revisit_time"],overall_results["vis_results"]["event_avg_revisit_time"],overall_results["vis_results"]["all_percent_coverage"],overall_results["vis_results"]["all_max_revisit_time"],overall_results["vis_results"]["all_avg_revisit_time"],
            elapsed_time
        ]
        csvwriter.writerow(row)
        csvfile.close()