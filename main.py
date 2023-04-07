from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
# Set up the headless browser

print('Successfully Started!')
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
# Send a request to the website
url = 'https://www.bovada.lv/sports/basketball/nba'
driver.get(url)
# Wait for the dynamic content to load
element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'grouped-events'))
)
# Scrape the dynamic content
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

date = []
home_array = []
away_array = []
home_spread_array = []
away_spread_array = []
home_odds_array = []
away_odds_array = []
over_odds_array = []
under_odds_array = []

for ele in soup.findAll('section', attrs={'class': 'coupon-content more-info'}):
    dates_and_times = ele.find('span', {'class': 'period hidden-xs'})
    date.append(dates_and_times.text)

    home_teams_ele = ele.find('h4', {'class': 'competitor-name'})
    home_teams_name = home_teams_ele.find('span', {'class': 'name'})
    home_array.append(home_teams_name.text)

    away_teams_ele = ele.find('h4', {'class': 'competitor-name favorite'})
    away_teams_name = away_teams_ele.find('span', {'class': 'name'})
    away_array.append(away_teams_name.text)

    spreads_ele = ele.find('sp-outcomes', {'class': 'markets-container'})

    new_array = []
    for x in spreads_ele.text.split(" "):
     if x != '':
        new_array.append(x)

    home_spread_array.append(new_array[0] + new_array[1])
    away_spread_array.append(new_array[2] + new_array[3])
    home_odds_array.append(new_array[4])
    away_odds_array.append(new_array[5])
    over_odds_array.append(new_array[6] + new_array[7])
    under_odds_array.append(new_array[8] + new_array[9])


dict = {'date-time': date, 'home-team': home_array, 'away-team': away_array, 'home-spread': home_spread_array, 'away-spread': away_spread_array, 'home-odds': home_odds_array, 'away-odds': away_odds_array, 'over-odds': over_odds_array, 'under-odds': under_odds_array, 'total': ''}
df = pd.DataFrame(dict)
print(df)

df.to_csv('data.csv')
print('Successfully Scrapped!')

driver.quit()