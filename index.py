# Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import colorama

COOKIE_NAME = 'pun_cookie_67386b'
DOMAIN = 'gamesense.pub'

# Our current scraped UID
uid = 2

# Read config/config.json
with open('config/config.json') as config_json:
    config = json.load(config_json)

    # Initialize our driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://gamesense.pub/')
    driver.add_cookie({'name': COOKIE_NAME, 'value': config['cookie'], 'domain': DOMAIN})

while True:
    # Open current UID profile page
    driver.get(f'https://gamesense.pub/forums/profile.php?id={uid}')

    # Check if we are at the last UID
    if 'Bad request. The link you followed is incorrect or outdated.' in driver.find_element(By.TAG_NAME, 'body').text:
        print(f'{colorama.Fore.RED}[!]{colorama.Style.RESET_ALL} Last UID ({uid}) reached.')
        break

    # Get username, title
    dl = driver.find_elements(By.TAG_NAME, 'dl')
    general_dl = dl[0]
    username = general_dl.find_element(By.XPATH, './dt[.="Username"]/following-sibling::dd').text
    title = general_dl.find_element(By.XPATH, './dt[.="Title"]/following-sibling::dd').text

    # Check if there's inviter username
    try:
        inviter_dl = dl[3]
        inviter_username = inviter_dl.find_element(By.XPATH, './dt[.="Invited by"]/following-sibling::dd').text
    except:
        inviter_username = 'Unknown'

    # Output data
    print(f'{colorama.Fore.GREEN}[+]{colorama.Fore.RESET} Processed UID {uid} | {inviter_username} -> {username} ({title})')

    with open('data.txt', 'a') as data_file:
        data_file.write(f'{uid},{inviter_username},{username},{title}\n')

    # Increment UID
    uid += 1

    time.sleep(0.5)