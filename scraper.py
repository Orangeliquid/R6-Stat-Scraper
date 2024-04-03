from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from database import Profile, Overall_Stats, All_Time_Ranked_Stats
import time
import datetime

# Setup Variables
GAME_URL = "https://r6.tracker.network/"
CHROMEDRIVER_PATH = "chromedriver.exe"
BRAVE_BINARY_LOCATION = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
WAIT_MAX = 10


def initialize_driver_headless():
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = BRAVE_BINARY_LOCATION
        options.add_argument('--headless')  # Set Chrome to run in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        service = Service(CHROMEDRIVER_PATH)
        output_driver = webdriver.Chrome(service=service, options=options)
        return output_driver
    except Exception as e:
        raise Exception(f"Error initializing driver: {e}")


def initialize_driver_headed():
    try:
        option = webdriver.ChromeOptions()
        option.binary_location = BRAVE_BINARY_LOCATION
        service = Service(CHROMEDRIVER_PATH)
        output_driver = webdriver.Chrome(service=service, options=option)
        return output_driver
    except Exception as e:
        raise Exception(f"Error initializing headless driver: {e}")


def select_platform(current_driver, platform: int) -> bool:
    try:
        # Find the anchor tag within the div
        platforms_div = current_driver.find_element(By.CLASS_NAME, "hp-search-form__platforms")
        platform_links = platforms_div.find_elements(By.TAG_NAME, "a")

        # Check if the provided platform index is valid
        if platform < 0 or platform >= len(platform_links):
            print("Error: Invalid platform index")
            return False

        # Select the specified platform
        selected_platform = platform_links[platform]
        selected_platform.click()
        return True
    except Exception as e:
        print(f"Error selecting platform: {e}")
        return False


class PlayerNotFoundError(Exception):
    pass


def scrape_profile_info(current_driver, profile_name):
    try:
        # Scrape Share Link
        share_link_element = current_driver.find_element(By.ID, 'perm-link')
        share_link = share_link_element.get_attribute("value").strip()
        print(f"Received share link before overall_stats are grabbed: {share_link}")

        # Create an instance of Profile with scraped data and save it
        profile_obj = Profile(
            profile_name=profile_name,
            share_link=share_link,
            current_date=datetime.datetime.now()
        )
        profile_obj.save_to_mongodb()

    except NoSuchElementException:
        raise PlayerNotFoundError("Player not found. Please check spelling and ensure platform is correct")

    except Exception as e:
        print(f"Error scraping profile info: {e}")

    return profile_obj


def scrape_overall_stats(current_driver, profile_name):
    try:

        # Scrape Wins
        wins_element = current_driver.find_element(By.XPATH,
                                                   '//div[@class="trn-defstat trn-defstat--large"]'
                                                   '[div[@class="trn-defstat__name"][contains(text(), "Wins")]]'
                                                   '//div[@class="trn-defstat__value"]')
        wins = wins_element.text.strip()

        # Scrape Win %
        win_percent_element = current_driver.find_element(By.XPATH,
                                                          '//div[@class="trn-defstat trn-defstat--large"]'
                                                          '[div[@class="trn-defstat__name"][contains(text(), "Win %")]]'
                                                          '//div[@class="trn-defstat__value"]')
        win_percent = win_percent_element.text.strip().split("%")[0]

        # Scrape Kills
        kills_element = current_driver.find_element(By.XPATH,
                                                    '//div[@class="trn-defstat trn-defstat--large"]'
                                                    '[div[@class="trn-defstat__name"][contains(text(), "Kills")]]'
                                                    '//div[@class="trn-defstat__value"]')
        kills = kills_element.text.strip()

        # Scrape K/D
        kd_element = current_driver.find_element(By.XPATH,
                                                 '//div[@class="trn-defstat trn-defstat--large"]'
                                                 '[div[@class="trn-defstat__name"][contains(text(), "KD")]]'
                                                 '//div[@class="trn-defstat__value"]')
        kd = kd_element.text.strip()

        # Create an instance of Overall_Stats with scraped data and save it
        overall_stats_obj = Overall_Stats(
            profile_name=profile_name,
            overall_wins=wins,
            overall_win_pct=win_percent,
            overall_kills=kills,
            overall_k_d=kd,
        )
        overall_stats_obj.save_to_mongodb()

    except NoSuchElementException:
        raise PlayerNotFoundError("Player not found. Please check spelling and ensure platform is correct")

    except Exception as e:
        print(f"Error scraping overall stats: {e}")

    return overall_stats_obj


class PlayerNotRankedError(Exception):
    pass


