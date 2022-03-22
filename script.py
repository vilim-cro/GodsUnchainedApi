import requests
import coinmarketcap_api
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BROJ_PON = 7
DRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'

def delete_content(file_name):
    file = open(file_name,"r+")
    file.truncate(0)
    file.close()

def find_candidates():
    delete_content("names.txt")
    names_file = open("names.txt", "a")
    SITE_PATH = "https://gudecks.com/meta/card-rankings?userRank=4&decksWithCard=5000"
    driver.get(SITE_PATH)
    names = []
    cookie_accept = 0
    try:
        cookie_accept = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="I understand"]'))
                )
    finally:
        cookie_accept.click()
    for i in range(BROJ_PON):
        try:
            names = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-ranking-name'))
                    )
        finally:
            for name in names:
                names_file.write(name.get_attribute('innerHTML'))
                names_file.write('\n')
        next = driver.find_element(By.XPATH, '//button[text()=">"]')
        next.click()
    
    names_file.close()

# Gets the card price in GODS and ETH
def get_gods_card_price(name):
    url = f"https://api.x.immutable.com/v1/orders?order_by=buy_quantity&direction=asc&status=active&buy_token_address=0xccc8cb5229b0ac8069c51fd58367fd1e622afd97&sell_token_name={name.replace(' ', '%20')}&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
    headers = {"Accept": "application/json"}
    try:
        result = requests.request("GET", url, headers=headers).json()["result"]
        return result[0]["buy"]["data"]["quantity"]
    except:
        return -1

def get_eth_card_price(name):
    url = f"https://api.x.immutable.com/v1/orders?order_by=buy_quantity&direction=asc&status=active&buy_token_type=eth&sell_token_name={name.replace(' ', '%20')}&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
    headers = {"Accept": "application/json"}
    try:
        result = requests.request("GET", url, headers=headers).json()["result"]
        return result[0]["buy"]["data"]["quantity"]
    except:
        return -1


# Find last price of GODS and ETH with conimarketcap API
gods_USD = round(coinmarketcap_api.get_price('GODS'), 2)
eth_USD = int(coinmarketcap_api.get_price('ETH'))
print(f"GODS: {gods_USD}$, ETH. {eth_USD}$")

# Setup chrome webdriver
op = Options()
op.add_argument('--headless')
driver = webdriver.Chrome(DRIVER_PATH, options=op)

find_candidates()

# Load card names
names_file = open("names.txt", "r")
names = names_file.read().splitlines()

delete_content("GODS-ETH.txt")
delete_content("ETH-GODS.txt")
GODS_ETH_file = open("GODS-ETH.txt", "a")
ETH_GODS_file = open("ETH-GODS.txt", "a")

cijena = 0
for name in names:
    gods_cijena = int(get_gods_card_price(name)) / 1.0E18 * gods_USD
    price = get_eth_card_price(name)
    eth_cijena = int(get_eth_card_price(name)) / 1.0E18 * eth_USD
    razlika = gods_cijena - eth_cijena
    rel_raz = razlika / eth_cijena * 100
    if gods_cijena >= 0 and eth_cijena >= 0:
        if eth_cijena > 1:
            print(f"{name} | {round(gods_cijena, 2)}$ (GODS) | {round(eth_cijena, 2)}$ (ETH) | {round(razlika, 1)}$ | {round(rel_raz, 1)}%")
        if (eth_cijena <= 15 and eth_cijena >= 0.5 and rel_raz <= -8):
            ETH_GODS_file.write(f"{name} | {round(gods_cijena, 2)}$ (GODS) | {round(eth_cijena, 2)}$ (ETH) | {round(razlika, 1)}$ | {round(rel_raz, 1)}%\n")
        if (eth_cijena <= 15 and razlika >= 0.5 and rel_raz >= 10):
            GODS_ETH_file.write(f"{name} | {round(gods_cijena, 2)}$ (GODS) | {round(eth_cijena, 2)}$ (ETH) | {round(razlika, 1)}$ | {round(rel_raz, 1)}%\n")

ETH_GODS_file.close()
GODS_ETH_file.close()