# R6-Stat-Scraper

This application scrapes your desired Rainbow 6 Siege profiles for profile information, overall stats, and all time ranked stats using Selenium WebDriver. This information is then sent to the three collections mentioned before using MongoDB. Visualization of said information is generated using Matplotlib and Seaborn! This is a small taste of what Selenium/MongoDB/Matplotlib/Seaborn can do. Feel free to add or completely change this scraper to suit your needs!

Side-note: MongoDB is used to keep track of all collectiuons - Make sure MongoDB is installed on device

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Screenshots](#screenshots)
    - [Database](#database)
    - [Collection-Example](#collection-example)
    - [Bar-Chart-Example](#bar-chart-example)
- [License](#license)

## Installation

To run the R6-Stat-Scraper locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Orangeliquid/R6-Stat-Scraper.git
   cd R6-Stat-Scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure CHROMEDRIVER_PATH is correctly set and chromedriver.exe is in the working directory

4. Locate the BRAVE_BINARY_LOCATION on your machine and ensure the variable is set to the correct path

## Usage

1. Ensure MongoDB is installed(Feel free to use MongoDBCompass to view the database)

2. Enter all profiles in "player_list" for scraping

3. Start the application:
   ```bash
   python main.py
   ```
   
4. Check MongoDBCompass or Mongosh after scraping to ensure data has been collected and added to DB
   
5. Choose which bar graphs you would like to create with data, feel free to create your own!

## Features

- Multi-Profile scraping (up to 7 profiles per "scrape_stats" function call) at once
- Headed Selenium WebDriver scraping for your viewing pleasure or headless for simplicity
- Four bar chart function to visualize data acquired, or creation of new functions to visualize other collections
- Three class creations for different categories of data found on TRN, allowing for easy databasing

## Screenshots

### Database

![MongoDB_Structure](https://github.com/Orangeliquid/R6-Stat-Scraper/assets/127478612/ec75efbe-ed1e-4140-a107-6f07c4901232)

### Collection Example

![ATRS_example](https://github.com/Orangeliquid/R6-Stat-Scraper/assets/127478612/fc48770d-87e6-47b9-be51-a1973a6923b0)

### Bar Chart Example

![Overall_Histogram1](https://github.com/Orangeliquid/R6-Stat-Scraper/assets/127478612/7bad42c6-3e1d-4592-a113-cccd194826fe)

## License

This project is licensed under the [MIT License](LICENSE.txt).