def scrape_all_time_ranked(current_driver, profile_name):
    try:
        # Scrape all the required data
        highest_rank_element = current_driver.find_element(By.XPATH, '//div[@class="r6-quickseason__image"]/img')
        highest_rank = highest_rank_element.get_attribute('title')

        highest_mmr_element = current_driver.find_element(By.XPATH, '//div[@title="Highest RP"]/div[2]')
        highest_mmr = highest_mmr_element.text.strip()

        current_rank_element = current_driver.find_element(By.XPATH,'//div[@class="trn-text--dimmed" '
                                                                     'and @style="font-size: 1.5rem;"]')
        current_rank = current_rank_element.text.strip()

        current_mmr_element = current_driver.find_element(By.XPATH, '//div[@style="font-family: Rajdhani; '
                                                                    'font-size: 3rem;"]')
        current_mmr = current_mmr_element.text.strip()

        ranked_wins_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedWins"]')
        ranked_wins = ranked_wins_element.text.strip()

        ranked_loses_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedLosses"]')
        ranked_loses = ranked_loses_element.text.strip()

        ranked_win_percentage_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedWLRatio"]')
        ranked_win_pct = ranked_win_percentage_element.text.strip().split("%")[0]

        ranked_matches_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedMatches"]')
        ranked_matches = ranked_matches_element.text.strip()

        ranked_kills_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedKills"]')
        ranked_kills = ranked_kills_element.text.strip()

        ranked_deaths_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedDeaths"]')
        ranked_deaths = ranked_deaths_element.text.strip()

        ranked_kd_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedKDRatio"]')
        ranked_k_d = ranked_kd_element.text.strip()

        ranked_kills_match_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedKillsPerMatch"]')
        ranked_kills_match = ranked_kills_match_element.text.strip()

        ranked_kills_minute_element = current_driver.find_element(By.XPATH, '//div[@data-stat="RankedKillsPerMinute"]')
        ranked_kills_minute = ranked_kills_minute_element.text.strip()

        # Create an instance of All_Time_Ranked_Stats with scraped data and share link
        all_time_ranked_stats_object = All_Time_Ranked_Stats(
            profile_name=profile_name,
            highest_rank=highest_rank,
            highest_mmr=highest_mmr,
            current_rank=current_rank,
            current_mmr=current_mmr,
            ranked_wins=ranked_wins,
            ranked_loses=ranked_loses,
            ranked_win_pct=ranked_win_pct,
            ranked_matches=ranked_matches,
            ranked_kills=ranked_kills,
            ranked_deaths=ranked_deaths,
            ranked_k_d=ranked_k_d,
            ranked_kills_match=ranked_kills_match,
            ranked_kills_minute=ranked_kills_minute,
        )

        # Save the stats to MongoDB
        all_time_ranked_stats_object.save_to_mongodb()

    except NoSuchElementException:
        raise PlayerNotRankedError("Player is not currently ranked.")

    except Exception as e:
        print(f"Error scraping all_time_ranked_stats: {e}")

    return all_time_ranked_stats_object


def scrape_stats(platform, profile, head):
    # The first bit of this function handles opening the webpage and navigating to the first profile and scraping all
    # data for collection

    # Select first name of profile list
    first_profile = profile[0]

    if head == "yes":
        # Initialize the driver - add "_head" to function call to run with head
        driver = initialize_driver_headed()
    else:
        driver = initialize_driver_headless()

    # Open the webpage
    driver.get(GAME_URL)

    # Select the platform of account
    select_platform(driver, platform)

    # Find the search bar element
    search_bar = driver.find_element(By.NAME, "name")

    # Type the keywords into the search bar
    search_bar.send_keys(first_profile)
    wait = WebDriverWait(driver, WAIT_MAX)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "name")))

    # Submit the form
    search_bar.send_keys(Keys.RETURN)  # Pressing Enter key to submit the form

    try:
        # Scrape profile info
        scrape_profile_info(driver, first_profile)
        print("Found profile info")
    except PlayerNotFoundError:
        print("Profile info not found. Please check spelling and ensure platform is correct")
        print("")
        # Handle this case as needed

    try:
        # Scrape info
        scrape_overall_stats(driver, first_profile)
        print(f"Overall Stats for {first_profile} acquired:")
    except PlayerNotFoundError:
        print("Error retrieving overall stats")
        print("")
        # Handle this case as needed

    try:
        scrape_all_time_ranked(driver, first_profile)
        print(f"All Time Ranked Stats acquired")
        print("-----------------------------------------------")
        print("")
    except PlayerNotRankedError:
        print("The player is not currently ranked.")
        print("")
        # Handle this case as needed

    # This if statement is for lists of profile names, pressing search, entering next profile, scraping data, repeat
    if len(profile) > 1:
        time.sleep(2)
        for number in range(1, len(profile)):
            # Click the small search icon while currently being on a previously scraped profile
            click_search_svg = driver.find_element(By.CLASS_NAME, "trn-nav-mini-search-box__icon")
            click_search_svg.click()
            # Find the search bar element - Update this with the appropriate selector for the search bar on the website
            search_bar = driver.find_element(By.XPATH,
                                             "//input[@placeholder='Search']")

            # Type the keywords into the search bar
            search_bar.send_keys(profile[number])
            wait = WebDriverWait(driver, WAIT_MAX)
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "name")))

            # Submit the form
            search_bar.send_keys(Keys.RETURN)  # Pressing Enter key to submit the form

            try:
                # Scrape profile info
                scrape_profile_info(driver, profile[number])
                print("Found profile info")
            except PlayerNotFoundError:
                print("Profile info not found. Please check spelling and ensure platform is correct")
                print("")
                # Handle this case as needed

            try:
                # Scrape info
                scrape_overall_stats(driver, profile[number])
                print(f"Overall Stats for {profile[number]} acquired")
            except PlayerNotFoundError:
                print("Overall stats not found.")
                print("")

            try:
                scrape_all_time_ranked(driver, profile[number])
                print(f"All Time Ranked Stats acquired")
                print("-----------------------------------------------")
                print("")
            except PlayerNotRankedError:
                print("The player is not currently ranked.")
                print("")

    # Close the browser
    driver.quit()
