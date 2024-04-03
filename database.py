from pymongo import MongoClient
import logging

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['r6_scraper']
users_collection = db['users']
overall_stats_collection = db['overall_stats']
all_time_ranked_collection = db['all_time_ranked_stats']

logging.basicConfig(filename='mongodb.log', level=logging.DEBUG)


# Creation of the Profile class for profile collection
class Profile:
    def __init__(self, profile_name, share_link, current_date):
        self.profile_name = profile_name
        self.share_link = share_link
        self.date_scraped = current_date

    def save_to_mongodb(self):
        try:
            existing_document = db['profiles'].find_one({"profile_name": self.profile_name})
            if existing_document:
                # Profile already exists, update the document
                logging.info(f"Profile:{self.profile_name} already in database. Updating data.")
                db['profiles'].update_one(
                    {"_id": existing_document["_id"]},
                    {"$set": {
                                    "share_link": self.share_link,
                                    "date_scraped": self.date_scraped,
                    }}
                )
            else:
                # Profile doesn't exist, insert a new document
                logging.info(f"Profile: {self.profile_name} not in database. Adding data.")
                db['profiles'].insert_one({
                    "profile_name": self.profile_name,
                    "share_link": self.share_link,
                    "date_scraped": self.date_scraped
                })
        except Exception as e:
            logging.error(f"Error saving Profile to MongoDB: {e}")

    # retrieves all profiles and collection info from Profile collection and returns as a list
    @staticmethod
    def get_all_profiles():
        try:
            profiles = db['profiles'].find()
            return list(profiles)
        except Exception as e:
            logging.error(f"Error retrieving profiles from MongoDB: {e}")
            return []

    # Retrieves all profile_names from the Profile collection and returns as a list
    @staticmethod
    def extract_profile_names():
        try:
            all_profiles = Profile.get_all_profiles()
            retrieved_profile_names = [profile['profile_name'] for profile in all_profiles]
            return retrieved_profile_names
        except Exception as e:
            logging.error(f"Error retrieving profiles from MongoDB: {e}")
            return []


# Creation of Overall_Stats class for Overall_Stats collection
class Overall_Stats:
    def __init__(self, profile_name, overall_wins, overall_win_pct, overall_kills, overall_k_d):
        self.profile_name = profile_name
        self.overall_wins = overall_wins
        self.overall_win_pct = overall_win_pct
        self.overall_kills = overall_kills
        self.overall_k_d = overall_k_d

    def save_to_mongodb(self):
        try:
            existing_document = db['overall_stats'].find_one({"profile_name": self.profile_name})
            if existing_document:
                # Profile already exists, update the document
                db['overall_stats'].update_one(
                    {"_id": existing_document["_id"]},
                    {"$set": {
                        "overall_wins": self.overall_wins,
                        "overall_win_pct": self.overall_win_pct,
                        "overall_kills": self.overall_kills,
                        "overall_k_d": self.overall_k_d
                    }}
                )
            else:
                # Profile doesn't exist, insert a new document
                db['overall_stats'].insert_one({
                    "profile_name": self.profile_name,
                    "overall_wins": self.overall_wins,
                    "overall_win_pct": self.overall_win_pct,
                    "overall_kills": self.overall_kills,
                    "overall_k_d": self.overall_k_d
                })
        except Exception as e:
            logging.error(f"Error saving Overall Stats to MongoDB: {e}")

    # Retrieves all collection data from Overall_Stats and returns as a list
    @staticmethod
    def get_overall_stats():
        try:
            overall_stats = db['overall_stats'].find()
            return list(overall_stats)
        except Exception as e:
            logging.error(f"Error retrieving profiles from MongoDB: {e}")
            return []


# Creation of All_Time_Ranked_Stats class for All_Time_Ranked_Stats collection
class All_Time_Ranked_Stats:
    def __init__(self, profile_name, highest_rank, highest_mmr, current_rank, current_mmr, ranked_wins,
                 ranked_loses, ranked_win_pct, ranked_matches, ranked_kills, ranked_deaths, ranked_k_d,
                 ranked_kills_match, ranked_kills_minute):

        self.profile_name = profile_name
        self.highest_rank = highest_rank
        self.highest_mmr = highest_mmr
        self.current_rank = current_rank
        self.current_mmr = current_mmr
        self.ranked_wins = ranked_wins
        self.ranked_loses = ranked_loses
        self.ranked_win_pct = ranked_win_pct
        self.ranked_matches = ranked_matches
        self.ranked_kills = ranked_kills
        self.ranked_deaths = ranked_deaths
        self.ranked_k_d = ranked_k_d
        self.ranked_kills_match = ranked_kills_match
        self.ranked_kills_minute = ranked_kills_minute

    def save_to_mongodb(self):
        try:
            existing_document = db['all_time_ranked_stats'].find_one({"profile_name": self.profile_name})
            if existing_document:
                # Profile already exists, update the document
                db['all_time_ranked_stats'].update_one(
                    {"_id": existing_document["_id"]},
                    {"$set": {
                        "highest_rank": self.highest_rank,
                        "highest_mmr": self.highest_mmr,
                        "current_rank": self.current_rank,
                        "current_mmr": self.current_mmr,
                        "ranked_wins": self.ranked_wins,
                        "ranked_loses": self.ranked_loses,
                        "ranked_win_pct": self.ranked_win_pct,
                        "ranked_matches": self.ranked_matches,
                        "ranked_kills": self.ranked_kills,
                        "ranked_deaths": self.ranked_deaths,
                        "ranked_k_d": self.ranked_k_d,
                        "ranked_kills_match": self.ranked_kills_match,
                        "ranked_kills_minute": self.ranked_kills_minute,
                    }}
                )
            else:
                # Profile doesn't exist, insert a new document
                db['all_time_ranked_stats'].insert_one({
                    "profile_name": self.profile_name,
                    "highest_rank": self.highest_rank,
                    "highest_mmr": self.highest_mmr,
                    "current_rank": self.current_rank,
                    "current_mmr": self.current_mmr,
                    "ranked_wins": self.ranked_wins,
                    "ranked_loses": self.ranked_loses,
                    "ranked_win_pct": self.ranked_win_pct,
                    "ranked_matches": self.ranked_matches,
                    "ranked_kills": self.ranked_kills,
                    "ranked_deaths": self.ranked_deaths,
                    "ranked_k_d": self.ranked_k_d,
                    "ranked_kills_match": self.ranked_kills_match,
                    "ranked_kills_minute": self.ranked_kills_minute
                })
        except Exception as e:
            logging.error(f"Error saving All Time Ranked Stats to MongoDB: {e}")

    # Retrieves all data from All_Time_Ranked_Stats collection and returns as a list
    @staticmethod
    def get_ranked_stats():
        try:
            ranked_stats = db['all_time_ranked_stats'].find()
            return list(ranked_stats)
        except Exception as e:
            logging.error(f"Error retrieving profiles from MongoDB: {e}")
            return []
