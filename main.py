from scraper import scrape_stats
import graph
from database import Profile, Overall_Stats, All_Time_Ranked_Stats

"""Sometimes TRN network will be able pop a video up on the bottom right of the screen - this slows the
scrapping down considerably but the program will continue.

Additionally, scraping over 7 profiles in player_list will cause the site to check for robots -> cloudflare"""

PLATFORM_INDEX = 0  # 0 = SOCIAL(PC), 1 = PLAYSTATION, 2 = XBOX

# Testing max amount of accounts to scrape before robot detection
# player_list = ["imm_adawg", "Baldhead04", "squishedcheeks", "grubbbinator", "Doq", "Hairyleg53476", "Orangeliquid1",
#                "HoosierDuty"]

player_list = ["HoosierDuty", "Kindred-.", "Mattcat102", "Hairyleg53476", "LividPickle", "Doq"]
HEAD = "yes"  # to watch selenium simply pass "yes" for HEAD... else it will run headless
scrape_stats(platform=PLATFORM_INDEX, profile=player_list, head=HEAD)

# These few print statements grab the first entry of each collection and shows the structure for reference
fetch_profiles = Profile.extract_profile_names()
# print(f"{fetch_profiles[0]}\n")

fetch_overall_stats = Overall_Stats.get_overall_stats()
print(f"{fetch_overall_stats[0]}\n")

fetch_all_time_ranked_stats = All_Time_Ranked_Stats.get_ranked_stats()
print(f"{fetch_all_time_ranked_stats[0]}\n")

# These 4 function calls are to test to graph creation with database collections from graph.py
graph.overall_kills_bar()
graph.overall_wins_bar()
graph.overall_k_d_bar()
graph.overall_stats_bar()
